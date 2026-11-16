import json
import os
import requests
import xml.etree.ElementTree as ET

# PubMed ki free API ka address
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(query, max_results=20):
    """Topic search karke articles ke ID (PMID) ki list deta hai."""
    r = requests.get(
        f"{BASE}/esearch.fcgi",
        params={"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"},
    )
    return r.json()["esearchresult"]["idlist"]


def fetch_abstracts(pmids):
    """PMID ki list leke har article ka title aur abstract lata hai."""
    r = requests.get(
        f"{BASE}/efetch.fcgi",
        params={"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"},
    )
    root = ET.fromstring(r.content)   # XML ko padhne layak banana

    articles = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title_el = article.find(".//ArticleTitle")
        title = "".join(title_el.itertext()) if title_el is not None else ""
        # abstract kai hisso me hota hai, sabko jod do
        parts = ["".join(el.itertext()) for el in article.findall(".//AbstractText")]
        abstract = " ".join(parts).strip()

        if abstract:   # jis article me abstract nahi, use chhod do
            articles.append({"pmid": pmid, "title": title, "abstract": abstract})
    return articles


if __name__ == "__main__":
    pmids = search_pubmed("type 2 diabetes treatment", max_results=20)
    articles = fetch_abstracts(pmids)

    # data folder me save karna (src ke ek level upar)
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "abstracts.json"), "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print("Articles save hue:", len(articles))