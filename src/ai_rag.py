import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rag.retriever import KnowledgeRetriever
from src.ai_response import load_model, generate_response


class JEEVANAI:
    def __init__(self):
        print("Loading JEEVAN AI...")

        # Load RAG retriever
        self.retriever = KnowledgeRetriever(top_k=3)

        # Load AI response model
        self.tokenizer, self.model = load_model()

        print("JEEVAN AI is ready.")

    def ask(self, question):
        # Retrieve trusted information from the knowledge base
        results = self.retriever.search(question)

        if not results:
            context = "No trusted safety information was found."
        else:
            context_parts = []

            for result in results:
                context_parts.append(
                    f"Source: {result['source']}\n"
                    f"Information: {result['text']}"
                )

            context = "\n\n".join(context_parts)

        # Generate response using retrieved context
        answer = generate_response(
            question,
            context,
            self.tokenizer,
            self.model
        )

        return {
            "question": question,
            "answer": answer,
            "sources": results
        }


if __name__ == "__main__":
    ai = JEEVANAI()

    question = "What should I do during a flood?"

    result = ai.ask(question)

    print("\nQUESTION:")
    print(result["question"])

    print("\nJEEVAN AI:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(similarity: {source['score']:.4f})"
        )

