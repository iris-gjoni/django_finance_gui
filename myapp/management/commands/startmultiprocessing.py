import csv
import os
import shutil
import time

from django.core.management.base import BaseCommand
from multiprocessing import Process, Manager

max_size = 180


class Command(BaseCommand):
    help = 'Start the multiprocessing manager and processes.'

    def handle(self, *args, **kwargs):
        start_manager()


def start_manager():
    print("starting manager")
    with Manager() as manager:
        file_path = "c:/quant/shared_data/share.csv"
        writer_process = Process(target=update_writer, args=(file_path,))
        writer_process.start()
        writer_process.join()


def update_writer(file_path):
    while True:
        # Code to check for updates and write them to shared_data
        new_data = check_for_updates()
        if new_data:
            if is_file_too_large(file_path, max_size):
                rotate_file(file_path)

            with open(file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(new_data)

        time.sleep(3)


def check_for_updates():
    data = ["10", "APPL"]
    return data


def is_file_too_large(file_path, max_size):
    """Check if the file size exceeds the max_size (in bytes)."""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) > max_size
    return False


def rotate_file(file_path):
    """Rotate the file - rename the current file and create a new one with the original name."""
    print("rotating file")
    rotated_file_path = file_path + ".old"
    shutil.move(file_path, rotated_file_path)
