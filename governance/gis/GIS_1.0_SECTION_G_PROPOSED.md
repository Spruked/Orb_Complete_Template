# Governance Implementation Specification 1.0 — Section G (PROPOSED)

**Status:** Proposed by Claude and GPT for owner ruling. Not ratified, not sealed, not deployed.
**Authority:** Bryan A. Spruk, final constitutional authority.
**Scope:** Implements Doctrine v1.0 Articles III, V and VII against the locked Core Four v2 extensions and the locked review-record contract v0.2.
**Leaves unchanged:** Doctrine v1.0, the four Core Four extension files and their seals, and the review-record contract. Nothing in this section edits a sealed file.

---

## G.1 Joint positions submitted for ruling

| Item | Joint proposal | Remaining disagreement |
|---|---|---|
| Conflict 1: Art. III vs S-R05 | S-R05 reports promotion eligibility only. Its sealed `recommended_outcome: promote` is read as a recommendation the controller may authorize. A.I.M.S. records; nothing in S-R05 changes magnitude. Invariant 2. | None |
| Conflict 2: Art. VII vs outcome learning | Outcome signals have zero influence on constitutional evidence selection: candidate generation, scoring, filtering, deduplication, truncation, ordering and snapshot formation. Outcome signals stay in a separate operational channel. Invariant 1. | None. GPT's acceptance was conditional on reproducible verification, which §G.2 supplies. |
| Conflict 3: Art. IV/V vs unanimity | Two separate metrics. Track A is examination coverage (sealed challenge catalog, four statuses). Track B is the historical DDR, kept unchanged in form. Invariant 3. | Article V's meaning (§G.5) is yours to rule. |
| Conflict 4: decision mechanics | No averaging, voting or winner-take-all. The controller decides by named criteria. | None |
| Versioning | Preserve Doctrine v1.0. Publish GIS 1.0 as a separate implementing document. | None |

---

## G.2 Evidence-selection correction to A.I.M.S. (release blocker)

### G.2.1 Verified finding

The test is `governance/gis/tests/test_inv1_evidence_selection.py`, run against Spruked/AIMS @ `d72a3ce`. It is deterministic and reproduced on three consecutive runs.

The same vault, evidence and configuration are used throughout; only outcome feedback changes. The two lowest-ranked facts receive five rounds of "useful" feedback. Bounded retrieval is then compared at limits 1, 2, N−1 and N.

| A.I.M.S. variant | Path A: utility term | Path B: outcome-reinforced SKG edges |
|---|---|---|
| As shipped | FAIL at every limit | FAIL at every limit |
| Utility term zeroed only | pass | **FAIL at every limit** |
| Utility zeroed and graph weight outcome-blind | pass | pass |

There are **two** leak paths, so zeroing the utility weight alone is not a sufficient patch.

- **Path A.** `indexes.search` scores `0.20 × utility`, and the utility comes from `retrieval_ledger.utilities()`.
- **Path B.** `evaluate_cognitive_outcome` calls `skg.update_edges_from_outcome`, which strengthens every A Posteriori edge touching a "useful" atom (+0.1 weight per round). `relevance_weight` averages edge weights into `skg_weight`, which is 10% of the score. Rewarded facts rise across the truncation boundary.

### G.2.2 Required correction

1. **Constitutional retrieval uses no outcome-derived quantity.** Ranking keys are limited to semantic relevance, atom confidence, and outcome-blind graph weight. Ties break by a stable non-outcome key.
2. **Outcome-blind graph weight.** Edge weight used for selection is the weight established by declared relationships and evidence events. Outcome-driven strengthening and weakening moves to a separate operational edge attribute, which retrieval for review never reads.
3. **Operational channel kept.** Outcome learning may continue for operational events, such as which phrasing a visitor found clear. It is admissible only for that event and only after the decision (Conflict 2).
4. **Owner review for behavior change.** Any change in what the ORB says or does that is caused by the operational channel is surfaced for owner review before adoption.

### G.2.3 Interface consequence

`retrieve()` gains an explicit purpose: `constitutional` (outcome-blind; the only mode the Core Four may consume) or `operational`. The review record stores the purpose. A Core Four review over an `operational` snapshot is `INTEGRITY_FAILURE`.

---

## G.3 Release-gating invariant tests

### Invariant 1: Evidence-selection invariance (Article VII)

For fixed evidence and configuration, changing outcome signals changes neither:

- the canonical snapshot manifest (membership, provenance and order), nor
- the resulting Decision Envelope.

The test covers both leak paths and adversarial truncation limits. Today it is implemented for retrieval, and it fails as shown in §G.2.1. Extending it to the Decision Envelope waits on the controller.

### Invariant 2: Spinoza non-amplification (Article III, GPT correction adopted)

For every atom and every Spinoza evaluation, M_post ≤ M_pre, checked independently for each of:

