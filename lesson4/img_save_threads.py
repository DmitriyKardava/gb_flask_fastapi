from threading import Thread
from tools import get_urls, save_url, create_img_dir, timeit


@timeit
def url_save_threads():
    create_img_dir()
    urls = get_urls()
    threads = []
    for url in urls:
        thread = Thread(target=save_url, kwargs={'url': url, })
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print('End all jobs')


if __name__ == "__main__":
    url_save_threads()
