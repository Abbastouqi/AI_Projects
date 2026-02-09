from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from core.config import settings
import json

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            embedding_function=self.embeddings
        )
    
    def add_laptops(self, laptops_file: str):
        """Load laptops from JSON and add to vector store"""
        with open(laptops_file, 'r', encoding='utf-8') as f:
            laptops = json.load(f)
        
        documents = []
        for laptop in laptops:
            content = json.dumps(laptop, ensure_ascii=False)
            metadata = {
                "name": laptop["name"],
                "price_pkr": laptop["price_pkr"],
                "category": laptop["category"]
            }
            documents.append(Document(page_content=content, metadata=metadata))
        
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
        print(f"Added {len(documents)} laptops to vector store")

if __name__ == "__main__":
    manager = VectorStoreManager()
    manager.add_laptops("../data/laptops.json")
