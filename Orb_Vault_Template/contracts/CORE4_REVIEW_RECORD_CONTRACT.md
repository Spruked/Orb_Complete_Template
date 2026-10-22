# Core Four Review-Record Contract

**Status:** v0.2, OWNER APPROVED AND LOCKED by Bryan A. Spruk, 2026-10-22.
**v0.2 changes:** evaluation time as a replay input; retrieval eligibility separated from lifecycle; holds always produce an evidence request and re-review trigger; time-based revalidation and periodic reconciliation; conflict registry generated from the sealed extensions.
**Owner:** Bryan A. Spruk. **Drafted by:** Claude and GPT.
**Depends on (locked, published in `Spruked/Vault_System_1.0` at commit `428c1c4`):**

| Extension | Seal (sha256) |
|---|---|
| `seed_locke.extension.v2.json` | `badef79b5526b38d07748fa7af8124a499ad58d32bfa1beac4e698be85525555` |
| `seed_hume.extension.v2.json` | `07a60a41bc5fa7e1acf5c934035abfe764025948ece89d3c3e04f2a0766266d1` |
| `seed_kant.extension.v2.json` | `19b340e7e496dd475fcb0689c821b97454d8429e227f7f32045a530131f4fd76` |
| `seed_spinoza.extension.v2.json` | `e322fcb6ce6dd2b70387c7afa6059793cfd130b74bfe448aba4a74e18030c900` |

---

## 1. Purpose

One review record captures one complete Core Four deep review of one subject: what evidence was examined, what each lens found, how the lenses compared, what the Fifth Mind advised, what the controller decided, and what A.I.M.S. actually did. It is the audit trail that lets anyone read why the ORB's knowledge changed, and replay the decision.

This contract governs **deep reviews** (triggered). The per-turn fast check produces no durable record.

## 2. Acceptance criteria

1. No Fifth Mind recommendation can directly execute an action.
2. An unresolved philosophical conflict remains unresolved in the final record.
3. No philosopher receives permanent preferential weight.
4. Full examinations run on material triggers, not on every turn.
5. Both over-holding and unsafe progression count as evaluation failures.
6. Missing structured evidence is reported as missing coverage, never treated as proof of safety.
7. Every executed memory change cites its `review_id`; the review cites the `rule_id`s and evidence that produced it.
8. Replaying the same snapshot, atom state, recorded lens findings, seed seals, controller version, policy configuration, and **evaluation time** reproduces the same controller decision: `decision = F(snapshot, atom_state, findings, controller_version, policy_config, evaluation_time)`. Recovery against current state is a separate operation with fresh validation; an interrupted retirement is revalidated, never finished blindly, and idempotency prevents duplicate lifecycle changes. Replay covers the controller's evaluation of the **recorded** verdicts, cross-examinations, and synthesis; it does not regenerate LLM language or embeddings, so those records are stored in full.

## 3. Authority boundaries

| Component | Produces | Authority |
|---|---|---|
| Each lens | Findings, aspect dispositions, a `recommended_outcome` | None |
| Cross-examinations | Agreement structure, disputed evidence, unresolved objections | None |
| Fifth Mind | Advisory synthesis, holds, minority objections | None (advisory only) |
| Deterministic controller | The decision and its rationale | Decides lifecycle outcome |
| A.I.M.S. | Lifecycle events | Executes and records |

**Operational precedence is not philosophical precedence.** The controller may give different consequences to different findings (for example, `consent_missing` blocks execution). When it does, the record states that it enforced an authorization requirement; it does not rank one lens over another.

## 4. Triggers

A deep review starts on any of:

1. Retirement candidacy (confidence below the A.I.M.S. prune floor, nominated rather than auto-retired)
2. Promotion to Active
3. A new contradiction edge
4. A subject touching price, policy, terms, or actions
5. Conflicting source authority
6. Material provenance change
7. Cross-bank knowledge transfer
8. Repeated failed outcomes for previously reinforced knowledge
9. **Time-based revalidation:** a time-sensitive fact (price, hours, policy, terms) passes its re-verification window, or a policy reaches its effective or expiry date. This fires without any new evidence or graph change.
10. **Incremental maintenance:** the atom, or a fact connected to it (its `derived_from` chain, or anything that supersedes or contradicts it), changed since its last review, or new evidence touching its `scope_identity` entered the store. Unchanged atoms are not re-reviewed.
11. **Periodic reconciliation (bounded):** a sweep for missed events, stale indexes, interrupted executions, and open evidence requests. It detects; it does not re-run every review.

