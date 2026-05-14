"""
Complete demonstration of the FloraHolland AI Agent workflow
Step-by-step following the architecture pipeline with configurable parameters
"""
import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.models.schemas import BotanicalInfo
from pydantic_ai import Agent


# ⚙️ CONFIGURATION - Adjust these for testing
N_SPECIES = 10        # Number of species to generate (max 102)
N_IMAGES = 20         # Number of images to download (max 8189)

def load_botanical_database():
    """Load botanical database from file if it exists"""
    botanical_db_path = settings.PROCESSED_DATA_DIR / "botanical_database.json"
    if botanical_db_path.exists():
        with open(botanical_db_path, 'r') as f:
            return json.load(f)
    else:
        print("❌ No botanical database found!")
        print("Run Step 1 first: python scripts/01_generate_botanical_data.py")
        return None

def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def print_config():
    """Display test configuration"""
    print_header("CONFIGURATION")
    print(f"🎛️ Test Parameters:")
    print(f"   Species to generate: {N_SPECIES}")
    print(f"   Images to download: {N_IMAGES}")
    print(f"\n💰 Estimated costs:")
    print(f"   Data generation: ~${(N_SPECIES * 0.003):.3f} (GPT-4o-mini)")
    print(f"   Image download: FREE")
    print(f"   ChromaDB indexing: FREE (local)")
    print(f"\n⚠️ To test full dataset (102 species):")
    print(f"   Set N_SPECIES = 102 (cost: ~$0.30)")


async def step1_generate_botanical_data():
    """STEP 1: Generate botanical database using Pydantic AI"""
    print_header("STEP 1: BOTANICAL DATA GENERATION (Pydantic AI)")
    
    from pydantic_ai import Agent
    from src.models.schemas import BotanicalInfo
    
    # Oxford Flowers 102 species with category IDs
    OXFORD_FLOWERS_CATEGORIES = {
        0: "pink primrose", 
        1: "hard-leaved pocket orchid", 
        2: "canterbury bells", 
        3: "sweet pea",
        4: "english marigold", 
        5: "tiger lily", 
        6: "moon orchid", 
        7: "bird of paradise", 
        8: "monkshood",
        9: "globe thistle", 
        10: "snapdragon", 
        11: "colt's foot", 
        12: "king protea", 
        13: "spear thistle",
        14: "yellow iris", 
        15: "globe-flower", 
        16: "purple coneflower", 
        17: "peruvian lily", 
        18: "balloon flower",
        19: "giant white arum lily", 
        20: "fire lily", 
        21: "pincushion flower", 
        22: "fritillary",
        23: "red ginger", 
        24: "grape hyacinth", 
        25: "corn poppy", 
        26: "prince of wales feathers",
        27: "stemless gentian", 
        28: "artichoke", 
        29: "sweet william", 
        30: "carnation", 
        31: "garden phlox",
        32: "love in the mist", 
        33: "mexican aster", 
        34: "alpine sea holly", 
        35: "ruby-lipped cattleya",
        36: "cape flower", 
        37: "great masterwort", 
        38: "siam tulip", 
        39: "lenten rose", 
        40: "barbeton daisy",
        41: "daffodil", 
        42: "sword lily", 
        43: "poinsettia", 
        44: "bolero deep blue", 
        45: "wallflower",
        46: "marigold", 
        47: "buttercup", 
        48: "oxeye daisy", 
        49: "common dandelion", 
        50: "petunia",
        51: "wild pansy", 
        52: "primula", 
        53: "sunflower", 
        54: "pelargonium", 
        55: "bishop of llandaff",
        56: "gaura", 
        57: "geranium", 
        58: "orange dahlia", 
        59: "pink-yellow dahlia", 
        60: "cautleya spicata",
        61: "japanese anemone", 
        62: "black-eyed susan", 
        63: "silverbush", 
        64: "californian poppy", 
        65: "osteospermum",
        66: "spring crocus", 
        67: "bearded iris", 
        68: "windflower", 
        69: "tree poppy",
        70: "gazania", 
        71: "azalea", 
        72: "water lily", 
        73: "rose", 
        74: "thorn apple", 
        75: "morning glory",
        76: "passion flower", 
        77: "lotus", 
        78: "toad lily", 
        79: "anthurium", 
        80: "frangipani", 
        81: "clematis",
        82: "hibiscus", 
        83: "columbine", 
        84: "desert-rose", 
        85: "tree mallow", 
        86: "magnolia", 
        87: "cyclamen",
        88: "watercress", 
        89: "canna lily", 
        90: "hippeastrum", 
        91: "bee balm", 
        92: "ball moss", 
        93: "foxglove",
        94: "bougainvillea", 
        95: "camellia", 
        96: "mallow", 
        97: "mexican petunia", 
        98: "bromelia", 
        99: "blanket flower",
        100: "trumpet creeper", 
        101: "blackberry lily"
    }
    
    print(f"🌸 Generating botanical data for all 102 species...\n")
    
    # Initialize agent
    agent = Agent(
        settings.DATA_GEN_MODEL,
        output_type=BotanicalInfo,
        system_prompt="You are a botanical expert. Provide accurate scientific information."
    )
    
    botanical_database = []
    
    for category_id, common_name in OXFORD_FLOWERS_CATEGORIES.items():
        print(f"[{category_id+1}/102] Generating: {common_name}")
        
        try:
            result = await agent.run(f"Provide botanical information for: {common_name}")
            data = result.output.model_dump()
            data['common_name'] = common_name
            data['category_id'] = category_id  # Add category ID
            botanical_database.append(data)
            print(f"   ✅ {data['scientific_name']} ({data['family']})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n✅ Generated {len(botanical_database)} botanical records")
    
    # Save to file
    output_path = settings.PROCESSED_DATA_DIR / "botanical_database.json"
    with open(output_path, 'w') as f:
        import json
        json.dump(botanical_database, f, indent=2)
    
    print(f"💾 Saved to: {output_path}")
    
    return botanical_database


