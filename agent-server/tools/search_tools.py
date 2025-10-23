import asyncio
from playwright.async_api import async_playwright
from langchain_core.tools import tool
from bs4 import BeautifulSoup
import json

async def scrape_search_results(
    url: str, 
    result_selector: str, 
    title_selector: str, 
    link_selector: str, 
    description_selector: str
) -> str:
    """
    Scrapes search results from a given URL using Playwright and parses them with BeautifulSoup.
    Returns a JSON string of the extracted results. Limited to maximum 50 results.
    """
    print(f"🔧 TOOL_RUNTIME: Starting search: {url}")
    
    async with async_playwright() as p:
        print("🔧 TOOL_RUNTIME: Launching browser...")
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        print(f"🔧 TOOL_RUNTIME: Navigating to: {url}")
        await page.goto(url)
        
        print("🔧 TOOL_RUNTIME: Extracting page content...")
        html_content = await page.content()
        await browser.close()

    print("🔧 TOOL_RUNTIME: Parsing search results (max 50)...")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    result_count = 0
    max_results = 50
    
    for item in soup.select(result_selector):
        title_element = item.select_one(title_selector)
        link_element = item.select_one(link_selector)
        description_element = item.select_one(description_selector)

        title = title_element.get_text(strip=True) if title_element else "No Title"
        link = link_element['href'] if link_element and 'href' in link_element.attrs else "No Link"
        description = description_element.get_text(strip=True) if description_element else "No Description"

        results.append({"title": title, "link": link, "description": description})
        result_count += 1
        
        if result_count % 10 == 0:
            print(f"🔧 TOOL_RUNTIME: Found {result_count} results so far...")
        
        # Stop after reaching max results
        if result_count >= max_results:
            print(f"🔧 TOOL_RUNTIME: Reached maximum limit of {max_results} results")
            break

    # Format and log the search results in JSON
    json_results = json.dumps(results, ensure_ascii=False, indent=2)
    print(f"🔧 TOOL_RUNTIME: Search results (JSON format, {len(results)} items):\n{json_results}")
    print(f"✅ TOOL_RUNTIME: Search completed. Found {len(results)} results (limited to {max_results}).")
    
    return json_results

@tool
def google_search(query: str) -> str:
    """Searches Google for the given query and returns a JSON string of parsed results."""
    print(f"🔧 TOOL_RUNTIME: Starting Google search for: {query}")
    
    search_url = f"https://www.google.com/search?q={query}"
    result = asyncio.run(scrape_search_results(
        search_url,
        result_selector="div.g",
        title_selector="h3",
        link_selector="a",
        description_selector=".VwiC3b"
    ))
    
    print(f"✅ TOOL_RUNTIME: Google search completed for: {query}")
    
    return result

@tool
def bing_search(query: str) -> str:
    """Searches Bing for the given query and returns a JSON string of parsed results."""
    print(f"🔧 TOOL_RUNTIME: Starting Bing search for: {query}")
    
    search_url = f"https://www.bing.com/search?q={query}"
    result = asyncio.run(scrape_search_results(
        search_url,
        result_selector="li.b_algo",
        title_selector="h2 > a",
        link_selector="h2 > a",
        description_selector=".b_vlist2 > .b_snippet"
    ))
    
    print(f"✅ TOOL_RUNTIME: Bing search completed for: {query}")
    
    return result

@tool
def baidu_search(query: str) -> str:
    """Searches Baidu for the given query and returns a JSON string of parsed results."""
    print(f"🔧 TOOL_RUNTIME: Starting Baidu search for: {query}")
    
    search_url = f"https://www.baidu.com/s?wd={query}"
    result = asyncio.run(scrape_search_results(
        search_url,
        result_selector=".result.c-container",
        title_selector="h3 > a",
        link_selector="h3 > a",
        description_selector=".c-abstract"
    ))
    
    print(f"✅ TOOL_RUNTIME: Baidu search completed for: {query}")
    
    return result
