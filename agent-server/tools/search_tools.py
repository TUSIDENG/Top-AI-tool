import asyncio
from playwright.async_api import async_playwright
from langchain_core.tools import tool
from bs4 import BeautifulSoup
import json

async def scrape_search_results(url: str, result_selector: str, title_selector: str, link_selector: str, description_selector: str) -> str:
    """
    Scrapes search results from a given URL using Playwright and parses them with BeautifulSoup.
    Returns a JSON string of the extracted results.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        html_content = await page.content()
        await browser.close()

    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    for item in soup.select(result_selector):
        title_element = item.select_one(title_selector)
        link_element = item.select_one(link_selector)
        description_element = item.select_one(description_selector)

        title = title_element.get_text(strip=True) if title_element else "No Title"
        link = link_element['href'] if link_element and 'href' in link_element.attrs else "No Link"
        description = description_element.get_text(strip=True) if description_element else "No Description"

        results.append({"title": title, "link": link, "description": description})
    return json.dumps(results, ensure_ascii=False, indent=2)

@tool
def google_search(query: str) -> str:
    """Searches Google for the given query and returns a JSON string of parsed results."""
    search_url = f"https://www.google.com/search?q={query}"
    # These selectors might need adjustment based on actual Google search page structure
    return asyncio.run(scrape_search_results(
        search_url,
        result_selector="div.g", # Common selector for search results
        title_selector="h3",
        link_selector="a",
        description_selector=".VwiC3b" # Common selector for description
    ))

@tool
def bing_search(query: str) -> str:
    """Searches Bing for the given query and returns a JSON string of parsed results."""
    search_url = f"https://www.bing.com/search?q={query}"
    # These selectors might need adjustment based on actual Bing search page structure
    return asyncio.run(scrape_search_results(
        search_url,
        result_selector="li.b_algo", # Common selector for search results
        title_selector="h2 > a",
        link_selector="h2 > a",
        description_selector=".b_vlist2 > .b_snippet" # Common selector for description
    ))

@tool
def baidu_search(query: str) -> str:
    """Searches Baidu for the given query and returns a JSON string of parsed results."""
    search_url = f"https://www.baidu.com/s?wd={query}"
    # These selectors might need adjustment based on actual Baidu search page structure
    return asyncio.run(scrape_search_results(
        search_url,
        result_selector=".result.c-container", # Common selector for search results
        title_selector="h3 > a",
        link_selector="h3 > a",
        description_selector=".c-abstract" # Common selector for description
    ))