def verify_step1(botanical_database):
    """Verify Step 1: Check generated data"""
    print_header("STEP 1 VERIFICATION: Checking Generated Botanical Data")
    
    if botanical_database:
        print(f"✅ Successfully generated {len(botanical_database)} species\n")
        
        # Show first 3 examples
        print("📊 Sample data (first 3 species):\n")
        for i, species in enumerate(botanical_database[:3], 1):
            print(f"{i}. {species['common_name']}")
            print(f"   Scientific: {species['scientific_name']}")
            print(f"   Family: {species['family']}")
            print(f"   Native: {species['native_region']}")
            print(f"   Description: {species['description'][:150]}...")
            print()
        
        # Save to file
        output_path = settings.PROCESSED_DATA_DIR / "botanical_database.json"
        with open(output_path, 'w') as f:
            json.dump(botanical_database, f, indent=2)
        
        print(f"💾 Saved to: {output_path}")
        print(f"📦 File size: {output_path.stat().st_size / 1024:.1f} KB")
        
        return True
    else:
        print("❌ No data generated! Check errors above.")
        return False


def step2_download_images():
    """STEP 2: Download Oxford Flowers images"""
    print_header("STEP 2: DOWNLOADING OXFORD FLOWERS IMAGES")
    
    from datasets import load_dataset
    
    print(f"📥 Downloading {N_IMAGES} images from Oxford Flowers 102...\n")
    
    # Load dataset
    print("Loading dataset from Hugging Face...")
    dataset = load_dataset("nelorth/oxford-flowers", split="train")
    print(f"✅ Dataset loaded: {len(dataset)} total images available\n")
    
    # Download N_IMAGES samples
    images_dir = settings.FLORA_IMAGES_DIR
    images_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded_count = 0
    
    for i in range(min(N_IMAGES, len(dataset))):
        item = dataset[i]
        image = item['image']
        label = item['label']
        
        # Save image
        image_filename = f"flower_{i:04d}_class_{label:03d}.jpg"
        image_path = images_dir / image_filename
        
        image.save(image_path)
        downloaded_count += 1
        
        if (i + 1) % 10 == 0:
            print(f"[{i+1}/{N_IMAGES}] Downloaded...")
    
    print(f"\n✅ Downloaded {downloaded_count} images to {images_dir}")
    
    return downloaded_count


def verify_step2():
    """Verify Step 2: Check downloaded images"""
    print_header("STEP 2 VERIFICATION: Checking Downloaded Images")
    
    images_dir = settings.FLORA_IMAGES_DIR
    image_files = list(images_dir.glob("*.jpg"))
    
    if image_files:
        print(f"✅ Found {len(image_files)} images in {images_dir}\n")
        
        # Show first 5 files
        print("📸 Sample images:")
        for i, img_path in enumerate(image_files[:5], 1):
            size_kb = img_path.stat().st_size / 1024
            print(f"   {i}. {img_path.name} ({size_kb:.1f} KB)")
        
        # Display total storage
        print(f"\n📊 Total storage: {sum(f.stat().st_size for f in image_files) / 1024 / 1024:.1f} MB")
        
        return True
    else:
        print("❌ No images found!")
        return False


