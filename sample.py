import asyncio
import aiohttp

# Configuration
URL = "http://127.0.0.1:5000/Code/1211"
CONCURRENCY = 500  # Number of simultaneous active connections. 

async def bombard(session, url, worker_id):
    """An infinite loop that fires requests as fast as the network allows."""
    count = 0
    while True:
        try:
            # Fire the request
            async with session.get(url) as response:
                # Await the read to ensure the connection is handled properly
                await response.read()
                count += 1
                
                # Print every 100th request per worker to avoid lagging the console
                if count % 100 == 0:
                    print(f"[Worker {worker_id}] Fired {count} requests | Last Status: {response.status}")
                    
        except Exception as e:
            print(f"[Worker {worker_id}] Connection dropped/failed: {e}")
            # Brief pause on failure so we don't spam error messages instantly
            await asyncio.sleep(0.5) 

async def main():
    print(f"Going full throttle on {URL} with {CONCURRENCY} concurrent workers...")
    print("Press Ctrl+C to abort the test.\n")
    
    # limit=0 removes the ceiling on concurrent connections in the pool
    connector = aiohttp.TCPConnector(limit=0) 
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        # Spin up hundreds of concurrent workers
        for i in range(CONCURRENCY):
            task = asyncio.create_task(bombard(session, URL, i))
            tasks.append(task)
        
        # Run them all infinitely
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        # Run the async event loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nThrottle pulled back. Stress test aborted.")