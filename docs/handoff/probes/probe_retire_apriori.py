import sys, tempfile, copy
from pathlib import Path
sys.path.insert(0, '/home/claude/spruked/pops_website')
from backend.orb_harness import WebsiteHarness
tmp = tempfile.TemporaryDirectory(); store = Path(tmp.name)
h = WebsiteHarness(store)
route = h.catalog['pages'][0]['route']
h.public.close()
cat = copy.deepcopy(h.catalog)
cat['pages'][0]['text'] = 'CHANGED PAGE COPY ' + cat['pages'][0]['text'][:200]
cat['pages'][0]['sha256'] = 'changed-hash'
h2 = WebsiteHarness(store, catalog=cat)
atoms = [a for a in h2.public.vault.all_atoms() if a.metadata.get('route') == route]
old = [a for a in atoms if a.metadata.get('source_hash') != 'changed-hash']
print('superseded atoms for', route, ':', len(old))
print('their statuses:', sorted({a.status.value for a in old}), '| vault types:', sorted({a.vault_type.value for a in old}))
h2.public.close(); tmp.cleanup()
