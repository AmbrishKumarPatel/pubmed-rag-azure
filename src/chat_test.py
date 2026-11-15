from openai import AzureOpenAI
import config   # apni config.py file se settings lena

# client = Azure ke model se baat karne wala object
client = AzureOpenAI(
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,   # model ka address
    api_key=config.AZURE_OPENAI_API_KEY,           # password
    api_version=config.AZURE_OPENAI_API_VERSION,   # API ka version
)

# model ko message bhejna
response = client.chat.completions.create(
    model=config.AZURE_OPENAI_CHAT_DEPLOYMENT,     # deployment ka naam
    messages=[
        # system = model ko batana ki use kaise behave karna hai
        {"role": "system", "content": "You explain things in simple English."},
        # user = aapka sawal
        {"role": "user", "content": "What is RAG? Explain in 3 lines."},
    ],
)

# jawab print karna
print(response.choices[0].message.content)

# kitne tokens kharch hue (isi se bill banta hai)
print("Tokens used:", response.usage.total_tokens)