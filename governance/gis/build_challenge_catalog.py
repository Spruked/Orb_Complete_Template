"""Generate the GIS 1.0 challenge catalog from the sealed Core Four v2 extensions.

The catalog adds no new reasoning. Each sealed rule becomes one challenge; its
`applies_when` (or `contexts`) is copied verbatim. Every entry cites the seal of
the file it came from, and the build fails if any extension's seal does not verify.
"""
import hashlib, itertools, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "Orb_Vault_Template" / "master_seed_vault"
LENSES = ["locke", "hume", "kant", "spinoza"]

def canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def verified(path):
    ext = json.loads(path.read_text(encoding="utf-8"))
    seal = ext.pop("seal")["sha256"]
    if hashlib.sha256(canon(ext)).hexdigest() != seal:
        sys.exit(f"SEAL MISMATCH: {path.name}")
    return ext, seal

challenges = []
for lens in LENSES:
    ext, seal = verified(VAULT / f"seed_{lens}.extension.v2.json")
    for rule in ext["rules"]:
        challenges.append({
            "challenge_id": rule["rule_id"],
            "lens": lens,
            "name": rule["name"],
            "applies_when": rule.get("applies_when") or {"contexts": sorted(rule.get("contexts", {}))},
            "context_restriction": rule.get("context"),
            "material_objection": bool(rule.get("material_objection", False)),
            "may_raise_conflict_types": rule.get("may_raise_conflict_types", []),
            "source": {"file": f"seed_{lens}.extension.v2.json", "extension_seal": seal},
            "applicability_predicate": None,   # bound in code; see GIS 1.0 §G.3.2
        })

catalog = {
    "catalog_id": "gis-1.0-core4-challenge-catalog",
    "version": "0.1.0-proposed",
    "status": "PROPOSED — not ratified; requires owner approval before sealing",
    "derived_from": "Core Four v2 extensions (sealed, owner locked 2026-10-22)",
    "challenges": challenges,
    "pairwise_cross_examinations": [list(p) for p in itertools.combinations(LENSES, 2)],
}
catalog["catalog_hash"] = hashlib.sha256(canon(catalog)).hexdigest()
out = Path(__file__).with_name("challenge_catalog.v0.1.proposed.json")
out.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(challenges)} challenges, 6 pairwise, catalog_hash {catalog['catalog_hash']}")