A trigger means "examine," never "something is wrong."

Note: A.I.M.S. Vault atoms have no time-based confidence decay (only session memory decays). Age alone never changes an atom's state, which is why trigger 9 exists.

## 5. Record structure

Stored as a single A.I.M.S. event named `skg.core_four_review`, written through `vault.record_skg_event()` so it is hash-chained, glyph-verified, and restored on replay.

```json
{
  "review_schema_version": "1.0",
  "review_id": "rev-<uuid>",
  "created": "<tri-timestamp>",
  "trigger": "retirement_candidate",

  "versions": {
    "seed_seals": {
      "locke": "badef79b…", "hume": "07a60a41…",
      "kant": "19b340e7…", "spinoza": "e322fcb6…"
    },
    "controller_version": "controller@<sha256>",
    "registry_version": "conflicts@<sha256 of registry>",
    "fifth_mind_version": "fm@<sha256>",
    "canonicalization": "json-sorted-keys-utf8-compact-v1"
  },

  "subject": {
    "atom_id": "atom-…",
    "vault_type": "a_posteriori",
    "scope_identity": {"subject": "…", "scope": "…", "applicable_time": "…"},
    "atom_state_hash": "<sha256 of canonical atom.to_dict()>"
  },

  "snapshot": {
    "manifest_hash": "<sha256 of canonical manifest>",
    "manifest": [
      {
        "ref": "atom-…", "kind": "atom|ltm_entry|edge|tool_event|consent_record",
        "content_hash": "<sha256>",
        "source_class": "verified_tool_outcome|site_crawl|visitor_statement|system_observation|model_hypothesis",
        "verification_status": "verified|unverified|disputed",
        "relation_state": {"relation": "supersedes", "edge_state": "active"}
      }
    ]
  },

  "verdicts": [
    {
      "lens": "locke",
      "seed_seal": "badef79b…",
      "snapshot_hash": "<must equal snapshot.manifest_hash>",
      "aspects": [
        {"aspect": "supersession", "rule_id": "L-R03",
         "disposition": "affirmed|conflicted|unresolved|unevaluated",
         "conflict_types": [], "cited_refs": ["atom-…"],
         "material_objection": false, "reason": "…"}
      ],
      "coverage": "full|partial|none",
      "unresolved_questions": ["…"],
      "recommended_outcome": "retain|challenge|consolidate|retire|promote"
    }
  ],

  "cross_examinations": [
    {
      "pair": ["locke", "kant"],
      "agreement": "agree|partial|disagree",
      "shared_refs": ["…"], "disputed_refs": ["…"],
      "rules_compared": ["L-R03", "K-R03"],
      "unresolved_objections": [{"lens": "locke", "rule_id": "L-R02", "conflict_type": "self_corroboration", "ref": "…"}],
      "evidence_requests": ["…"],
      "explanation": "…"
    }
  ],

  "fifth_mind": {
    "method": "uniform",
    "advisory_relevance": {"locke": 0.25, "hume": 0.25, "kant": 0.25, "spinoza": 0.25},
    "recommended_outcome": "retire",
    "holds": [],
    "minority_objections": [],
    "unresolved_carried_forward": ["…"],
    "learning_value": "low|medium|high"
  },

  "decision": {
    "outcome": "retain|challenge|consolidate|retire|promote",
    "criteria_applied": ["C-…"],
    "authorization_enforcements": [],
    "rationale": "…",
    "evaluation_time": "<tri-timestamp; frozen for replay>",
    "policy_config_hash": "<sha256 of applicable configuration, incl. re-verification windows>",
    "expected_atom_state_hash": "<sha256 at decision time>",
    "current_fact_eligibility": "eligible|disputed|excluded",
    "evidence_requests": [{"request_id": "req-…", "needs": "…", "rereview_on": "new evidence in scope_identity"}]
  },

  "execution": {
    "state": "pending|applied|superseded|flagged",
    "aims_event_ids": []
  }
}
```

