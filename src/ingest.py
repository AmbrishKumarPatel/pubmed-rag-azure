import json
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import config
from embeddings import get_embedding   # Day 2 wala function

# index me data daalne/search karne wala client
search_client = SearchClient(
    endpoint=config.AZURE_SEARCH_ENDPOINT,
    index_name=config.AZURE_SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(config.AZURE_SEARCH_API_KEY),
)

# save kiya hua data padhna
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "abstracts.json")
with open(data_path, encoding="utf-8") as f:
    articles = json.load(f)

docs = []
for a in articles:
    text = a["title"] + ". " + a["abstract"]   # title + abstract ka vector banega
    docs.append({
        "id": a["pmid"],
        "pmid": a["pmid"],
        "title": a["title"],
        "content": a["abstract"],
        "embedding": get_embedding(text),
    })
    print("Embedding bani:", a["pmid"])

# sab documents ek saath index me bhejna
result = search_client.upload_documents(documents=docs)
print("Index me gaye:", sum(1 for r in result if r.succeeded), "/", len(docs))