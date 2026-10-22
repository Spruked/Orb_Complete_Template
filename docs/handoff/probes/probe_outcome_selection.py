"""Does outcome feedback change WHICH evidence a bounded retrieval returns?"""
import sys, tempfile, hashlib, json
sys.path.insert(0, '/home/claude/aims')
from memory_core import AIMSMemorySystem

def snapshot(system, limit):
    r = system.retrieve('basic package price', mode='COLLECTIVE', limit=limit)
    ids = [x['atom_id'] for x in r['results']]
    return ids, r['retrieval_id']

with tempfile.TemporaryDirectory() as d:
    s = AIMSMemorySystem(d)
    # Five equally relevant price facts; two say the old price, three the new one.
    facts = ['basic package price is 488 (crawl 2026-08)', 'basic package price is 488 (crawl 2026-09)',
             'basic package price is 988 (verified scan)', 'basic package price is 988 (owner update)',
             'basic package price is 988 (checkout page)']
    atoms = [s.assert_apriori(f) for f in facts]
    s.indexes.rebuild(s.vault)
    before, rid = snapshot(s, limit=2)
    # Outcome feedback: visitors "found useful" the answers that quoted the OLD price (e.g. they bought).
    for _ in range(5):
        _, rid = snapshot(s, limit=5)
        s.record_retrieval_feedback(rid, useful_atom_ids=[atoms[0].atom_id, atoms[1].atom_id])
    after, _ = snapshot(s, limit=2)
    name = {a.atom_id: f for a, f in zip(atoms, facts)}
    print('top-2 evidence BEFORE outcome feedback:', [name[i] for i in before])
    print('top-2 evidence AFTER  outcome feedback:', [name[i] for i in after])
    h = lambda ids: hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest()[:12]
    print('snapshot membership hash before/after:', h(before), h(after), '-> CHANGED' if h(before) != h(after) else '-> same')
    s.close()