## 6. Field rules

### 6.1 Snapshot
- The manifest lists every item any lens may cite. Each item carries `content_hash`, `source_class`, `verification_status`, and relevant relation state.
- `manifest_hash` = sha256 over the canonical serialization of the manifest sorted by `ref`.
- Every verdict's `snapshot_hash` must equal `manifest_hash`. A mismatch invalidates the review.
- Cross-examinations operate only on this snapshot. If more evidence is needed, they record an `evidence_request`; a later review uses the expanded snapshot.

### 6.2 Aspect dispositions
| Disposition | Meaning |
|---|---|
| `affirmed` | The rule was examined and its **positive** conditions were satisfied. A failed conflict condition alone is not affirmation. |
| `conflicted` | The rule was examined and a defined conflict was established. |
| `unresolved` | The rule was examined but the evidence could not establish either result. |
| `unevaluated` | No examination occurred. Recorded under coverage; never counted as approval or objection. |

This distinction must survive serialization, retrieval, and Fifth Mind synthesis.

### 6.3 Source class
Every cited item carries `source_class`. A `model_hypothesis` can inform a hold or lead to further review, but never by itself supports retirement, promotion, or corroboration (Locke L-R02).

### 6.4 Conflict registry
Closed, versioned registry. **Generated from the four sealed extensions, not written by hand:** 17 types, each raised only by the named rules below. Any change requires a new extension version.

| Conflict type | Raised by |
|---|---|
| `causal_overreach` | H-R01 |
| `consent_missing` | L-R04 |
| `contradicted_by_verified` | K-R03 |
| `inadequate_for_stakes` | S-R03 |
| `internal_inconsistency` | S-R02 |
| `is_ought_conflation` | H-R02 |
| `overstated_certainty` | H-R04 |
| `person_as_means` | K-R02 |
| `self_corroboration` | L-R02 |
| `superseded` | L-R03 |
| `unaddressed_distress` | H-R05 |
| `unfounded_pressure` | S-R04 |
| `uninformed_choice` | K-R04 |
| `universalizability_failure` | K-R01 |
| `unsupported_provenance` | L-R01, K-R03 |
| `unwarranted_generalization` | H-R03 |
| `whole_system_harm` | S-R01 |

`registry_version` is recorded in each review alongside the seed seals.

### 6.5 Fifth Mind
- Starts with **uniform** relevance (0.25 each). Evidence-property relevance is permitted only after tests show it improves outcomes without suppressing minority objections; `method` records which is in use.
- Relevance is never a probability of truth.
- Preserves every unresolved question and minority objection; may recommend a hold; never resolves a question the rules left open.

### 6.6 Controller decision
- Deterministic code, versioned by `controller_version`.
- Applies named criteria (`criteria_applied`). Baseline criterion (pending owner approval): **an unresolved, material evidentiary objection holds retirement.**
- **Every hold records at least one `evidence_request`** naming the missing evidence, the affected atom, its scope, and the originating `review_id`, and registers a re-review trigger for new evidence in that scope. The status stays unresolved until the objection is resolved or formally dispositioned. **Request identity is stable:** re-reviewing an unchanged objection updates the existing request through recorded events; it never creates a duplicate.
- **Lifecycle, retrieval, and review status are separate.** Holding retirement preserves the atom in A.I.M.S.; `current_fact_eligibility` independently decides whether it may be served as a current fact (`disputed` facts are served only with their dispute stated; `excluded` facts are not served as current). Review status is carried by the open evidence requests.
- The decision is a function of recorded inputs and `evaluation_time`; the controller never reads the wall clock during replay.
- `authorization_enforcements` lists any requirement enforced regardless of other findings (for example `consent_missing`).
- Records `expected_atom_state_hash` for reconciliation.

