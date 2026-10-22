# ORB_Vault_Template

Vault template for the ORB: the master seed vault with the owner-approved Core Four v2 ethical extensions, and the Core Four review-record contract.

## Contents

- `master_seed_vault/` — copied unchanged from `Spruked/Vault_System_1.0` at commit `428c1c4`. Includes the four canonical v1 philosopher seeds (`seed_locke.json`, `seed_hume.json`, `seed_kant.json`, `seed_spinoza.json`) and their locked companions (`seed_*.extension.v2.json`).
- `contracts/CORE4_REVIEW_RECORD_CONTRACT.md` — review-record contract v0.2, owner approved and locked 2026-10-22. Its SHA-256 is in the adjacent `.sha256` file.

## Integrity

Each `seed_*.extension.v2.json` references its v1 seed by the SHA-256 of the file bytes and carries its own seal (SHA-256 over sorted-key, compact UTF-8 JSON, excluding the `seal` field).

Owner and curator: Bryan A. Spruk.
