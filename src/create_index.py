from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
import config

# index banane/badalne wala client
index_client = SearchIndexClient(
    endpoint=config.AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(config.AZURE_SEARCH_API_KEY),
)

# index ke columns (fields)
fields = [
    # id = har chunk ki unique pehchaan (primary key jaisa)
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    # pmid = PubMed article ka number, filter karne ke kaam aayega
    SimpleField(name="pmid", type=SearchFieldDataType.String, filterable=True),
    # title aur content = text, jisme keyword search hogi
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="content", type=SearchFieldDataType.String),
    # embedding = 1536 numbers ka vector, jisme meaning wali search hogi
    SearchField(
        name="embedding",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="vector-profile",
    ),
]

# vector search kaise chalegi (HNSW = tez search ka algorithm)
vector_search = VectorSearch(
    algorithms=[HnswAlgorithmConfiguration(name="hnsw-config")],
    profiles=[
        VectorSearchProfile(
            name="vector-profile",
            algorithm_configuration_name="hnsw-config",
        )
    ],
)

# index ka poora design
index = SearchIndex(
    name=config.AZURE_SEARCH_INDEX_NAME,
    fields=fields,
    vector_search=vector_search,
)

# index banao (pehle se ho to update kar do)
result = index_client.create_or_update_index(index)
print("Index ban gaya:", result.name)