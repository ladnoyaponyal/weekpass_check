import argparse
import requests
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

ASCII_ART = """
__        ____________ _                 _   _  
\ \      / /___ /___ /| | ___ __   __ _ | | | | 
 \ \ /\ / /  |_ \ |_ \| |/ / '_ \ / _` / __) __)
  \ V  V /  ___) |__) |   <| |_) | (_| \__ \__ \_
   \_/\_/  |____/____/|_|\_\ .__/ \__,_(   (   /
                           |_|          |_| |_|  

tg: @profileusername
"""

API_URL = "https://weakpass.com/api/v1/search/"

def query_hash(hash_value):
    try:
        response = requests.get(f"{API_URL}{hash_value}")
        response.raise_for_status()
        data = response.json()
        return data if 'pass' in data else None
    except requests.RequestException as e:
        #print(f"Error querying hash {hash_value}: {e}")
        return None

def check_hashes_multithread(hashes, output_file, max_workers=50):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_hash = {executor.submit(query_hash, h): h for h in hashes}
        with open(output_file, "a") as f:
            for future in as_completed(future_to_hash):
                hash_value = future_to_hash[future]
                try:
                    result = future.result()
                    if result:
                        f.write(f"{hash_value} : {result['pass']}\n")
                        print(f"Hash {hash_value} found: {result['pass']}")
                    else:
                        pass
			#print(f"Hash {hash_value} not found.")
                except Exception as exc:
                    print(f"Error processing hash {hash_value}: {exc}")

def check_hash_file(file_path, output_file, max_workers=50):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    with open(file_path, "r") as file:
        hashes = file.read().splitlines()
    
    check_hashes_multithread(hashes, output_file, max_workers=max_workers)

def main():
    parser = argparse.ArgumentParser(
        description="WeakPass Hash Checker - Проверка хешей через weakpass.com",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=ASCII_ART
    )
    parser.add_argument("-s", "--hash", help="Передача одного хеша для проверки")
    parser.add_argument("-l", "--list", help="Передача файла с хешами для проверки")
    parser.add_argument("-o", "--output", help="Файл для сохранения результатов", required=True)
    parser.add_argument("-t", "--threads", type=int, default=50, help="Количество потоков для обработки (по умолчанию 50)")

    args = parser.parse_args()
    print(ASCII_ART)

    # Очищаем файл перед записью
    with open(args.output, "w") as f:
        f.write("")  # Записываем пустую строку, очищая файл

    if args.hash:
        check_hashes_multithread([args.hash], args.output, max_workers=args.threads)
    elif args.list:
        check_hash_file(args.list, args.output, max_workers=args.threads)
    else:
        print("Ошибка: укажите либо -s для одного хеша, либо -l для файла с хешами")
        sys.exit(1)

if __name__ == "__main__":
    main()