### 6.7 Freshness (separate from confidence)
Three independent properties of a fact; none is derived from another:

| Property | Meaning | Changed by |
|---|---|---|
| Confidence | How strongly evidence established it | reinforce / challenge |
| Freshness | How recently it was verified | `last_verified_at`, reset **only** by a verified source event (repeating the claim or retrieving it does not reset it) |
| Historical value | What it records about an earlier time | never lost; preserved by the ledger |

A stale fact keeps its confidence. When it passes its window it becomes **due for verification**: it is served only qualified ("as of {last_verified_at}") until re-verified. Age alone never retires or challenges it.

**Approved windows (configurable freshness thresholds, not retirement deadlines):**

| Fact category | Window |
|---|---|
| Prices | 24 hours |
| Business hours | 24 hours |
| Policies | 7 days |
| Terms and conditions | 7 days |

Consequential transaction terms are verified against the authoritative source at the moment of commitment, regardless of earlier verification.

Not set by this lock: a window for stable product specifications (proposed 30 days), and how re-verification is performed (scheduled local re-check vs. owner-triggered scan). Both are recorded as open in section 11.

### 6.8 Canonical hashing
- `canonicalization: json-sorted-keys-utf8-compact-v1`: keys sorted, UTF-8, separators `,` and `:`, fixed timestamp and numeric representation, versioned.
- `atom_state_hash` = sha256 of the canonical `atom.to_dict()`. A.I.M.S. atom schema is unchanged.

## 7. Execution and reconciliation

The review event records **what was decided**. The A.I.M.S. lifecycle event records **what happened** (for retirement, `vault.retired` with reason `core_four_review:<review_id>`). A later `skg.core_four_reconciliation` event closes any gap; historical events are never edited.

| Ledger state | Controller behavior |
|---|---|
| Decision is retain or challenge | Nothing further to execute |
| Decision is retire; matching retirement exists | Mark applied |
| Decision is retire; retirement missing | Compare current `atom_state_hash` with `expected_atom_state_hash`. Equal: execute once. Different: mark `superseded` and re-review |
| Retirement exists with no matching review | Flag for audit |
| Conflicting reviews for one atom | Resolve by schema version and snapshot ordering before any execution |

Single-writer constraint: reviews may be computed anywhere, but every memory commit passes through the one serialized A.I.M.S. writer and compares `expected_atom_state_hash` before writing. This holds until the documented cross-process writer-lock failure is resolved.

## 8. Out of scope for this contract

- Deterministic predicates for the 18 rules (rule-engine contract).
- Live-turn responses `hold` and `qualify` (rule-engine contract; they are not lifecycle outcomes).
- A.I.M.S. changes (candidacy, relation-aware relevance, seed as A Posteriori, session history references), each test-first and separately authorized.
- Part V evaluation taxonomy.

## 9. First acceptance tests

1. Replay at a frozen `evaluation_time` reproduces the decision.
2. A time-sensitive fact expires with no graph change and triggers revalidation.
3. Interrupted retirement: equal state hash executes once; changed hash is marked superseded and re-reviewed.
4. An unresolved material objection holds retirement and records an evidence request.
5. A disputed current fact is served only with its dispute stated, or excluded, per `current_fact_eligibility`.
6. `affirmed` is recorded only when a rule's positive conditions are met.

## 10. Owner decisions (approved 2026-10-22)

1. **Hold rule:** an unresolved, material evidentiary objection holds retirement, generates a deduplicated `evidence_request`, and registers a re-review trigger. Current-fact eligibility is controlled independently.
2. **Maintenance:** incremental reviews, time-based revalidation, and bounded periodic reconciliation. No time-based confidence decay is introduced into A.I.M.S.
3. **Re-verification windows:** prices 24 hours, business hours 24 hours, policies 7 days, terms and conditions 7 days.

## 11. Open, outside this lock

1. Window for stable product specifications (proposed: 30 days).
2. Re-verification mechanism: (a) scheduled local re-check inside the ORB, no contact with Orb Weaver; or (b) owner-triggered scan only, with prices spoken "as of {last update}" once the window passes. Decided in the rule-engine and controller contract.
