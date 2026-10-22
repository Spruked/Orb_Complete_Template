# ORB Complete Template — Integration Inventory and Compatibility Assessment

**Date:** 2026-10-22 · **Status:** Read-only assessment. No source repository was modified.
**Decisions applied (GPT Turn 57, owner-accepted):** Orbot's three-runtime architecture is the foundation; Orb Weaver's manufacturing model is the provisioning standard; the two A.I.M.S. lines merge into one tested `Spruked/AIMS` release; Orb Weaver `memory-consent-boundary` @ `5375b23` is the integration reference.

## Sources examined

| Repository | Ref | Notes |
|---|---|---|
| `Spruked/Orbot` (private) | `5b2cf54` (2026-10-20) | Three runtimes, supervisor, TPC, Correspondence Engine + Doctrine, Vault-Logic-System with A.I.M.S., Tauri desktop |
| `Spruked/Orb_Weaver` (private) | `memory-consent-boundary` @ `5375b23` (2026-10-14) | Manufacturing, golden template `Website_Orb_Final`, ORB backend, screen motion, MCP server, inculcation.md, A.I.M.S. fork |
| `Spruked/AIMS` (private) | `d72a3ce` (2026-09-17) | Canonical A.I.M.S. repository |
| `Spruked/Correspondence_Engine_skg_v1` | default branch | Standalone Correspondence Engine |
| `Spruked/POPS_website` | `dev/pops-demo-launch-20261022` @ `29e364e` | A.I.M.S. copy, ORB harness |
| `Spruked/Vault_System_1.0` | `428c1c4` | Canonical v1 seeds + locked Core Four v2 extensions |

---

## 1. Summary

The pieces of one complete ORB already exist, but in parallel versions. Four findings decide the integration order:

