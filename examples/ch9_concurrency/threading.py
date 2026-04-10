#!/usr/bin/env python3
"""Threading for I/O-bound tasks."""

import threading
import time

def worker_thread(name, delay):
    """Worker function for threading."""
    for i in range(3):
        print(f"{name}: {i}")
        time.sleep(delay)

# Create and start threads
thread1 = threading.Thread(target=worker_thread, args=("Thread-1", 1))
thread2 = threading.Thread(target=worker_thread, args=("Thread-2", 0.5))

start = time.time()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(f"\nCompleted in {time.time()-start:.2f}s")