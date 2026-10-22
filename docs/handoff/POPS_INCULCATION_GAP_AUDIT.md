# POPS Website ORB — Inculcation Contract Gap Audit

**Audited:** `Spruked/POPS_website`, branch `dev/pops-demo-launch-20261022`, commit `29e364e` (2026-10-22 03:28).
**Against:** `INCULCATION_CONTRACT.md` (six-stage sequence).
**Mode:** Read-only. No repository files were changed.

**Files examined:** `backend/orb_harness.py`, `backend/website_orb_host.py`, `backend/test_orb_harness.py`, `data/orb-context/website.json`, `scripts/generate-orb-context.mjs`, `src/services/orbApi.ts`, `src/pops-demo-app/tour/*`, `docs/launch/MEMORY_INTEGRATION.md`, `src/pops-demo-app/README.md`.

**Baseline:** The existing 11 harness tests pass (`python -m unittest backend.test_orb_harness`).

## Verdict

The runtime safety layer is strong and should be kept. The education layer the contract requires is mostly missing. Today the ORB receives one 615-character role string plus per-turn data, assembled into a single JSON system message. There is no Core Four, no Professional Inculcation, and no stable prefix. That is the "generic system prompt" the contract prohibits.

## Stage-by-stage

| Stage | Status | Finding |
|---|---|---|
| 1. Core Four | **Missing** | No Core Four content or loader anywhere in the repo. |
| 2. Professional Inculcation (A Priori) | **Missing** | `inculcation.md` v1.0 is not in the repo. The only identity text is the `role` string in `orb_harness.py` (615 chars). It contains some correct rules (untrusted input, allowlisted actions only, no legal claims) but no profession, mission, methods, consultation practice or Example Language Library. |
| 3. Site Seed | **Partial** | `data/orb-context/website.json` is generated from the public build (32 pages, registered targets) and hash-tracked into A.I.M.S. with retirement of superseded copy. Correct source discipline. But it is raw page text, not a structured seed (business identity, products, terminology, pricing, policies, routes), and only 2 retrieved excerpts of ≤450 chars reach the model per turn. |
| 4. Current Context / Acquired | **Present** | Per-visitor A.I.M.S. `ShortTermMemory`, route, screen, revision, recent and relevant earlier turns. No raw visitor text reaches durable ledgers (tested). |
| 5. TPC | **Absent, by design** | Explicitly deferred; the capabilities endpoint and docs say so. Consistent with the contract: inculcation does not depend on TPC. |
| 6. Articulation and Execution | **Present, strong** | Strict JSON-schema output, server-side `validate_action` allowlist, adjacent-only tour transitions, stale-revision discard, client-side `admitDemoCommand`. The LLM proposes; code decides. |

## Specific gaps

### G1. No inculcation layer (Stages 1–2)
The ORB is not educated for its profession. Everything the contract lists under Professional Inculcation Contents is absent except a few boundary rules.

### G2. No stable prefix; nothing cacheable
`answer()` builds one JSON object that mixes the role string with volatile fields (`current_page`, `event`, `visited_pages`, `published_context`, `fictional_case`). Every turn is a full rebuild. The contract requires Stages 1–3 as a stable, cacheable prefix and Stage 4 updated per turn.

### G3. Demo facts survive exit through conversation history (confirmed by test)
The demo package is correctly scoped: `fictional_case` is sent only while `demo_active` is true and is never written to the durable Vault. But on exit, prior demo turns stay in session history and are sent to the model.

Reproduced with a mocked model: start demo → ask about the incident → model answers "Alex Morgan recorded the October 10 exchange attempt with Jamie Morgan" → exit demo → go to `/` → ask "Tell me about POPS". The post-exit request still carries that assistant turn in `history`. This violates "no fictional fact may appear in a later non-demo answer."

### G4. Spoken output is not reconciled with the executed action (`FALSE_TOOL_NARRATION` exposure)
When `validate_action` or the revision check downgrades a proposed action to `stay`, `spoken_output` is returned unchanged. The ORB can say "I've opened the timeline for you" while nothing happened. There is no hard checksum between narration and the action actually admitted.

### G5. Response contract field name differs
The contract and `inculcation.md` name the field `requested_tool`. This implementation uses `action`. Not renamed in this audit; needs your decision (see D3).

### G6. Demo fixtures share the seed file
The demo package is stored under the `demo` key inside `website.json`, and its vocabulary feeds `public_terms`. It is not asserted into the Vault, so this is a physical-layout issue rather than a contamination path, but it blurs the seed / demo boundary the contract draws.

### G7. No Part V evaluation harness
The 11 existing tests are security and boundary tests. There is no versioned case suite, no failure labels, no semantic review, no per-model runs and no release gate. The Playwright suites record real model replies but do not grade them.

### G8. Conversational rule not represented
Only "respond naturally, briefly" and tour behavior. No rapport/objective rule (pending your ruling anyway).

## Keep as-is

Origin/CSRF/session isolation, private-route and private-text exclusion, loopback-only inference, action allowlists on server and client, adjacent-only tour progression, stale-action discard, ephemeral visitor memory, hash-tracked public copy, and the labeled offline narration fallback.

## Decisions needed from you before any code

- **D1. A Priori source.** Is POPS's A Priori layer the Website ORB `inculcation.md` v1.0 as-is (same occupation), or does POPS need its own adaptation? The current role string calls the ORB "Pops, the local-development website guide."
- **D2. Seed classification in A.I.M.S.** Site copy is currently stored with `assert_apriori`. The contract reserves "A Priori" for the professional inculcation and treats seed as Stage 3. Keep seed in the A.I.M.S. a priori partition (initial knowledge), or separate it?
- **D3. `action` vs `requested_tool`.** Which name is canonical?
- **D4. Demo history on exit.** The contract says both "retain previous visitor context" and "no fictional fact after exit." Options: (a) drop demo-tagged turns from post-exit history; (b) keep them but mark them as fictional so the model may reference them only as "the demo." Your call.
- **D5. Small-talk ruling and release pass threshold** (still open from the contract).

## Proposed order once decided

1. Add Core Four and the A Priori inculcation to the repo and assemble Stages 1–3 as a stable system prefix; move Stage 4 into a separate per-turn message (G1, G2).
2. Apply the D4 rule for demo history (G3), with a test reproducing the leak above.
3. Reconcile narration with the admitted action before speech (G4).
4. Build the Part V suite (G7).

No changes to the A.I.M.S./Vault implementations are required by any of these.