1. **A.I.M.S. has forked into two lines that neither contains the other** (Orbot and Orb Weaver). Both fork from the same base as `Spruked/AIMS`. Neither has fixed the two known defects.
2. **The Doctrine v1 "seal" is the SHA-256 of an empty string**, and the check passes whenever no doctrine text is supplied. Doctrine is not currently sealed in any meaningful sense.
3. **The Core Four is implemented at least four separate times** (TPC philosophers, Orbot Core-4 tribunal, the MCP server's R-Substrate, CALI SKG) with different role assignments, in addition to the locked Core Four v2 specification.
4. **Orb Weaver's ORB work is spread across 12 branches with unmerged commits** (13 refs; two are duplicates); `main` is 88 commits behind the integration reference.

## 2. Component classification

### 2.1 Reuse unchanged

| Component | Source | Evidence |
|---|---|---|
| Canonical v1 philosopher seeds | `Vault_System_1.0` | Byte-identical to TPC's `philosophers/seed_*.json` in Orbot **and** in the golden template (SHA-256 `6c94f41d…`, `92047181…`, `835db9f9…`, `74e17ef7…`) |
| Core Four v2 extensions + review-record contract v0.2 | `Orb_Complete_Template/Orb_Vault_Template/` | Locked, sealed, verified |
| Runtime supervisor and service boundaries | Orbot `runtime/` | Communication :16521, Cognition/Governance :16524, Motion :16525; refuses occupied ports; single A.I.M.S. writer hosted in Communication |
| Manufacturing contract (12 steps, storage boundary, provenance fields, clean A Posteriori per customer, fail-closed integrity) | Orb Weaver `manufacturing/website_orb/` | Documented contract plus compiler, audit, schemas |
| Correspondence Engine | Orbot or standalone | Copies differ only in 2 files of the EGF visualization module |
| ISS timekeeping | golden template `backend/timekeeping` + vendored `interplanetary_stardate_syncrometer` | Declared authoritative ordering field in `PACKAGE_MANIFEST.json` |
| inculcation.md v1.0 | Orb Weaver `artifacts/inculcation.md` | Canonical Website ORB professional inculcation (not present in Orbot or the golden template) |

### 2.2 Reuse through an adapter

| Component | Source | Adapter needed |
|---|---|---|
| Website ORB answer path (Vault-first, TPC on knowledge miss, Doctrine gate) | golden template `backend/` | Becomes the Website product's Cognition adapter over the standard Cognition runtime; single backend today, three runtimes in the template |
| Site payload model (`A_Priori_Vault` catalog/ontology/qa/policies/site_skg, `compiled_orb/`) | golden template + manufacturing | Payload loader per product; matches the locked decision that mutable site facts are A Posteriori with provenance (see 2.3, item 5) |
| Screen motion (pointer, kinetic transit, LiDAR cache, target validation, voice lifecycle, captions; 45 files) | Orb Weaver `frontend/src/orb/` | Motion runtime's screen adapter; Orbot's motion runtime is a disabled ROS/NATS robotics bridge |
| Robotic motion | Orbot `runtime/motion/ral_ros_bridge/` | Motion runtime's robotics adapter (prototype; `/commands` always rejects) |
| Desktop embodiment | Orbot `desktop/` (Tauri 2) | Desktop product adapter; embodiment, not a runtime |
| Inference gateway (llama.cpp, Aphrodite, TensorRT-LLM, Ollama lanes) | Orb Weaver branch `feature/orb-inference-three-engine-gateway` (25 commits, unmerged) | Communication runtime's articulation provider; Orbot already targets llama.cpp on :16520 |
| Desktop tools | Orb_Assistant `user_dock_station/mcp_server` (28 tools: control, click, type, scroll, screenshot, OCR, browser, clipboard, windows, apps, substrate, session) and golden template `dock_adapter/orb_desktop_mcp.py` | Tool provider behind the control plane; requires a unified manifest (2.3, item 6) |

### 2.3 Requires reconciliation

1. **A.I.M.S. — two lines, merge required.**
   - Base: `Spruked/AIMS` = POPS copy (0 differing files).
   - Orbot line adds `host_knowledge.py`, `host_priority.py`, `host_sessions.py`; adds opt-in probation retrieval (`indexes.py`) and `ShortTermMemory.remove()`.
   - Orb Weaver line adds `outcomes.py` (OutcomeSignal), `maintenance.py` (privacy-safe telemetry), `schema.py`, `session_memory.py`, `authority_class` on atoms, and changes to `vault.py`, `memory_layer.py`, `retrieval_ledger.py`, `skg/domain.py`, `skg/trio.py`.
   - Neither line fixes: automatic retirement below 0.20 (`skg/domain.py`), or relation-blind `relevance_weight()` that lets contradiction edges raise relevance. Both are release blockers (owner decision).
   - Two session-memory designs (`host_sessions.py` vs `session_memory.py`) must be reconciled into one.

2. **Doctrine v1 — the seal is not real.**
   - `Correspondence_Engine_skg_v1/doctrine/evaluator.py`: `DOCTRINE_CANONICAL_SHA256 = e3b0c442…b855`, which is `sha256("")`.
   - When `doctrine_source_text` is omitted, `hash_valid = True` (fails open). When real doctrine text is supplied, the check fails, because no non-empty text hashes to the empty-string digest.
   - The provenance amendment `Doctrine_v1.0_Provenance_Amendment_HLSF_Core4.md` hashes to `040c8008…09a1`; the ratified Doctrine text itself was not found as a file in Orbot or Orb Weaver (a PDF exists in Orb_Assistant).
   - Separately, the golden template's `doctrine_gate.py` is a simple action-class blocklist, a different implementation from the Doctrine v1 evaluator.
   - Required: locate the ratified Doctrine text, seal it with its real hash, make the check fail closed, and decide which gate is canonical.

3. **Core Four — four implementations, different roles.**
   | Implementation | Kant | Locke | Hume | Spinoza |
   |---|---|---|---|---|
   | Locked Core Four v2 (knowledge/ethics review) | truthfulness, people as ends, informed choice | provenance, consent, supersession | proportion, causation, is–ought, sympathy | whole system, consistency, adequacy, learning |
   | Orbot `ral_core/core4.py` (action admission) | authority rank and dangerous capabilities | WorldState staleness, forbidden/live targets | confidence floor 0.35, ambiguity, risk + confirmation | coherence, goal alignment, continuity (a ranking signal, not a veto) |
   | TPC philosopher loops | softmax reasoning loops over the shared v1 seeds | | | |
   | MCP server `orb_substrate/r_substrate.py` | four philosopher nodes + ECM + HLSF for desktop tools | | | |
   - The owner has ruled the redundancy with TPC intentional. Still required: a decision on how Orbot's action-admission Core-4 relates to the locked v2 lenses (same lenses in an action context, or separate), and whether the MCP R-Substrate is retired in favor of the runtime path. Under the locked rule, lens verdicts are findings; only the deterministic controller decides.

4. **TPC — two copies, 20 differing entries.** Orbot vs golden-template vendor differ in `acp_synthesis.py`, `api/main.py`, `core/ecm.py`, cochlear processor files, docs, and packaging. Seeds identical. Pick one canonical TPC and pin it.

5. **Site knowledge classification.** The golden template and POPS store settled site truth as A Priori; the locked decision classifies mutable site facts (prices, hours, policies) as A Posteriori with provenance, because A Priori atoms cannot be retired. Reproduced in POPS: superseded page copy stays Active.

6. **MCP / API manifests — no unified manifest exists.** Inputs: the 28-tool MCP server, the golden template's desktop MCP adapter, the A.I.M.S. OpenAPI spec, Orbot's runtime endpoints (Communication: voice, sessions, memory, conversation, status; Cognition: field observe/status; Motion: commands). One manifest must define every tool, its authority requirement, and its runtime owner.

7. **Inculcation placement.** inculcation.md v1.0 exists only in Orb Weaver `artifacts/`. The complete template needs it as the A Priori professional layer, assembled per the inculcation contract (Core Four → Professional Inculcation → Site Seed → Current Context → TPC → Articulation).

## 3. Orb Weaver branch inventory

Measured against `memory-consent-boundary` (`git cherry` distinguishes new patches from patches already applied under a different hash).

### Relevant to the complete ORB

| Branch | New commits | Content | Destination |
|---|---|---|---|
| `feature/orb-inference-three-engine-gateway` | 25 | Three-lane inference gateway, deploy profiles, TensorRT engine runtime | Communication runtime (articulation provider) |
| `orb-truth-audit-2026-08-25` | 23 | Two-pass browser pointer verification, verified safe-subset pointer recovery, tech-stack and local-SEO crawl intelligence | Motion (pointer recovery); manufacturing (crawl) |
| `fix/lidar-evidence-runtime-completion-2026-09-06` | 11 | IPv6 LiDAR telemetry, scan pause evidence, journey stage validation, LiDAR CI | Motion (screen) |
| `restore/lidar-2d-mapping-package` | 10 | LiDAR 2D mapping manifest, telemetry endpoint and client, React hook | Motion (screen) |
| `agency-contract-integration` (+ dated duplicate) | 10 | Agency primitives registry, validation tests, telemetry exposure | Cognition/Governance (Agency Envelope) |
| `fix/preflight-pointer-ping-light` | 8 | Verified live-DOM pointer fallbacks, non-null merged pointer records | Motion (screen) |
| `fix/truemark-rendered-pointer-scan` | 3 (+4 already applied) | Rendered DOM validation, zero-target scans not labeled ready | Manufacturing |
| `fix/customer-map-crawl-seeds` | 2 (+1 already applied) | Customer crawls protected from Orb Weaver route seeds | Manufacturing |

### Product-specific (Orb Weaver site/business; not ORB foundation)

`paid-customer-review-package` (17), `returning-account-login-shortcut` (6), `scaffold/targets-2-through-5` (2), `recovered-marketplace` (2).

### Fully contained in the reference (no unique commits)

`development/startup-account-session-16667`, `checkpoint/target-one-working-2026-09-07`, `main`, `orb-integrity-navigation-integration-2026-08-21`, `topological-worldstate-orbot-handoff`, `orb-integrity-fix3-guidance`, `orb/catalog-audit-reporting-20260820`, `local-orb-weaver-snapshot-2026-08-10`, `fix/website-orb-vault-manufacturing-contracts`, `feature/tesseract-lidar-weaves`, `fix/ga4-project-settings`, `desktop-orb-now-surface`, `vault-consolidation`.

These relevant branches diverged 88 to 288 commits behind the reference. They are integration inputs to re-apply with tests, not branches to merge wholesale.

## 4. Release blockers before any component is pinned

1. A.I.M.S.: retirement candidacy instead of auto-retire at 0.20; relation-aware relevance; one session-memory design; single-writer enforcement; backward-compatible Vault loading.
2. Doctrine v1: real seal over the ratified text; fail-closed verification.
3. Site knowledge stored so superseded facts can be retired.

## 5. Proposed integration order

1. Runtime shell from Orbot into `Orb_Complete_Template/runtime/` (history preserved).
2. Merged A.I.M.S. release (test-first; blockers above) and pin.
3. Doctrine sealing; canonical TPC and Correspondence Engine pinned.
4. Core Four reconciliation decision, then rule-engine and controller contract.
5. Inculcation layer and site-payload loader.
6. Screen motion adapter, applying the relevant pointer and LiDAR branch work with tests.
7. Unified tool and API manifest; MCP tools behind the control plane.
8. Manufacturing pipeline producing products from the template; shared regression suite.

## 6. Owner decisions required

1. **Core Four in action admission:** treat Orbot's Core-4 tribunal as the same four lenses applied to actions (aligned to the locked v2 roles), or as a separate admission check?
2. **MCP R-Substrate:** retire it in favor of the runtime cognition path, or keep it as an independent desktop-tool check?
3. **Canonical TPC:** Orbot's copy or the golden template's vendored copy?
4. **Doctrine text:** where is the ratified Doctrine v1.0 text to seal?
5. **Canonical gate:** Doctrine v1 evaluator, the golden template's action-class gate, or both in sequence?
