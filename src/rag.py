from openai import AzureOpenAI
import config
from search import search

client = AzureOpenAI(
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_key=config.AZURE_OPENAI_API_KEY,
    api_version=config.AZURE_OPENAI_API_VERSION,
)

SYSTEM_PROMPT = """You are a medical research assistant.
Answer only from the given context.
If the answer is not in the context, say "I don't know based on the given articles."
After each fact, mention the PMID in brackets, like [PMID: 12345]."""


def ask(question):
    """Sawal leta hai, articles dhundta hai, aur model se jawab banwata hai."""
    # Step 1: Retrieve - milte-julte articles lana
    hits = search(question, top=3)

    # Step 2: Augment - articles ko ek text (context) me jodna
    context = "\n\n".join(
        f"PMID: {h['pmid']}\nTitle: {h['title']}\n{h['content']}" for h in hits
    )

    # Step 3: Generate - context + sawal model ko dena
    response = client.chat.completions.create(
        model=config.AZURE_OPENAI_CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0,   # 0 = model apni taraf se kam jodega
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [h["pmid"] for h in hits],
    }


if __name__ == "__main__":
    result = ask("What are the new treatments for type 2 diabetes?")
    print(result["answer"])
    print("\nSources:", result["sources"])