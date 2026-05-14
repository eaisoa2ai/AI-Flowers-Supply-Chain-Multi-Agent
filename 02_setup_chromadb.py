"""
Setup ChromaDB with botanical taxonomy data
"""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import db
from src.config import settings


def main():
    """Index botanical data into ChromaDB"""
    print("💾 Setting up ChromaDB Botanical Database\n")
    
    # Load botanical data
    data_file = settings.PROCESSED_DATA_DIR / "botanical_database.json"
    
    if not data_file.exists():
        print(f"❌ Botanical data not found: {data_file}")
        print("Run: python scripts/01_generate_botanical_data.py first")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        botanical_data = json.load(f)
    
    print(f"📖 Loaded {len(botanical_data)} species from {data_file}")
    
    # Get or create collection
    collection = db.get_or_create_collection()
    
    # Clear existing data
    try:
        count = collection.count()
        if count > 0:
            print(f"🗑️  Clearing {count} existing records...")
            collection.delete(where={})
    except:
        pass
    
    # Prepare data for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for species in botanical_data:
        # Create searchable document
        doc = f"{species['common_name']} {species['description']}"
        documents.append(doc)
        
        # Store metadata with category_id
        metadatas.append({
            'common_name': species['common_name'],
            'scientific_name': species['scientific_name'],
            'family': species['family'],
            'native_region': species['native_region'],
            'category_id': species['category_id']  # Include category ID
        })
        
        ids.append(f"species_{species['category_id']}")  # Use category_id for ID
    
    # Add to ChromaDB
    print(f"\n📥 Indexing {len(documents)} species...")
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Indexed {len(documents)} species into ChromaDB")
    
    # Test query
    print("\n🔍 Testing retrieval...")
    test_query = "red flower with thorny stem"
    results = collection.query(
        query_texts=[test_query],
        n_results=3
    )
    
    print(f"\nQuery: '{test_query}'")
    print("Top 3 matches:")
    for i, metadata in enumerate(results['metadatas'][0], 1):
        print(f"  {i}. {metadata['common_name']} ({metadata['scientific_name']}) - ID: {metadata['category_id']}")
    
    print("\n✅ ChromaDB setup complete!")
    print(f"📁 Database location: {settings.CHROMA_PERSIST_DIR}")


if __name__ == "__main__":
    main()