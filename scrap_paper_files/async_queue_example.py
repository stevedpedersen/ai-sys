# async_queue_example.py
import asyncio

async def worker(name, queue):
    while True:
        task = await queue.get()
        if task is None:  # A sentinel value to signal shutdown.
            break
        print(f"{name} processing task: {task}")
        # Simulate processing time
        await asyncio.sleep(1)
        print(f"{name} completed task: {task}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    # Create a pool of workers (simulate your agents).
    workers = [asyncio.create_task(worker(f"Worker-{i}", queue)) for i in range(4)]

    # Enqueue tasks (simulate tasks from your orchestrator).
    tasks = ["Task A", "Task B", "Task C", "Task D"]
    for task in tasks:
        await queue.put(task)

    # Wait until all tasks are processed.
    await queue.join()

    # Send shutdown signals to the workers.
    for _ in workers:
        await queue.put(None)

    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())