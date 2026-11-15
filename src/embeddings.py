from openai import AzureOpenAI
import config

# wahi client jo chat me use kiya tha
client = AzureOpenAI(
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_key=config.AZURE_OPENAI_API_KEY,
    api_version=config.AZURE_OPENAI_API_VERSION,
)


def get_embedding(text):
    """Ek text leta hai aur uska vector (numbers ki list) wapas deta hai."""
    response = client.embeddings.create(
        model=config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
    )
    return response.data[0].embedding


def similarity(vec1, vec2):
    """Do vectors kitne milte-julte hai. 1 ke paas = bahut similar."""
    # dono vectors ke numbers ko aapas me guna karke jodna (dot product)
    return sum(a * b for a, b in zip(vec1, vec2))


# ye hissa tabhi chalega jab aap is file ko seedha run karoge
if __name__ == "__main__":
    v1 = get_embedding("Diabetes is treated with insulin.")
    v2 = get_embedding("Insulin therapy helps patients with high blood sugar.")
    v3 = get_embedding("The football match was played yesterday.")

    print("Vector ki length:", len(v1))
    print("Pehle 5 numbers:", v1[:5])
    print("Diabetes vs Insulin  :", round(similarity(v1, v2), 3))
    print("Diabetes vs Football :", round(similarity(v1, v3), 3))