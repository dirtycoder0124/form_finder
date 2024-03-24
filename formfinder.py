import aiohttp
import asyncio
import sys
from bs4 import BeautifulSoup
from aiohttp.client_exceptions import ClientConnectorCertificateError

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text(), url
    except ClientConnectorCertificateError:
        print(f"{RED}SSL Certificate Error: Unable to verify certificate for {url}{RESET}")
        return None, url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, url

async def process_url(session, url):
    html, url = await fetch(session, url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form")
        text_inputs = soup.find_all("input", type="text")
        if forms or text_inputs:
            print(GREEN + f"Form Found at {url}" + RESET)
        else:
            print(RED + f"Form Not Found at {url}" + RESET)

async def main(filename):
    urls = []
    with open(filename, "r") as file:
        urls = [line.strip() for line in file]

    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    asyncio.run(main(filename))