def step3_setup_chromadb(botanical_database):
    """STEP 3: Index botanical data into ChromaDB"""
    print_header("STEP 3: INDEXING INTO CHROMADB (RAG Setup)")
    
    from src.utils.database import db
    
    print(f"🔍 Setting up ChromaDB with {len(botanical_database)} species...\n")
    
    # Get or create collection
    collection = db.get_or_create_collection()
    
    # Clear existing data
    try:
        existing_count = collection.count()
        if existing_count > 0:
            print(f"🗑️  Clearing {existing_count} existing records...")
            collection.delete(where={})
    except:
        pass
    
    # Prepare data for indexing
    documents = []
    metadatas = []
    ids = []
    
    for species in botanical_database:  # Changed: iterate directly
        # Create searchable document
        doc = f"{species['common_name']} {species['description']}"
        documents.append(doc)
        
        # Store metadata WITH category_id
        metadatas.append({
            'common_name': species['common_name'],
            'scientific_name': species['scientific_name'],
            'family': species['family'],
            'native_region': species['native_region'],
            'category_id': species['category_id']  # ← ADD THIS!
        })
        
        ids.append(f"species_{species['category_id']}")  # ← Use category_id for ID
    
    # Add to ChromaDB
    print("Adding species to ChromaDB...")
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"\n✅ Indexed {len(botanical_database)} species into ChromaDB")
    print(f"📁 Database location: {settings.CHROMA_PERSIST_DIR}")
    
    return True


def verify_step3():
    """Verify Step 3: Test ChromaDB retrieval"""
    print_header("STEP 3 VERIFICATION: Testing ChromaDB RAG")
    
    from src.utils.database import db
    
    test_queries = [
        "red flower with thorny stem",
        "yellow flower with large petals",
        "purple orchid"
    ]
    
    print("🔍 Testing semantic search...\n")
    
    collection = db.get_or_create_collection()
    
    for query in test_queries:
        print(f"Query: '{query}'")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        
        if results and results['metadatas']:
            print("   Top matches:")
            for i, metadata in enumerate(results['metadatas'][0], 1):
                print(f"   {i}. {metadata['common_name']} ({metadata['scientific_name']})")
        else:
            print("   ⚠️  No results found")
        print()
    
    return True

async def step4_build_and_test_agent():
    """STEP 4: Build LangGraph agent and test workflow"""
    print_header("STEP 4: BUILDING LANGGRAPH AGENT & TESTING WORKFLOW")
    
    from src.agents.graph import flora_agent
    
    # Find a sample image
    images_dir = settings.FLORA_IMAGES_DIR
    image_files = list(images_dir.glob("*.jpg"))
    
    if not image_files:
        print("❌ No images found for testing!")
        print("Run Step 2 first to download images.")
        return False
    
    sample_image = image_files[0]
    print(f"📸 Using sample image: {sample_image.name}\n")
    
    # Create initial state
    initial_state = {
        "image_path": str(sample_image),
        "visual_description": [],
        "species_candidates": [],
        "auction_data": {},
        "final_response": "",
        "error": ""
    }
    
    print("🚀 Running LangGraph agent workflow...")
    print("   → Node 1: Vision analysis (Gemini 2.0 Flash)...")
    print("   → Node 2: Species identification (DeepSeek + ChromaDB RAG)...")
    print("   → Node 3: Auction intelligence (Dynamic pricing)...")
    print("   → Node 4: Report synthesis (DeepSeek)...")
    print()
    
    try:
        # Run the agent
        result = await flora_agent.ainvoke(initial_state)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return False
        else:
            print("✅ Agent workflow completed successfully!\n")
            return result
    
    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_step4(result):
    """Verify Step 4: Display agent output"""
    print_header("STEP 4 VERIFICATION: Agent Output")
    
    if result and result.get('final_response'):
        print("="*80)
        print("📋 FLORAHOLLAND MARKET INTELLIGENCE REPORT")
        print("="*80)
        print(result['final_response'])
        print("="*80)
        
        # Show intermediate results
        print("\n📊 Workflow Details:\n")
        
        if result.get('visual_description'):
            print("🔍 Visual Analysis:")
            print(f"   Features extracted: {len(result['visual_description'])} observations")
        
        if result.get('species_candidates'):
            print("\n🌺 Species Candidates:")
            for candidate in result['species_candidates'][:3]:
                print(f"   • {candidate.get('common_name')} ({candidate.get('scientific_name')})")
                print(f"     Confidence: {candidate.get('confidence', 'N/A')}")
        
        if result.get('auction_data'):
            print("\n💰 Auction Data:")
            auction = result['auction_data']
            print(f"   Price: €{auction.get('auction_price_eur', 0):.2f}/stem")
            print(f"   Trend: {auction.get('price_trend', 'N/A')}")
            print(f"   Volume: {auction.get('daily_volume_stems', 0):,} stems/day")
        
        return True
    else:
        print("❌ No valid output generated")
        return False