- confidence,
- certainty, and
- scope.

The test also checks that an S-R05 finding carries no magnitude field. Spinoza may lower magnitude; it may never raise it. Only the controller, under A.I.M.S. thresholds, can authorize a promotion. This waits on the lens runtime.

### Invariant 3: Unexamined is never healthy (Article V)

These cases must hold:

- Any review whose applicable challenges were not all executed returns `UNEXAMINED`.
- Any review where expected tension under independence is 0 or undefined returns `UNEXAMINED`.
- `UNEXAMINED` never maps to a trusted or healthy state, and the controller may not promote it.

This waits on the controller.

---

## G.4 Tension calculus

### G.4.1 Track A: examination coverage (sealed challenge catalog)

`challenge_catalog.v0.1.proposed.json` is **generated** from the four sealed extensions by `build_challenge_catalog.py`, and the build fails if any seal does not verify. It contains:

- 18 challenges, one per sealed rule (L-R01…L-R04, H-R01…H-R05, K-R01…K-R04, S-R01…S-R05). Each rule's `applies_when` is copied verbatim and cites its file's seal.
- The six pairwise cross-examinations.

It adds no reasoning beyond what you already locked. Proposed catalog hash: `f35123c0d82f9654947b51c50d370cb3106d547d7ed50041ffbc1949cae7738d`.

**Deterministic applicability.** Each challenge gets a coded predicate over review-record fields, such as "subject is used as a current fact" → `subject.use == "current_fact"`. Every predicate gets a test case that applies and one that doesn't. A challenge judged inapplicable must record the predicate result that excluded it. A non-applicability with no recorded result counts as unexamined.

**Examination record (per applicable challenge):**

- `challenge_id`
- `executed` (bool)
- `finding`
- `objection_material` (bool)
- `resolution_evidence_ids`
- `resolved` (bool)
- `independence`: proof that no outcome signal and no Fifth Mind preference reached the lens. This is the snapshot purpose plus the manifest hash.

**Statuses:**

| Status | Condition |
|---|---|
| `STRESSED_PASS` | Every applicable challenge executed, and every material objection resolved with admissible evidence |
| `STRESSED_UNRESOLVED` | Examination complete, and at least one material objection open |
| `UNEXAMINED` | Any applicable challenge missing, any non-applicability unrecorded, or the evaluation incomplete |
| `INTEGRITY_FAILURE` | Independence broken, the snapshot not constitutional, disagreement manufactured, or evidence contaminated |

The controller maps each status to permitted actions. That mapping belongs to the controller contract, not this section, except that `UNEXAMINED` and `INTEGRITY_FAILURE` may never yield trusted or promoted outcomes.

### G.4.2 Track B: doctrine drift (historical DDR, form unchanged)

DDR = observed_tension / expected_tension_under_independence. It is computed across reviews, not per review.

- **Estimator.** Expected tension comes only from measured Phase 1 base rates per outcome type. Until those exist, Track B reports `baseline_not_established` and makes no claim of health.
- **Zero or undefined denominator.** Track B reports `undefined_baseline`, never healthy, and the affected reviews fall under Invariant 3.
- **Role.** Track B watches whether the four lenses lose independence over time. It never manufactures disagreement in a single review to raise a number.

---

## G.5 Remaining Article V question for your ruling

Article V says "low tension is failure." Track A introduces an **interpretive change**: a review with little disagreement that passed every applicable challenge (`STRESSED_PASS`) is not a failure. Choose one reading:

| Option | Reading | Consequence |
|---|---|---|
| **A. Literal** | Low observed disagreement is failure regardless of examination. | Well-supported facts fail. The system is pressured to manufacture disagreement, which Track A labels `INTEGRITY_FAILURE`. |
| **B. Pressure** | "Low tension" means low pressure *applied*. Low tension maps to `UNEXAMINED`, and consensus after full challenge is a pass. | Matches Track A. Stated in GIS as an explicit interpretation of Article V; Doctrine text untouched. |
| **C. Both tracks** | B for each single review, and Article V's literal sense applied to the *pattern*. Sustained low DDR across reviews (Track B) is a doctrine failure that triggers an owner review of lens independence. | Keeps both meanings without forcing disagreement into individual answers. |

Claude recommends **C**. GPT's position is that the change must be named explicitly whichever option is chosen, and this section names it.

---

## G.6 Open dependencies

- The controller contract (status → permitted actions; Decision Envelope) must exist before Invariants 1 (envelope half), 2 and 3 can run.
- Applicability predicates need binding in code, with tests.
- The phase 1 measurement plan for Track B base rates is still to be written.
- The A.I.M.S. merge release must include the §G.2 correction. This joins the existing blockers: retirement candidacy, relation-aware relevance, one session design, and single writer.
