"""
Initialize vector store with laptop documents
Run this after seeding the database
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import SessionLocal, Laptop
from services.document_processor import DocumentProcessor
from services.vector_store_service import VectorStoreService

def initialize_vector_store():
    """Load laptops from database and create vector embeddings"""
    
    print("=" * 60)
    print("Initializing Vector Store for RAG Pipeline")
    print("=" * 60)
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Fetch all laptops from database
        print("\n1. Fetching laptops from database...")
        laptops = db.query(Laptop).all()
        
        if not laptops:
            print("❌ No laptops found in database!")
            print("Please run: python scripts/init_database.py first")
            return
        
        print(f"✓ Found {len(laptops)} laptops")
        
        # Convert to dictionaries
        print("\n2. Processing laptop documents...")
        laptop_dicts = []
        for laptop in laptops:
            laptop_dicts.append({
                "id": laptop.id,
                "brand": laptop.brand,
                "model": laptop.model,
                "cpu": laptop.cpu,
                "ram_gb": laptop.ram_gb,
                "storage_gb": laptop.storage_gb,
                "storage_type": laptop.storage_type,
                "gpu": laptop.gpu,
                "display_size": laptop.display_size,
                "price_pkr": laptop.price_pkr,
                "battery_hours": laptop.battery_hours,
                "weight_kg": laptop.weight_kg,
                "ideal_for": laptop.ideal_for,
                "source_url": laptop.source_url
            })
        
        # Create documents with expert advice
        documents = DocumentProcessor.batch_create_documents(laptop_dicts)
        print(f"✓ Created {len(documents)} enriched documents")
        
        # Initialize vector store
        print("\n3. Initializing ChromaDB vector store...")
        vector_store = VectorStoreService()
        
        # Check if collection already has documents
        stats = vector_store.get_collection_stats()
        if stats.get('document_count', 0) > 0:
            print(f"⚠ Collection already has {stats['document_count']} documents")
            response = input("Reset and reinitialize? (yes/no): ")
            if response.lower() == 'yes':
                print("Resetting collection...")
                vector_store.reset_collection()
            else:
                print("Keeping existing collection")
                return
        
        # Add documents to vector store
        print("\n4. Generating embeddings and adding to vector store...")
        print("(This may take a minute...)")
        
        count = vector_store.add_documents(documents)
        
        print(f"\n✓ Successfully added {count} documents to vector store")
        
        # Display statistics
        print("\n" + "=" * 60)
        print("Vector Store Statistics")
        print("=" * 60)
        
        stats = vector_store.get_collection_stats()
        print(f"Collection: {stats.get('collection_name')}")
        print(f"Documents: {stats.get('document_count')}")
        
        cache_stats = stats.get('embedding_cache', {})
        print(f"\nEmbedding Cache:")
        print(f"  Cached embeddings: {cache_stats.get('cached_embeddings', 0)}")
        print(f"  Cache size: {cache_stats.get('cache_size_mb', 0):.2f} MB")
        
        # Test search
        print("\n" + "=" * 60)
        print("Testing Vector Search")
        print("=" * 60)
        
        test_queries = [
            "programming laptop under 120000 PKR",
            "FSC student budget laptop",
            "gaming laptop with good graphics"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            results = vector_store.search(query, n_results=3)
            
            if results:
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    metadata = result['metadata']
                    print(f"  {i}. {metadata['brand']} {metadata['model']} - PKR {metadata['price_pkr']:,}")
                    print(f"     Similarity: {result['similarity_score']:.3f}")
            else:
                print("  No results found")
        
        print("\n" + "=" * 60)
        print("✓ Vector Store Initialization Complete!")
        print("=" * 60)
        print("\nYou can now start the FastAPI server:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    initialize_vector_store()
