import asyncio
import random


async def retry_with_backoff(
    operation,
    retries=3,
    base_delay=1
):
    for attempt in range(retries):

        try:
            return await operation()

        except Exception as e:

            if attempt == retries - 1:
                print(f"Request failed after {retries} attempts: {e}")
                return None

            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, 0.5)

            wait_time = delay + jitter

            print(
                f"Request failed. "
                f"Retrying in {wait_time:.2f}s..."
            )

            await asyncio.sleep(wait_time)

    return None