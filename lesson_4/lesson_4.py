"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
Каждое изображение должно сохраняться в отдельном файле, название которого
соответствует названию изображения в URL-адресе.

Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg

— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и
 общем времени выполнения программы.
"""

import argparse
import asyncio
import aiohttp
import requests
import threading
from urllib.parse import urlparse
from multiprocessing import Process

import os
import time


# Default URLs
exp_urls = [
        'https://mykaleidoscope.ru/x/uploads/posts/2022-10/'
        '1666364979_14-mykaleidoscope-ru-p-krasivie-peizazhi-prirodi-oboi-17.jpg',
        'https://mykaleidoscope.ru/x/uploads/posts/2022-10/'
        '1666365039_2-mykaleidoscope-ru-p-krasivie-peizazhi-prirodi-oboi-4.jpg',
        'https://gas-kvas.com/uploads/posts/2023-02/'
        '1675483689_gas-kvas-com-p-fonovii-risunok-dlya-kompyutera-priroda-15.jpg',
        'https://catherineasquithgallery.com/uploads/posts/2021-03/'
        '1614612233_137-p-fon-dlya-fotoshopa-priroda-209.jpg',
        ]


def download_image(url, folder, start_time):
    """uploading photos to a folder"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extracting the file name from the URL
            filename = os.path.join(folder, os.path.basename(url))

            # Saving the image
            with open(filename, 'wb') as file:
                for chunk in response.iter_content():
                    file.write(chunk)

            print(f"Скачано: {url} -> {filename}, Время загрузки: {time.time()-start_time:.2f}")
        else:
            print(f"Ошибка при скачивании {url}")
    except Exception as e:
        print(f"Ошибка: {e}")


def threading_download_images(urls, folder):
    """implementing a multithreaded approach"""
    print("Многопоточный вариант:")
    start_time = time.time()

    # Creating a folder to save images, if there is none
    os.makedirs(folder, exist_ok=True)

    # Creating and launching streams for downloading images
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url, folder, start_time))
        threads.append(thread)
        thread.start()

    # We are waiting for the completion of all streams
    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nОбщее время выполнения для многопоточного подхода: {total_time}\n")


def multiprocessing_download_images(urls, folder):
    """implementation of a multiprocessor approach"""
    print("Многопроцессорный вариант:")
    start_time = time.time()

    # Creating a folder to save images, if there is none
    os.makedirs(folder, exist_ok=True)

    # Creating and launching streams for downloading images
    processes = []
    for url in urls:
        process = Process(target=download_image, args=(url, folder, start_time))
        processes.append(process)
        process.start()

    # We are waiting for the completion of all streams
    for process in processes:
        process.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nОбщее время выполнения для многопроцессорного подхода: {total_time}\n")


async def async_download_image(session, url, folder, start_time):
    """Downloading photos to a folder asynchronously."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                # Extracting the file name from the URL
                filename = os.path.join(folder, os.path.basename(url))

                # Saving the image
                with open(filename, 'wb') as file:
                    while True:
                        chunk = await response.content.read()
                        if not chunk:
                            break
                        file.write(chunk)

                print(f"Скачано: {url} -> {filename}, Время загрузки: {time.time()-start_time:.2f}")
            else:
                print(f"Ошибка при скачивании {url}")
    except Exception as e:
        print(f"Ошибка: {e}")


async def async_download_images(urls, folder):
    """Implementing an asynchronous approach."""
    print("Асинхронный вариант:")
    start_time = time.time()

    # Creating a folder to save images if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        tasks = [async_download_image(session, url, folder, start_time) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nОбщее время выполнения для асинхронного подхода: {total_time}\n")


if __name__ == "__main__":
    # Setting the list of URLs via command line arguments:
    parser = argparse.ArgumentParser(description='Загружаем изображения по URL-адресам')
    parser.add_argument('urls', nargs='?', default=exp_urls)
    args = parser.parse_args()

    # Launching a multithreaded approach:
    threading_folder = "threading_downloaded"
    threading_download_images(args.urls, threading_folder)

    # Launching a multiprocessor approach:
    multiprocessing_folder = "multiprocessing_downloaded"
    multiprocessing_download_images(args.urls, multiprocessing_folder)

    # Launching the asynchronous approach:
    async_folder = "async_downloaded"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_download_images(args.urls, async_folder))
