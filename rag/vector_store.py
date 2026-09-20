from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"

MODEL_DIR = BASE_DIR / "models" / "rag"

INDEX_PATH = MODEL_DIR / "knowledge.index"

METADATA_PATH = MODEL_DIR / "knowledge_metadata.npy"


# ---------------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# ---------------------------------------------------------
# LOAD KNOWLEDGE DOCUMENTS
# ---------------------------------------------------------

def load_documents():

    documents = []

    if not KNOWLEDGE_DIR.exists():

        raise FileNotFoundError(
            f"Knowledge directory not found: {KNOWLEDGE_DIR}"
        )

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if text:

            documents.append({
                "source": file_path.name,
                "text": text
            })

    return documents


# ---------------------------------------------------------
# CREATE TEXT CHUNKS
# ---------------------------------------------------------

def create_chunks(
    text,
    chunk_size=100,
    overlap=20
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words)
        )

        chunk = " ".join(
            words[start:end]
        )

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        if end >= len(words):
            break

        start = end - overlap

    return chunks


# ---------------------------------------------------------
# BUILD VECTOR STORE
# ---------------------------------------------------------

def build_vector_store():

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"Knowledge directory: {KNOWLEDGE_DIR}"
    )

    documents = load_documents()

    if not documents:

        raise ValueError(
            "No .txt knowledge documents found."
        )

    print(
        f"Documents loaded: {len(documents)}"
    )

    # -----------------------------------------------------
    # CREATE CHUNKS
    # -----------------------------------------------------

    chunks = []

    metadata = []

    for document in documents:

        document_chunks = create_chunks(
            document["text"]
        )

        for chunk in document_chunks:

            chunks.append(chunk)

            metadata.append({
                "source": document["source"],
                "text": chunk
            })

    print(
        f"Chunks created: {len(chunks)}"
    )

    # -----------------------------------------------------
    # LOAD EMBEDDING MODEL
    # -----------------------------------------------------

    print(
        "Loading embedding model..."
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    print(
        "Embedding model loaded."
    )

    # -----------------------------------------------------
    # CREATE EMBEDDINGS
    # -----------------------------------------------------

    print(
        "Creating embeddings..."
    )

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # -----------------------------------------------------
    # CREATE FAISS INDEX
    # -----------------------------------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    # -----------------------------------------------------
    # SAVE FAISS INDEX
    # -----------------------------------------------------

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    # -----------------------------------------------------
    # SAVE METADATA
    # -----------------------------------------------------

    np.save(
        METADATA_PATH,
        np.array(
            metadata,
            dtype=object
        ),
        allow_pickle=True
    )

    # -----------------------------------------------------
    # SUCCESS INFORMATION
    # -----------------------------------------------------

    print()
    print("=" * 55)
    print("VECTOR STORE CREATED SUCCESSFULLY")
    print("=" * 55)

    print(
        f"Documents: {len(documents)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    print(
        f"Vector dimension: {dimension}"
    )

    print(
        f"Vectors stored: {index.ntotal}"
    )

    print(
        f"FAISS index: {INDEX_PATH}"
    )

    print(
        f"Metadata: {METADATA_PATH}"
    )

    print("=" * 55)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":

    build_vector_store()