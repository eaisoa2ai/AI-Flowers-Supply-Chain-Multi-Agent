"""
Download Oxford Flowers 102 dataset images
"""
from datasets import load_dataset
from src.config import settings
import os

def main():
    """Download Oxford Flowers images from Hugging Face"""
    print("📥 Downloading Oxford Flowers 102 Dataset\n")
    
    # Load dataset
    print("Loading from Hugging Face...")
    dataset = load_dataset("nelorth/oxford-flowers")
    
    print(f"✅ Dataset loaded: {len(dataset['train'])} images\n")
    
    # Create output directory
    settings.FLORA_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save sample images (first 20 from each class for demo)
    print("Saving sample images...")
    saved_count = 0
    
    for idx in range(min(200, len(dataset['train']))):
        sample = dataset['train'][idx]
        image = sample['image']
        label = sample['label']
        
        # Save image
        output_path = settings.FLORA_IMAGES_DIR / f"flower_{idx:04d}_class_{label:03d}.jpg"
        image.save(output_path)
        
        saved_count += 1
        if saved_count % 20 == 0:
            print(f"  Saved {saved_count} images...")
    
    print(f"\n✅ Downloaded {saved_count} sample images")
    print(f"📁 Location: {settings.FLORA_IMAGES_DIR}")
    print("\n💡 Tip: For full dataset, increase the range in the script")

if __name__ == "__main__":
    main()