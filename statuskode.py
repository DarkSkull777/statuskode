import argparse
import requests
import threading
import queue as q
import random
import time
from urllib.parse import urlparse

# Fungsi untuk membaca user-agent dari file
def load_user_agents(file_path):
    with open(file_path, 'r') as f:
        user_agents = f.read().splitlines()
    return user_agents

# Fungsi untuk mendapatkan status kode HTTP
def get_status_code(url, user_agents, timeout=10):
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        return response.status_code
    except requests.RequestException:
        return None

# Fungsi untuk memproses target URL
def process_target(target, match_codes, filter_codes, output_file, user_agents):
    # Tambahkan protokol jika tidak ada
    parsed_url = urlparse(target)
    if not parsed_url.scheme:
        target = 'http://' + target

    status_code = get_status_code(target, user_agents)
    if status_code is not None:
        if match_codes and status_code not in match_codes:
            return
        if filter_codes and status_code in filter_codes:
            return
        result = f"{target} > {status_code}"
        print(result)
        if output_file:
            with open(output_file, 'a') as f:
                f.write(result + '\n')

# Fungsi worker untuk thread
def worker(task_queue, match_codes, filter_codes, output_file, user_agents, rate):
    while True:
        target = task_queue.get()
        if target is None:
            break
        start_time = time.time()
        try:
            process_target(target, match_codes, filter_codes, output_file, user_agents)
        except Exception as e:
            print(f"Error processing {target}: {e}")
        end_time = time.time()
        
        # Hitung waktu yang dibutuhkan untuk mematuhi rate limit
        elapsed_time = end_time - start_time
        wait_time = max(0, (1 / rate) - elapsed_time)
        time.sleep(wait_time)
        task_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description='Dymles Ganz 1337')
    parser.add_argument('-l', '--list', type=str, help='File containing list of target URLs')
    parser.add_argument('-mc', '--match-code', type=str, help='Comma-separated list of status codes to match')
    parser.add_argument('-fc', '--filter-code', type=str, help='Comma-separated list of status codes to filter out')
    parser.add_argument('-t', '--threads', type=int, default=30, help='Number of threads to use')
    parser.add_argument('-o', '--output', type=str, help='File to save results')
    parser.add_argument('-r', '--rate', type=float, default=float('inf'), help='Rate limit (requests per second)')

    args = parser.parse_args()

    if not args.list:
        parser.print_help()
        return

    match_codes = set(map(int, args.match_code.split(','))) if args.match_code else None
    filter_codes = set(map(int, args.filter_code.split(','))) if args.filter_code else None
    output_file = args.output
    rate = args.rate

    # Load user agents from file
    user_agents = load_user_agents('useragent.txt')

    task_queue = q.Queue()

    with open(args.list, 'r') as f:
        targets = f.read().splitlines()
        for target in targets:
            task_queue.put(target)

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(task_queue, match_codes, filter_codes, output_file, user_agents, rate))
        t.start()
        threads.append(t)

    task_queue.join()

    for _ in range(args.threads):
        task_queue.put(None)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
