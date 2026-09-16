from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .source_library import SOURCE_DISPOSITIONS, SourceRecord, SourceRegistry

RECONCILIATION_DISPOSITIONS = frozenset(
    disposition for disposition in SOURCE_DISPOSITIONS if disposition != "UNREVIEWED"
)

@dataclass(frozen=True)
class ReconciliationItem:
    source_id: str
    claim_id: str
    disposition: str
    hold_items: tuple[str, ...] = ()
    notes: str = ""

def enqueue_claims(
    source_id: str,
    claims: Iterable[dict[str, Any]],
) -> list[ReconciliationItem]:
    source_id = source_id.strip()
    if not source_id:
        raise ValueError("source_id is required")
    items: list[ReconciliationItem] = []
    for claim in claims:
        claim_id = str(claim.get("claim_id", "")).strip()
        disposition = str(claim.get("disposition", "")).strip().upper()
        if not claim_id:
            raise ValueError("claim_id is required")
        if disposition not in RECONCILIATION_DISPOSITIONS:
            raise ValueError(f"invalid reconciliation disposition: {disposition}")
        holds = tuple(str(item).strip() for item in claim.get("hold_items", ()) if str(item).strip())
        items.append(
            ReconciliationItem(
                source_id=source_id,
                claim_id=claim_id,
                disposition=disposition,
                hold_items=holds,
                notes=str(claim.get("notes", "")),
            )
        )
    return items
def record_reconciliation(
    registry: SourceRegistry,
    source_id: str,
    disposition: str,
    *,
    accepted_authority: str = "",
    hold_items: Iterable[str] = (),
) -> SourceRecord:
    disposition = disposition.strip().upper()
    if disposition not in RECONCILIATION_DISPOSITIONS:
        raise ValueError(f"invalid reconciliation disposition: {disposition}")
    record = registry.set_disposition(
        source_id,
        disposition,
        accepted_authority=accepted_authority,
    )
    return registry.set_hold_items(record.source_id, hold_items)

def eligible_for_core_link(record: SourceRecord) -> bool:
    return (
        record.phase in {"RECONCILED", "REGISTERED"}
        and record.disposition == "ACCEPTED_CORE"
        and bool(record.accepted_authority)
        and not record.hold_items
    )
