# Chapter 09: Concurrency & Async

Python provides multiple ways to handle concurrent operations.

## Threading
For I/O-bound tasks:
```python
import threading
thread = threading.Thread(target=func)
thread.start()
```

## Multiprocessing
For CPU-bound tasks:
```python
from multiprocessing import Process
process = Process(target=func)
process.start()
```

## Async/Await
Modern async programming:
```python
async def fetch_data():
    await asyncio.sleep(1)
    return "Data"
```
