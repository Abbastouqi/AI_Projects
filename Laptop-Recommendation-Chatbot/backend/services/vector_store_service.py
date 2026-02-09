"""
ChromaDB vector store service for similarity search
"""
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from core.config import settings
from services.embedding_service import EmbeddingService
from services.document_processor import LaptopDocument
import json

class VectorStoreService:
    """Manage ChromaDB vector store for laptop documents"""
    
    def __init__(self, collection_name: str = "laptop_recommendations"):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection_name = collection_name
        self.embedding_service = EmbeddingService()
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Laptop recommendation embeddings"}
            )
            print(f"Created new collection: {collection_name}")
    
    def add_documents(
        self,
        documents: List[LaptopDocument],
        batch_size: int = 100
    ) -> int:
        """
        Add laptop documents to vector store
        
        Args:
            documents: List of LaptopDocument objects
            batch_size: Number of documents to process at once
            
        Returns:
            Number of documents added
        """
        if not documents:
            return 0
        
        # Prepare data for ChromaDB
        ids = []
        contents = []
        metadatas = []
        
        for doc in documents:
            ids.append(f"laptop_{doc.laptop_id}")
            contents.append(doc.content)
            metadatas.append(doc.metadata)
        
        # Generate embeddings
        print(f"Generating embeddings for {len(documents)} documents...")
        embeddings = self.embedding_service.generate_embeddings_batch(
            contents,
            batch_size=batch_size
        )
        
        # Add to ChromaDB in batches
        for i in range(0, len(documents), batch_size):
            batch_ids = ids[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            batch_contents = contents[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            
            try:
                self.collection.add(
                    ids=batch_ids,
                    embeddings=batch_embeddings,
                    documents=batch_contents,
                    metadatas=batch_metadatas
                )
            except Exception as e:
                print(f"Error adding batch: {e}")
                # Try upserting instead
                self.collection.upsert(
                    ids=batch_ids,
                    embeddings=batch_embeddings,
                    documents=batch_contents,
                    metadatas=batch_metadatas
                )
        
        print(f"Added {len(documents)} documents to vector store")
        return len(documents)
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar laptops using semantic search
        
        Args:
            query: Search query text
            n_results: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of matching laptop documents with scores
        """
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Build where clause for filtering
        where_clause = None
        if filters:
            where_clause = self._build_where_clause(filters)
        
        # Search in ChromaDB
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results and results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        "laptop_id": results['metadatas'][0][i]['laptop_id'],
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                        "distance": results['distances'][0][i]
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
    
    def search_with_budget_filter(
        self,
        query: str,
        min_budget: Optional[int] = None,
        max_budget: Optional[int] = None,
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search with budget constraints
        
        Args:
            query: Search query
            min_budget: Minimum price in PKR
            max_budget: Maximum price in PKR
            n_results: Number of results
            
        Returns:
            Filtered search results
        """
        filters = {}
        
        if min_budget is not None:
            filters['min_price'] = min_budget
        if max_budget is not None:
            filters['max_price'] = max_budget
        
        return self.search(query, n_results, filters)
    
    def _build_where_clause(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build ChromaDB where clause from filters
        
        Note: ChromaDB has limited filtering capabilities
        We'll do additional filtering in the recommendation engine
        """
        where = {}
        
        # Brand filter
        if 'brand' in filters:
            where['brand'] = filters['brand']
        
        # Storage type filter
        if 'storage_type' in filters:
            where['storage_type'] = filters['storage_type']
        
        return where if where else None
    
    def get_document_by_id(self, laptop_id: int) -> Optional[Dict[str, Any]]:
        """Get document by laptop ID"""
        try:
            result = self.collection.get(
                ids=[f"laptop_{laptop_id}"],
                include=["documents", "metadatas"]
            )
            
            if result and result['ids']:
                return {
                    "laptop_id": laptop_id,
                    "content": result['documents'][0],
                    "metadata": result['metadatas'][0]
                }
        except Exception as e:
            print(f"Error getting document: {e}")
        
        return None
    
    def update_document(self, document: LaptopDocument):
        """Update existing document"""
        embedding = self.embedding_service.generate_embedding(document.content)
        
        try:
            self.collection.upsert(
                ids=[f"laptop_{document.laptop_id}"],
                embeddings=[embedding],
                documents=[document.content],
                metadatas=[document.metadata]
            )
            print(f"Updated document for laptop {document.laptop_id}")
        except Exception as e:
            print(f"Error updating document: {e}")
    
    def delete_document(self, laptop_id: int):
        """Delete document by laptop ID"""
        try:
            self.collection.delete(ids=[f"laptop_{laptop_id}"])
            print(f"Deleted document for laptop {laptop_id}")
        except Exception as e:
            print(f"Error deleting document: {e}")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_cache": self.embedding_service.get_cache_stats()
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
    
    def reset_collection(self):
        """Delete and recreate collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Laptop recommendation embeddings"}
            )
            print(f"Reset collection: {self.collection_name}")
        except Exception as e:
            print(f"Error resetting collection: {e}")
