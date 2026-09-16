from __future__ import annotations

from copy import deepcopy
from difflib import unified_diff
from typing import Any, Iterable

from .source_library import SOURCE_DISPOSITIONS, SourceRecord

RECONCILED_PHASES = frozenset({"RECONCILED", "REGISTERED"})


def _validate_record(record: SourceRecord) -> None:
    if record.phase not in RECONCILED_PHASES:
        raise ValueError(
            f"source update proposal requires reconciled source: {record.source_id}"
        )
    if record.disposition not in SOURCE_DISPOSITIONS or record.disposition == "UNREVIEWED":
        raise ValueError(
            f"source update proposal requires reconciled disposition: {record.source_id}"
        )
    if record.disposition == "ACCEPTED_CORE":
        if not record.accepted_authority.strip():
            raise ValueError("ACCEPTED_CORE proposal requires explicit accepted authority")
        if record.hold_items:
            raise ValueError("ACCEPTED_CORE proposal cannot carry HOLD items")
    elif record.accepted_authority.strip():
        raise ValueError("non-ACCEPTED_CORE disposition cannot emit Core promotion")


def build_register_rows(records: Iterable[SourceRecord]) -> list[dict[str, Any]]:
    ordered = sorted(records, key=lambda record: record.source_id)
    source_ids = [record.source_id for record in ordered]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("duplicate source_id in source update proposal")

    rows: list[dict[str, Any]] = []
    for record in ordered:
        _validate_record(record)
        rows.append(
            {
                "source_id": record.source_id,
                "uri": record.uri,
                "digest": record.digest,
                "size": record.size,
                "media_type": record.media_type,
                "artifact_role": record.artifact_role,
                "provenance": record.provenance,
                "tier": record.tier,
                "phase": record.phase,
                "disposition": record.disposition,
                "accepted_authority": record.accepted_authority,
                "authority_refs": list(record.authority_refs),
                "core_rule_ids": list(record.core_rule_ids),
                "affected_modules": list(record.affected_modules),
                "hold_items": list(record.hold_items),
                "metadata": deepcopy(record.metadata),
                "created_at": record.created_at,
                "updated_at": record.updated_at,
            }
        )
    return rows


def _cell(value: Any) -> str:
    text = str(value)
    return (
        text.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def _render_index_block(rows: list[dict[str, Any]]) -> str:
    lines = [
        "<!-- BEGIN BBMA SOURCE AUTONOMY PROPOSAL -->",
        "### Proposed source-register update",
        "| SourceID | Phase | Disposition | Tier | Provenance | Digest | Authority | HOLD |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        authority = row["accepted_authority"] if row["disposition"] == "ACCEPTED_CORE" else ""
        holds = ", ".join(row["hold_items"])
        lines.append(
            "| {source_id} | {phase} | {disposition} | {tier} | {provenance} | {digest} | {authority} | {holds} |".format(
                source_id=_cell(row["source_id"]),
                phase=_cell(row["phase"]),
                disposition=_cell(row["disposition"]),
                tier=_cell(row["tier"]),
                provenance=_cell(row["provenance"]),
                digest=_cell(row["digest"]),
                authority=_cell(authority or "-"),
                holds=_cell(holds or "-"),
            )
        )
    lines.append("<!-- END BBMA SOURCE AUTONOMY PROPOSAL -->")
    return "\n".join(lines)


def build_index_patch(
    records: Iterable[SourceRecord],
    current_text: str,
    anchor: str,
) -> dict[str, Any]:
    if not anchor:
        raise ValueError("anchor is required")
    if current_text.count(anchor) != 1:
        raise ValueError("anchor must occur exactly once")
    rows = build_register_rows(records)
    newline = "\r\n" if "\r\n" in current_text else "\n"
    block = _render_index_block(rows).replace("\n", newline)

    anchor_start = current_text.index(anchor)
    line_end = current_text.find("\n", anchor_start + len(anchor))
    if line_end == -1:
        insertion_at = len(current_text)
        inserted_text = newline + newline + block + newline
    else:
        insertion_at = line_end + 1
        inserted_text = newline + block + newline

    proposed_text = current_text[:insertion_at] + inserted_text + current_text[insertion_at:]
    diff = "".join(
        unified_diff(
            current_text.splitlines(keepends=True),
            proposed_text.splitlines(keepends=True),
            fromfile="SOURCE_INDEX/current",
            tofile="SOURCE_INDEX/proposed",
        )
    )
    return {
        "anchor": anchor,
        "source_ids": [row["source_id"] for row in rows],
        "inserted_text": block,
        "proposed_text": proposed_text,
        "diff": diff,
    }
