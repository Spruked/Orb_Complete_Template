"""GIS 1.0 Invariant 1 — Evidence-selection invariance (Doctrine Article VII).

Constitutional evidence selection must not change when outcome-performance
signals change, with the underlying evidence and configuration held constant.

Run against an A.I.M.S. checkout:
    AIMS_PATH=/path/to/AIMS python -m unittest governance.gis.tests.test_inv1_evidence_selection

Status against Spruked/AIMS @ d72a3ce: both leak paths FAIL (expected until the
GIS §G.2 retrieval correction lands). These tests gate the merged A.I.M.S. release.
"""
import hashlib, json, os, sys, tempfile, unittest

AIMS_PATH = os.environ.get("AIMS_PATH")
if AIMS_PATH:
    sys.path.insert(0, AIMS_PATH)

FACTS = [
    "basic package price is 488 (crawl 2026-08)",
    "basic package price is 488 (crawl 2026-09)",
    "basic package price is 988 (verified scan)",
    "basic package price is 988 (owner update)",
    "basic package price is 988 (checkout page)",
]
QUERY = "basic package price"
FEEDBACK_ROUNDS = 5


def manifest_hash(results):
    """Membership and order of the bounded evidence set.

    Each run builds a fresh vault, so atom ids differ between runs; the test
    compares by statement. A production manifest also binds atom ids and
    provenance (review-record contract, snapshot manifest hash).
    """
    rows = [r["statement"] for r in results]
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


@unittest.skipUnless(AIMS_PATH, "set AIMS_PATH to an A.I.M.S. checkout")
class EvidenceSelectionInvariance(unittest.TestCase):

    def _build(self, directory, posterior):
        from memory_core import AIMSMemorySystem, EntryType
        from memory_core.skg.types import Relation
        s = AIMSMemorySystem(directory)
        if posterior:
            src = s.commit(EntryType.OBSERVATION, {"observation": "site crawl"})
            atoms = [s.derive_aposteriori(f, [src], initial_confidence=0.8) for f in FACTS]
            ctx = s.derive_aposteriori("pricing page context", [src], initial_confidence=0.8)
            for a in [*atoms, ctx]:
                while s.vault.get(a.atom_id).status.value != "active":
                    s.vault.reinforce(a.atom_id, 0.05)
            for a in atoms:
                s.link(a.atom_id, ctx.atom_id, Relation.CONTEXT_DEPENDENT, weight=0.5)
        else:
            atoms = [s.assert_apriori(f) for f in FACTS]
        s.indexes.rebuild(s.vault)
        return s, atoms

    LIMITS = (1, 2, len(FACTS) - 1, len(FACTS))   # adversarial bounds included

    def _assert_invariant(self, posterior):
        # Same vault, same evidence, same configuration: only outcome signals change.
        with tempfile.TemporaryDirectory() as d:
            s, atoms = self._build(d, posterior)
            snap = lambda n: manifest_hash(s.retrieve(QUERY, mode="COLLECTIVE", limit=n)["results"])
            before = {n: snap(n) for n in self.LIMITS}
            # Adversarial: reward the two facts currently ranked LAST, so any outcome
            # influence on ranking must move them across a truncation boundary.
            ranked = [r["atom_id"] for r in s.retrieve(QUERY, mode="COLLECTIVE", limit=len(FACTS))["results"]]
            rewarded = ranked[-2:]
            for _ in range(FEEDBACK_ROUNDS):
                rid = s.retrieve(QUERY, mode="COLLECTIVE", limit=len(FACTS))["retrieval_id"]
                s.record_retrieval_feedback(rid, useful_atom_ids=rewarded)
            after = {n: snap(n) for n in self.LIMITS}
            s.close()
        for n in self.LIMITS:
            with self.subTest(limit=n):
                self.assertEqual(before[n], after[n])

    def test_path_a_retrieval_utility(self):
        """Leak A: the 20% outcome-utility term in relevance_score."""
        self._assert_invariant(posterior=False)

    def test_path_b_outcome_reinforced_skg_edges(self):
        """Leak B: outcome feedback strengthens A Posteriori SKG edges, which feed skg_weight (10%)."""
        self._assert_invariant(posterior=True)


if __name__ == "__main__":
    unittest.main()
