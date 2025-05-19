import weaviate

def get_weaviate_client():
    return weaviate.Client("http://localhost:8080")
