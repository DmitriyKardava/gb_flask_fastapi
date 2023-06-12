import asyncio
import aiohttp
from time import time
from tools import get_urls, create_img_dir, timeit


async def aio_save_url(url):
    _start = time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            cont = await response.read()
            filename = f'{url.split("/")[-1]}'
            with open(f'img/{filename}', 'wb') as f:
                f.write(cont)
                print(f'Saving {filename}')
    print(f'Executed in {(time() - _start):.4f}s')


async def main():
    tasks = []
    urls = get_urls()
    for url in urls:
        task = asyncio.ensure_future(aio_save_url(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


@timeit
def aio_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print('End all jobs')


if __name__ == '__main__':
    create_img_dir()
    aio_loop()