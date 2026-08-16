# P1 Compile Repair Record

Status: **NATIVE METAEDITOR COMPILE VERIFIED BY USER — 0 ERRORS, 0 WARNINGS**

Canonical source:
`blueprint/source/BBMA_PROFESSIONAL_EA.mq4`

Canonical source SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

Compile repair scope:
- MQL4 array-return helpers converted to output-array parameters;
- reserved identifier `input` removed from affected helpers/locals;
- MQL4 object/struct parameters converted to pass-by-reference where required;
- `RiskValidationSnapshot.StopLevel` added and populated for M17 broker-stop validation;
- M17 `ValidateSLTP` rejection propagation signature aligned;
- local struct-array aggregate initialization converted to explicit assignments;
- warning-only cleanup for magic-number parameter shadowing/overflow guard and hex conversion.

These repairs are compile/integration repairs only. They do not intentionally alter locked BBMA strategy semantics.
