import os
import threading
import multiprocessing
import time


# Пошук ключових слів у файлі
def search_keywords_in_file(file_path, keywords, result_dict, lock):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:  # Захист словника від одночасного доступу
                        result_dict.setdefault(keyword, []).append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Розподілення файлів між потоками
def process_files_threading(files, keywords):
    threads = []
    result_dict = {}
    lock = threading.Lock()

    # Створення та запуск потоків
    for file_path in files:
        thread = threading.Thread(
            target=search_keywords_in_file,
            args=(file_path, keywords, result_dict, lock),
        )
        threads.append(thread)
        thread.start()

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    return result_dict


# Основна функція для threading
def main_threading(file_list, keywords):
    start_time = time.time()
    result = process_files_threading(file_list, keywords)
    end_time = time.time()

    print(f"Threading approach took {end_time - start_time:.4f} seconds")
    return result


# Пошук ключових слів у файлі (з multiprocessing)
def search_keywords_in_file_mp(file_path, keywords, queue):
    result = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result.setdefault(keyword, []).append(file_path)
        queue.put(result)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Розподілення файлів між процесами
def process_files_multiprocessing(files, keywords):
    processes = []
    queue = multiprocessing.Queue()
    result_dict = {}

    # Створення та запуск процесів
    for file_path in files:
        process = multiprocessing.Process(
            target=search_keywords_in_file_mp, args=(file_path, keywords, queue)
        )
        processes.append(process)
        process.start()

    # Очікування завершення всіх процесів
    for process in processes:
        process.join()

    # Збір результатів з черги
    while not queue.empty():
        result = queue.get()
        for keyword, file_paths in result.items():
            result_dict.setdefault(keyword, []).extend(file_paths)

    return result_dict


# Основна функція для multiprocessing
def main_multiprocessing(file_list, keywords):
    start_time = time.time()
    result = process_files_multiprocessing(file_list, keywords)
    end_time = time.time()

    print(f"Multiprocessing approach took {end_time - start_time:.4f} seconds")
    return result


if __name__ == "__main__":
    # Список файлів для тестування
    file_list = ["words_1.txt", "words_2.txt", "words_3.txt"]
    # Ключові слова для пошуку
    keywords = ["choose", "come", "cost"]

    print("Threading Version:")
    result_threading = main_threading(file_list, keywords)
    print(result_threading)

    print("\nMultiprocessing Version:")
    result_multiprocessing = main_multiprocessing(file_list, keywords)
    print(result_multiprocessing)
