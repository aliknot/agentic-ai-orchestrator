import requests
import json
from langchain_core.tools import tool

# Import our global configurations
from src.config import SERPER_API_KEY


@tool
def search_live_web(query: str) -> str:
    """
    Searches the live internet for up-to-date information, news, and current events.
    Use this tool when the user asks about recent events, weather, stock prices,
    or anything that requires real-time factual knowledge outside of the static archive.
    """
    print(f"\n[Tool Execution] Searching the live web for: '{query}'")

    url = "https://google.serper.dev/search"
    payload = json.dumps(
        {
            "q": query,
            "num": 3,  # Keep it to top 3 results to save LLM context window space
        }
    )

    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Check for HTTP errors
        results = response.json()

        # Parse the organic search results
        organic_results = results.get("organic", [])

        if not organic_results:
            return "No web search results found for this query."

        formatted_results = "--- Live Web Results ---\n\n"
        for i, item in enumerate(organic_results):
            formatted_results += f"Source {i+1}: {item.get('title')}\n"
            formatted_results += f"Snippet: {item.get('snippet')}\n"
            formatted_results += f"Link: {item.get('link')}\n\n"

        return formatted_results

    except Exception as e:
        return f"Error executing web search: {str(e)}"


# A quick local test to verify the Serper connection!
if __name__ == "__main__":
    # Asking a question about something recent that wouldn't be in old archives
    test_query = "What is the current stock price of Apple?"
    print(search_live_web.invoke({"query": test_query}))