def show_cost_summary():
    """Show final cost summary"""
    print_header("COST ANALYSIS")
    
    print("💰 Actual Costs (This Run):\n")
    print(f"   Botanical data generation ({N_SPECIES} species):")
    print(f"      GPT-4o-mini: ~${(N_SPECIES * 0.003):.3f}")
    print(f"   Image download ({N_IMAGES} images): FREE")
    print(f"   ChromaDB indexing: FREE (local)")
    print(f"   Agent test run: ~$0.002")
    print(f"   " + "-"*60)
    print(f"   TOTAL: ~${(N_SPECIES * 0.003 + 0.002):.3f}")
    
    print("\n📊 Per-Request Costs (Production):\n")
    print("   Gemini 2.0 Flash (vision):  $0.0000 (FREE)")
    print("   DeepSeek V3.2 (reasoning):  $0.0017")
    print("   ChromaDB (local):           $0.0000")
    print("   " + "-"*60)
    print("   TOTAL per identification:   $0.0017")
    
    print("\n🎯 Volume Pricing:\n")
    print("   100 identifications:     $0.17")
    print("   1,000 identifications:   $1.70")
    print("   10,000 identifications:  $17.00")
    
    print("\n✅ 95% cheaper than GPT-4 Vision (~$50 per 1,000 runs)")


async def main00():
    """Run complete demonstration"""
    print("\n" + "🌺"*40)
    print("  ROYAL FLORAHOLLAND AI AGENT - STEP-BY-STEP DEMO")
    print("🌺"*40)
    
    # Show configuration
    print_config()
    
    input("\n👉 Press Enter to start Step 1 (Data Generation)...")
    
    # STEP 1: Generate botanical data
    botanical_database = await step1_generate_botanical_data()
    if not verify_step1(botanical_database):
        print("\n❌ Step 1 failed. Exiting.")
        return
    
    input("\n👉 Press Enter to start Step 2 (Download Images)...")
    
    # STEP 2: Download images
    step2_download_images()
    if not verify_step2():
        print("\n❌ Step 2 failed. Exiting.")
        return
    
    input("\n👉 Press Enter to start Step 3 (Setup ChromaDB)...")
    
    # STEP 3: Setup ChromaDB
    step3_setup_chromadb(botanical_database)
    if not verify_step3():
        print("\n❌ Step 3 failed. Exiting.")
        return
    
    input("\n👉 Press Enter to start Step 4 (Build & Test Agent)...")
    
    # STEP 4: Build and test agent
    result = await step4_build_and_test_agent()
    if not result:
        print("\n❌ Step 4 failed. Exiting.")
        return
    
    verify_step4(result)
    
    # Show cost summary
    show_cost_summary()
    
    print("\n" + "="*80)
    print("✅ ALL STEPS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\n📚 Next steps:")
    print("   1. Adjust N_SPECIES and N_IMAGES at the top of this script")
    print("   2. Test with full dataset (N_SPECIES=102, N_IMAGES=8189)")
    print("   3. Try your own flower images")
    print("   4. Customize prompts in src/agents/nodes.py")
    print("   5. Deploy as FastAPI endpoint")
    print()

async def main():
    """Run complete demonstration - comment out steps you don't want to run"""
    
    # Step 1: Generate botanical data
    botanical_database = await step1_generate_botanical_data()
    verify_step1(botanical_database)
    
    # Step 2: Download images
    step2_download_images()
    verify_step2()

    
    # Step 3: Setup ChromaDB
    #botanical_database = load_botanical_database()
    step3_setup_chromadb(botanical_database)
    verify_step3()
    
    # Step 4: Build and test agent
    result = await step4_build_and_test_agent()
    verify_step4(result)
    
    # Show cost summary
    show_cost_summary()


if __name__ == "__main__":
    asyncio.run(main())