from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
import config
from embeddings import get_embedding

search_client = SearchClient(
    endpoint=config.AZURE_SEARCH_ENDPOINT,
    index_name=config.AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(config.AZURE_SEARCH_API_KEY),
)


def search(query, top=3):
    """Sawal ke liye sabse milte-julte articles dhundta hai (hybrid search)."""
    # sawal ka vector banana
    vector_query = VectorizedQuery(
        vector=get_embedding(query),
        k_nearest_neighbors=top,   # kitne paas wale vectors chahiye
        fields="embedding",        # index ke kis field me dhundna hai
    )

    results = search_client.search(
        search_text=query,               # keyword search
        vector_queries=[vector_query],   # meaning wali search
        select=["pmid", "title", "content"],
        top=top,
    )

    # results ko simple list me badalna
    return [
        {
            "pmid": r["pmid"],
            "title": r["title"],
            "content": r["content"],
            "score": r["@search.score"],
        }
        for r in results
    ]


if __name__ == "__main__":
    hits = search("What are the new treatments for type 2 diabetes?")
    for h in hits:
        print(round(h["score"], 4), "|", h["pmid"], "|", h["title"][:80])