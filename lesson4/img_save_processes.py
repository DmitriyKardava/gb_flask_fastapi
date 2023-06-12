from multiprocessing import Process
from tools import create_img_dir, get_urls, save_url, timeit


def save_process(**kwargs):
    timeit(save_url(url=kwargs.get('url')))


@timeit
def url_save_processes():
    create_img_dir()
    processes = []
    urls = get_urls()
    for url in urls:
        process = Process(target=save_process, kwargs={'url': url})
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print('End all jobs')


if __name__ == '__main__':
    url_save_processes()
