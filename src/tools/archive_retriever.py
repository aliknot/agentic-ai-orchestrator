from pydantic import SecretStr
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.tools import tool

# Import our global configurations
from src.config import GEMINI_API_KEY, PINECONE_INDEX_NAME


@tool
def search_static_archive(query: str) -> str:
    """
    Searches the internal Static Archive (OpenWebText) for relevant historical documents.
    Use this tool when the user asks about general knowledge, historical events, or
    information that does not require live, up-to-the-second web searches.
    """
    print(f"\n[Tool Execution] Searching internal archive for: '{query}'")

    try:
        # 1. Initialize the exact same embedding model used to build the DB
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", api_key=SecretStr(GEMINI_API_KEY)
        )

        # 2. Connect to the existing Pinecone index
        vector_store = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME, embedding=embeddings
        )

        # 3. Perform the similarity search (Fetch the top 3 most relevant chunks)
        results = vector_store.similarity_search(query, k=3)

        # 4. Format the results so the LLM can easily read them
        if not results:
            return "No relevant information found in the internal archive."

        formatted_results = "--- Archive Results ---\n\n"
        for i, doc in enumerate(results):
            formatted_results += f"Document {i+1}:\n{doc.page_content}\n\n"

        return formatted_results

    except Exception as e:
        return f"Error accessing the internal archive: {str(e)}"


# A quick local test to make sure it works!
if __name__ == "__main__":
    # The first document in your subset was about an earthquake in Haiti
    test_query = "What happened at the hospital in Haiti?"
    print(search_static_archive.invoke({"query": test_query}))
