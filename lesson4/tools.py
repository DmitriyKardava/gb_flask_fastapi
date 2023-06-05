import argparse
import requests
from time import time
import os

test_urls = [
    'https://www.kasandbox.org/programming-images/avatars/spunky-sam.png',
    'https://www.kasandbox.org/programming-images/avatars/spunky-sam-green.png',
    'https://www.kasandbox.org/programming-images/avatars/purple-pi.png',
    'https://www.kasandbox.org/programming-images/avatars/purple-pi-teal.png',
    'https://www.kasandbox.org/programming-images/avatars/purple-pi-pink.png',
    'https://www.kasandbox.org/programming-images/avatars/primosaur-ultimate.png',
    'https://www.kasandbox.org/programming-images/avatars/primosaur-tree.png',
    'https://www.kasandbox.org/programming-images/avatars/primosaur-sapling.png',
    'https://www.kasandbox.org/programming-images/avatars/orange-juice-squid.png',
    'https://www.kasandbox.org/programming-images/avatars/duskpin-sapling.png',
]


def timeit(func):
    def wrap_func(*args, **kwargs):
        _start = time()
        url = kwargs.get('url')
        result = func(*args, **kwargs)
        if url:
            print(f'{url=}')
        print(f'Executed in {(time() - _start):.4f}s')
        return result
    return wrap_func


def create_img_dir():
    if not os.path.exists('img'):
        os.makedirs('img')


def get_urls():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', nargs="*")
    urls = parser.parse_args().urls
    if not urls:
        urls = test_urls
    return urls


@timeit
def save_url(url):
    response = requests.get(url)
    filename = f'{url.split("/")[-1]}'
    with open(f'img/{filename}', 'wb') as f:
        f.write(response.content)
