import asyncio, json, tempfile, sys
from pathlib import Path
import httpx
sys.path.insert(0, '/home/claude/spruked/pops_website')
from backend.orb_harness import WebsiteHarness

async def main():
    tmp = tempfile.TemporaryDirectory()
    h = WebsiteHarness(Path(tmp.name))
    sent = []
    replies = iter([
        'Alex Morgan recorded the October 10 exchange attempt with Jamie Morgan.',
        'POPS is Windows software for organizing records.',
    ])
    def respond(req):
        if req.url.path == '/v1/models':
            return httpx.Response(200, json={'data': [{'id': 'm'}]})
        sent.append(json.loads(req.content))
        return httpx.Response(200, json={'choices': [{'message': {'content': json.dumps({'spoken_output': next(replies), 'action': {'type': 'stay'}})}}]})
    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as c:
        _, v, _ = h.visitor(None)
        h.event(v, 'start_demo', '/product-demo', 'incident')
        await h.answer(v, 'Who is in this incident?', client=c)
        h.event(v, 'exit_demo', '/product-demo')
        h.event(v, 'page', '/')
        await h.answer(v, 'Tell me about POPS', client=c)
    last = sent[-1]
    system = json.loads(last['messages'][0]['content'])
    history = last['messages'][1:-1]
    print('demo_active after exit:', system['demo_active'])
    print('fictional_case in system after exit:', system['fictional_case'] is not None)
    print('history entries after exit:', len(history))
    leaked = [m for m in history if 'Morgan' in m['content']]
    print('fictional facts in post-exit history:', len(leaked))
    for m in leaked: print('  ', m['role'], '->', m['content'][:90])
    print('system prompt chars (whole instruction object):', len(last['messages'][0]['content']))
    print('role/identity string chars:', len(system['role']))
    h.public.close(); tmp.cleanup()
asyncio.run(main())
