import nest_asyncio
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser

nest_asyncio.apply()

# Launch Playwright browser
async_browser = create_async_playwright_browser(headless=False)  # change to True for headless mode
toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
tools = toolkit.get_tools()