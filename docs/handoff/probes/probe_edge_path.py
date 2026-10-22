"""With the 20% utility term ZEROED, does outcome feedback still change bounded evidence via SKG edge weights?"""
import sys, tempfile, hashlib, json
sys.path.insert(0, '/home/claude/aims')
from memory_core import AIMSMemorySystem
from memory_core.skg.types import Relation

with tempfile.TemporaryDirectory() as d:
    s = AIMSMemorySystem(d)
    s.retrieval_ledger.utilities = lambda: {}          # the proposed patch: 0% outcome utility in selection
    facts = ['basic package price is 488 (crawl 2026-08)', 'basic package price is 488 (crawl 2026-09)',
             'basic package price is 988 (verified scan)', 'basic package price is 988 (owner update)',
             'basic package price is 988 (checkout page)']
    from memory_core import EntryType
    src = s.commit(EntryType.OBSERVATION, {'observation': 'site crawl'})
    atoms = [s.derive_aposteriori(f, [src], initial_confidence=0.8) for f in facts]
    ctx = s.derive_aposteriori('pricing page context', [src], initial_confidence=0.8)
    for a in [*atoms, ctx]:                              # bring every fact to ACTIVE identically
        while s.vault.get(a.atom_id).status.value != 'active': s.vault.reinforce(a.atom_id, 0.05)
    for a in atoms:                                      # identical neutral edge for every fact
        s.link(a.atom_id, ctx.atom_id, Relation.CONTEXT_DEPENDENT, weight=0.5)
    s.indexes.rebuild(s.vault)
    snap = lambda n: s.retrieve('basic package price', mode='COLLECTIVE', limit=n)
    before = [x['atom_id'] for x in snap(2)['results']]
    for _ in range(5):
        rid = snap(5)['retrieval_id']
        s.record_retrieval_feedback(rid, useful_atom_ids=[atoms[0].atom_id, atoms[1].atom_id])
    res = snap(2)['results']; after = [x['atom_id'] for x in res]
    name = {a.atom_id: f for a, f in zip(atoms, facts)}
    print('utility term in score:', [x['retrieval_utility'] for x in res])
    print('skg_weight after:', {name[x['atom_id']]: round(x['skg_weight'], 3) for x in snap(5)['results']})
    print('BEFORE:', [name[i] for i in before]); print('AFTER: ', [name[i] for i in after])
    h = lambda ids: hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest()[:12]
    print('membership hash:', h(before), h(after), 'CHANGED' if h(before) != h(after) else 'same')
    s.close()
