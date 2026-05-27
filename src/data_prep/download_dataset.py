import os
import pandas as pd
from datasets import load_dataset


def fetch_openwebtext():
    """
    Streams the first 10,000 documents of the OpenWebText corpus
    and saves it locally as a CSV, bypassing the 38GB download.
    """
    print("Initializing STREAMING download of OpenWebText (10k subset)...")

    try:
        # 1. Use streaming=True to read over the network without caching
        dataset = load_dataset("Skylion007/openwebtext", split="train", streaming=True)

        # 2. Pluck exactly the first 10,000 rows from the stream
        dataset_head = dataset.take(10000)

        # 3. Convert only those 10,000 rows into a DataFrame
        df = pd.DataFrame(dataset_head)

        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "openwebtext_10k.csv")

        # 4. Save to CSV
        df.to_csv(output_path, index=False)
        print(f"Success! {len(df)} documents securely saved to {output_path}")

    except Exception as e:
        print(f"An error occurred during dataset extraction: {e}")


if __name__ == "__main__":
    fetch_openwebtext()
