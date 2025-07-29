import multiprocessing
import queue
import time
from ftplib import FTP
import os

DESTINATION_DIR = "/path/to/destination"
FTP_HOST = "ftp.example.com"
FTP_USER = "anonymous"
FTP_PASS = ""

NUM_DOWNLOADERS = 4

def find_files(file_queue):
    """
    Simulate fast file discovery on FTP server.
    Replace with actual FTP listing.
    """
    with FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd('/remote/path/')
        filenames = ftp.nlst()

    for filename in filenames:
        file_queue.put(filename)
        print(f"[Finder] Queued {filename}")

    # Signal downloaders to stop
    for _ in range(NUM_DOWNLOADERS):
        file_queue.put(None)

def download_file(file_queue):
    while True:
        filename = file_queue.get()
        if filename is None:
            break

        try:
            local_path = os.path.join(DESTINATION_DIR, filename)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with FTP(FTP_HOST) as ftp:
                ftp.login(FTP_USER, FTP_PASS)
                ftp.cwd('/remote/path/')
                with open(local_path, 'wb') as f:
                    print(f"[Downloader-{multiprocessing.current_process().name}] Downloading {filename}")
                    ftp.retrbinary(f"RETR {filename}", f.write)
        except Exception as e:
            print(f"[Downloader-{multiprocessing.current_process().name}] Error downloading {filename}: {e}")

def main():
    manager = multiprocessing.Manager()
    file_queue = manager.Queue()

    # Start the finder process
    finder = multiprocessing.Process(target=find_files, args=(file_queue,))
    finder.start()

    # Start downloader processes
    downloaders = []
    for _ in range(NUM_DOWNLOADERS):
        p = multiprocessing.Process(target=download_file, args=(file_queue,))
        p.start()
        downloaders.append(p)

    finder.join()
    for p in downloaders:
        p.join()

    print("[Main] All files downloaded.")

if __name__ == "__main__":
    main()
