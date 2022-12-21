from asyncio import get_event_loop

from service.parser.main import all_armani_tasks


async def all_tasks():
    tasks = []
    tasks.extend(await all_armani_tasks())
    for task in tasks:
        res = await task.start()
        print(res)


def parser_event_loop():
    loop = get_event_loop()
    loop.run_until_complete(all_tasks())