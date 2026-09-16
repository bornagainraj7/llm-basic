import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from llm_client import get_llm_response

print("========================= Simple RAG Chatbot (With external knowledge) =========================\n")
print("Type 'exit' or 'quit' to end the conversation.\n")


# step 1: Internal knowledge base (system prompt)
documents = [
    "Sam is a 32 year old software engineer working at Marsh Inc",
    "He is married to Maria.",
    "He studied computer science from UCLA",
    "His annual earnings from his job is $80,000. He also earns $4000 from his side business monthly."
]

# step 2: create embeddings
vectorizer = TfidfVectorizer()
doc_embeddings = vectorizer.fit_transform(documents)

# step 3: retriever function
def retrieve(query, top_k=2):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, doc_embeddings).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]

    print("\n========================== Printing variable for debugging ==========================\n")
    print(f"Cosine similarity: \n{similarities}")
    print(f"np argsort return: {np.argsort(similarities)}")
    print(f"np argsort [::-1]: {np.argsort(similarities)[::-1]}")
    print(f"np argsort [::-1][top_k]: {np.argsort(similarities)[::-1][:top_k]}")
    print("\n=====================================================================================\n")

    return [documents[i] for i in top_indices]


# step 4: conversation loop
while True:
    user_input = input("User Prompt: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    # step 5: retrieve relevant documents
    retrieved_docs = retrieve(user_input)
    context = "\n".join(retrieved_docs)

    # step 6: Augmented prompt with context
    message = [
        { 
            "role": "system", 
            "content": "Answer only using the context provided. If the answer is not in the context, say 'I don't know'."
        },
        {
            "role": "user", 
            "content": f"""Context: {context}\n\n
            User Query: {user_input}"""
        }
    ]

    response_text = get_llm_response(message, provider="gemini")
    # print("\n Retrieved context: ")
    # for doc in retrieved_docs:
    #     print("-", doc)

    print(f"\nAI response: {response_text}\n\n")


