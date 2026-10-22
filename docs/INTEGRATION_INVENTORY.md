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

2. **Doctrine v1 — no implementation verifies the ratified text.** Located the governance record in `Spruked/Governance_Orb_Interface_Docking_Station` @ `210a884` (2026-03-07), `orb-governance/doctrine/`:

   | File | Actual SHA-256 (bytes as stored) |
   |---|---|
   | `Doctrine_v1.0+B+C+D.txt` (3,700 bytes, LF) | `250e189900e4428576d4d8184403b2746f4e770f370db8ec024b82184cefbb72` |
   | same file with Windows CRLF line endings | `f122266f90474fdebe8adb57b4ecdc51f691cad3326dd70dafe2e5b6fce44bb8` (the `F122266F…` hash Orb Weaver production verifies) |
   | `doctrine_record_v1.0.md`, `doctrine_v1.0_hash.txt`, `doctrine_readme.md` | each records `b601457a…` |

   Findings:
   - **Neither recorded hash can be reproduced.** `27c7bfa7…` and `b601457a…` match no byte variant tested (LF/CRLF, BOM, trailing newline, UTF-16). They cannot be hashes of `Doctrine_v1.0+B+C+D.txt`, because that file contains both values inside itself; a file cannot contain its own SHA-256.
   - **The file named `Doctrine_v1.0+B+C+D.txt` is a freeze-confirmation summary, not the constitution.** It references Articles I–VIII and Appendices B, C, D but does not contain their text. The Articles were not found in any repository examined.
   - **The production seal depends on line endings.** The same content hashes to `250e1899…` (LF, as stored in git) or `f122266f…` (CRLF, Windows checkout).
   - **Every gate fails open or checks a claimed string:** Orbot's evaluator anchors to `sha256("")` and passes when no text is supplied; `Orb_Assistant_Desktop_2026` (`doctrine_governance.py`) compares a caller-supplied hash string against the two recorded values and passes when none is supplied, never hashing the file; the golden template's `doctrine_gate.py` is an action-class blocklist.
   - **Google Drive (folder "02 — Doctrine v1 · Governance") holds the source text as Google Docs, not as a byte file:** " Doctrine v1.0" (created 2026-02-09, last modified 2026-02-10) contains Articles I–VIII, the analysis sections, and Appendix A; "Doctrine v1 Governance Baselineshe 256" holds the March 5 freeze summary describing Appendices B, C, D. Neither recorded hash matches the exported text under any tested normalization, which is expected: a Google Doc has no fixed byte form, so it cannot be the artifact those hashes were computed over. The original `.txt` bundle was most likely produced on the owner's machine (`R:\substrate\governance\`).
   - Required: locate the ratified Articles I–VIII + B/C/D text (governance record also references `R:\substrate\governance\doctrine_record_v1.0.md`, which is on the owner's machine and not reachable from this session); seal it with canonical normalization (UTF-8, LF, as for the Core Four seals); verify by hashing the actual bytes at startup; fail closed.

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
2. Doctrine v1: locate the ratified Articles; seal with line-ending-independent normalization; verify by hashing actual bytes; fail closed.
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

## 6. Decisions applied (GPT Turn 58, owner-accepted)

| # | Decision | Effect |
|---|---|---|
| 1 | One canonical Core Four v2; Orbot's admission tribunal becomes an evaluation context, not a competing definition | Authority rank moves to the controller; confidence floors become policy thresholds |
| 2 | MCP R-Substrate becomes a cognition/tool adapter | Tool capabilities kept; duplicate decision authority removed after compatibility tests |
| 3 | Orbot's TPC is the integration baseline | All 20 differing files compared against the golden template; Website ORB capabilities preserved |
| 4 | Locate and verify the ratified Doctrine; no substitute seal | See 2.3 item 2; governed execution path fails closed until resolved |
| 5 | Two enforcement layers in fixed order: Doctrine + controller authorization, then deployment-specific action gate | The deployment gate may narrow permissions, never expand them |

## 7. Compatibility tests required before enabling governed execution

1. Doctrine: startup hashes the canonical text and refuses to authorize on mismatch, missing file, or empty anchor; LF and CRLF checkouts produce the same verified result.
2. Core Four admission context: authority-rank denials originate from the controller and are recorded as authorization enforcement, not as a Kant verdict.
3. MCP adapter: every existing desktop tool workflow still succeeds through the control plane; no tool executes on an R-Substrate verdict alone.
4. TPC baseline: the golden template's answer tests (`tests/test_route_lookup.py`, `test_technique_skg.py`, `test_guiderails.py`, `test_pointer_index.py`, `test_field_maintenance.py`) pass against Orbot's TPC.
5. Gate order: a Doctrine denial cannot be overridden by the deployment gate; a deployment-gate denial (for example an unverified DOM target) holds an action Doctrine permits.
6. A.I.M.S. merged release: the existing suites from both lines pass, plus tests pinning retirement candidacy and relation-aware relevance.

## 8. Owner decisions required

1. **Doctrine source bytes:** supply the original `Doctrine_v1.0+B+C+D` text file from the machine that produced it (for example `R:\substrate\governance\`), so `b601457a…` and `27c7bfa7…` can be checked against real bytes. If that file cannot be found, decide whether to **re-seal**: ratify the Articles I–VIII (Google Doc " Doctrine v1.0") plus Appendices B, C, D as one canonical text, seal it with UTF-8 + LF normalization, and record the original hashes as historical and unverifiable. Re-sealing is the owner's decision; it is not done by default.
2. **Which recorded hash was meant to identify what:** `27c7bfa7…` is labelled "file bundle" and `b601457a…` "canonical" in `Orb_Assistant_Desktop_2026`; neither is reproducible from any file or document found.
