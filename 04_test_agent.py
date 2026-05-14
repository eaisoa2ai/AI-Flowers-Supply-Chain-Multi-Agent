"""
Test the complete FloraHolland AI agent workflow
"""
import asyncio
from pathlib import Path
from src.agents.graph import flora_agent
from src.config import settings

async def test_agent(image_path: str):
    """
    Test the agent with a flower image
    
    Args:
        image_path: Path to flower image
    """
    print("🌺 Testing FloraHolland AI Agent\n")
    print(f"Image: {image_path}\n")
    print("="*60)
    
    # Initial state
    initial_state = {
        "image_path": image_path,
        "visual_description": [],
        "species_candidates": [],
        "auction_data": {},
        "final_response": "",
        "error": ""
    }
    
    # Run agent
    print("\n🔄 Running agent workflow...\n")
    result = await flora_agent.ainvoke(initial_state)
    
    # Check for errors
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
        return
    
    # Display results
    print("="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    print("\n" + result['final_response'])
    print("\n" + "="*60)

async def main():
    """Main execution"""
    
    # Find a sample image
    image_dir = settings.FLORA_IMAGES_DIR
    
    if not image_dir.exists() or not list(image_dir.glob("*.jpg")):
        print("❌ No images found!")
        print(f"Run: python scripts/03_download_images.py first")
        return
    
    # Use first available image
    sample_image = list(image_dir.glob("*.jpg"))[0]
    
    await test_agent(str(sample_image))
    
    print("\n💡 To test with your own image:")
    print(f"   python -c 'import asyncio; from scripts.test_agent import test_agent; asyncio.run(test_agent(\"your_image.jpg\"))'")

if __name__ == "__main__":
    asyncio.run(main())