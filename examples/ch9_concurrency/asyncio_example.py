#!/usr/bin/env python3
"""Async/await for concurrent I/O."""

import asyncio

async def fetch_data(name, delay):
    """Simulate fetching data."""
    print(f"{name}: Starting...")
    await asyncio.sleep(delay)
    print(f"{name}: Done!")
    return f"Data from {name}"

async def main():
    """Run concurrent tasks."""
    tasks = [
        fetch_data("Task 1", 2),
        fetch_data("Task 2", 1),
        fetch_data("Task 3", 1.5)
    ]
    
    start = asyncio.get_event_loop().time()
    results = await asyncio.gather(*tasks)
    end = asyncio.get_event_loop().time()
    
    print(f"\nResults: {results}")
    print(f"Total time: {end-start:.2f}s")

# Use event loop directly to avoid circular import
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.close()