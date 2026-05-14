"""
ChromaDB utilities for botanical taxonomy
"""
import chromadb
from chromadb.utils import embedding_functions
from typing import Dict, List
from src.config import settings

class BotanicalDatabase:
    """Wrapper for ChromaDB botanical taxonomy database"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(settings.CHROMA_PERSIST_DIR))
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
    def get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                embedding_function=self.embedding_fn
            )
            print(f"✅ Loaded existing collection: {settings.CHROMA_COLLECTION_NAME}")
        except:
            collection = self.client.create_collection(
                name=settings.CHROMA_COLLECTION_NAME,
                embedding_function=self.embedding_fn,
                metadata={"description": "Oxford Flowers 102 botanical taxonomy"}
            )
            print(f"✅ Created new collection: {settings.CHROMA_COLLECTION_NAME}")
        
        return collection
    
    def add_species(self, collection, species_data: List[Dict]):
        """
        Add species to ChromaDB
        
        Args:
            collection: ChromaDB collection
            species_data: List of species dictionaries
        """
        documents = []
        metadatas = []
        ids = []
        
        for species in species_data:
            documents.append(species['description'])
            metadatas.append({
                'category_id': species['category_id'],  # Now required (will error if missing)
                'scientific_name': species['scientific_name'],
                'common_name': species['common_name'],
                'family': species['family'],
                'native_region': species.get('native_region', 'Unknown')
            })
            ids.append(f"species_{species['category_id']}")
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Added {len(species_data)} species to ChromaDB")
    
    def query(self, collection, query_text: str, n_results: int = 5) -> Dict:
        """
        Query ChromaDB for similar species
        
        Args:
            collection: ChromaDB collection
            query_text: Query string
            n_results: Number of results to return
            
        Returns:
            Query results
        """
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

# Global database instance
db = BotanicalDatabase()

def query_chromadb(query_text: str, n_results: int = 5) -> Dict:
    """
    Convenience function to query ChromaDB
    
    Args:
        query_text: Query string
        n_results: Number of results
        
    Returns:
        Query results
    """
    collection = db.get_or_create_collection()
    return db.query(collection, query_text, n_results)