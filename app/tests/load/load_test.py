import asyncio
import websockets

CONCURRENCY = 5000
BATCH_SIZE = 1000
DELAY = 0.1
URI = "ws://localhost/ws/chat/"
MESSAGES = 2

async def worker(cid):
    async with websockets.connect(URI) as ws:
        for i in range(MESSAGES):
            await ws.send(f"{cid}-{i}")
            await ws.recv()

async def run_batch(start, size):
    tasks = [asyncio.create_task(worker(i)) for i in range(start, start + size)]
    await asyncio.gather(*tasks)

async def main():
    batches = (CONCURRENCY + BATCH_SIZE - 1) // BATCH_SIZE
    cid = 0
    for b in range(batches):
        size = min(BATCH_SIZE, CONCURRENCY - cid)
        print(f"Batch {b+1}/{batches}: clients {cid}–{cid+size-1}")
        await run_batch(cid, size)
        cid += size
        await asyncio.sleep(DELAY)

if __name__ == "__main__":
    asyncio.run(main())
