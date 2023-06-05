from multiprocessing import Process
from tools import create_img_dir, get_urls  # , save_url, timeit
from time import time
import requests


def save_url(url):
    _start = time()
    response = requests.get(url)
    filename = f'{url.split("/")[-1]}'
    with open(f'img/{filename}', 'wb') as f:
        f.write(response.content)
    print(f'{url=}')
    print(f'Executed in {(time() - _start):.4f}s')


# @timeit
def url_save_processes():
    create_img_dir()
    processes = []
    urls = get_urls()
    for url in urls:
        process = Process(target=save_url, kwargs={'url': url})
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print('End all jobs')


if __name__ == '__main__':
    start = time()
    url_save_processes()
    print(f'Executed in {(time() - start):.4f}s')
