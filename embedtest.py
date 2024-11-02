from langchain_community.embeddings import XinferenceEmbeddings
xinference = XinferenceEmbeddings(
    server_url="http://12.12.12.101:9997", model_uid="custom-bge-m3"
)
res = xinference.embed_query("nihao")
print(res)