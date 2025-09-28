import asyncio
from playwright.async_api import async_playwright

SPAN_CLASS = "data-item-fullname"
MAX_CONCURRENT = 35 

async def fetch_span(id, browser, outfile):
    url = f"https://namus.gov/MissingPersons/Case#/{id}"
    page = await browser.new_page()
    try:
        await page.goto(url)
        span = await page.query_selector(f"span.{SPAN_CLASS}")
        if span:
            span_text = await span.inner_text()
            print(f"ID {id} span content: {span_text}")
            outfile.write(f"ID {id} span content: {span_text}\n")
        else:
            print(f"ID {id} span not found")
    except:
        print(f"ID {id} page failed to load")
    finally:
        await page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = []
        with open("res.txt", "a") as outfile:
            for i in range(0, 250000):
                tasks.append(fetch_span(i, browser, outfile))
                # limit concurrency
                if len(tasks) >= MAX_CONCURRENT:
                    await asyncio.gather(*tasks)
                    tasks = []
            if tasks:
                await asyncio.gather(*tasks)
        await browser.close()

asyncio.run(main())
