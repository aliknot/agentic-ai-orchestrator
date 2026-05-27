import time
import pandas as pd
from pydantic import SecretStr
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Import global configurations
from src.config import GEMINI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME


def build_cloud_database(
    csv_path: str = "data/openwebtext_10k.csv",
    document_limit: int = 20,
):
    print("1. Initializing Pinecone Client...")
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Check if index exists, create a Serverless one if it doesn't
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"   -> Creating new Serverless Index: '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=3072,  # Required dimension for gemini-embedding-001
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        # Wait until Pinecone finishes spinning up the new index
        print("   -> Waiting for index to be ready...")
        while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
            time.sleep(2)

    print("\n2. Loading and chunking dataset...")
    df = pd.read_csv(csv_path)

    # We take a subset to stay well within Google's free API rate limits
    subset = df.head(document_limit)
    texts = subset["text"].tolist()

    # Split massive articles into 1000-character chunks with overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    documents = [Document(page_content=text) for text in texts]
    chunks = text_splitter.split_documents(documents)
    print(f"   -> Created {len(chunks)} chunks from {document_limit} documents.")

    print("\n3. Initializing Google Embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", api_key=SecretStr(GEMINI_API_KEY)
    )

    print("\n4. Uploading Vectors to Pinecone (Handling API Rate Limits)...")

    # Initialize the Pinecone Store reference first
    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME, embedding=embeddings
    )

    # BATCHING LOGIC: Process in groups of 90 to stay safely under the 100/min limit
    batch_size = 90
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        current_batch_num = (i // batch_size) + 1
        total_batches = (len(chunks) + batch_size - 1) // batch_size

        print(f"   -> Uploading batch {current_batch_num} of {total_batches}...")
        vector_store.add_documents(batch)

        # If there are more chunks left, pause to respect the rate limit
        if i + batch_size < len(chunks):
            print("      (Sleeping for 60 seconds to reset Google free-tier quotas...)")
            time.sleep(60)

    print("\nSuccess! Your Static Archive is now live on Pinecone.")


if __name__ == "__main__":
    build_cloud_database()
