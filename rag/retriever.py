from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = BASE_DIR / "models" / "rag"

INDEX_PATH = MODEL_DIR / "knowledge.index"

METADATA_PATH = MODEL_DIR / "knowledge_metadata.npy"


# ---------------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# ---------------------------------------------------------
# RAG RETRIEVER
# ---------------------------------------------------------

class KnowledgeRetriever:

    def __init__(
        self,
        top_k=3
    ):

        self.top_k = top_k

        # ---------------------------------------------
        # CHECK FILES
        # ---------------------------------------------

        if not INDEX_PATH.exists():

            raise FileNotFoundError(
                f"FAISS index not found: {INDEX_PATH}"
            )

        if not METADATA_PATH.exists():

            raise FileNotFoundError(
                f"Metadata file not found: {METADATA_PATH}"
            )

        # ---------------------------------------------
        # LOAD FAISS INDEX
        # ---------------------------------------------

        self.index = faiss.read_index(
            str(INDEX_PATH)
        )

        # ---------------------------------------------
        # LOAD METADATA
        # ---------------------------------------------

        self.metadata = np.load(
            METADATA_PATH,
            allow_pickle=True
        )

        # ---------------------------------------------
        # LOAD EMBEDDING MODEL
        # ---------------------------------------------

        self.model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    def search(
        self,
        query
    ):

        if not query or not query.strip():

            return []

        # ---------------------------------------------
        # CREATE QUERY EMBEDDING
        # ---------------------------------------------

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        # ---------------------------------------------
        # SEARCH FAISS
        # ---------------------------------------------

        scores, indices = self.index.search(
            query_embedding,
            min(
                self.top_k,
                self.index.ntotal
            )
        )

        results = []

        # ---------------------------------------------
        # BUILD RESULTS
        # ---------------------------------------------

        for score, index_position in zip(
            scores[0],
            indices[0]
        ):

            if index_position < 0:
                continue

            item = self.metadata[
                index_position
            ]

            results.append({

                "source":
                    item["source"],

                "text":
                    item["text"],

                "score":
                    float(score)

            })

        return results


# ---------------------------------------------------------
# TEST RETRIEVER
# ---------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("JEEVAN-NETRA RAG RETRIEVER TEST")
    print("=" * 55)

    retriever = KnowledgeRetriever(
        top_k=3
    )

    question = (
        "What should I do during a flood?"
    )

    results = retriever.search(
        question
    )

    print()
    print(
        f"Question: {question}"
    )

    print()

    for number, result in enumerate(
        results,
        start=1
    ):

        print(
            f"Result {number}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Similarity: {result['score']:.4f}"
        )

        print(
            f"Text: {result['text']}"
        )

        print(
            "-" * 55
        )