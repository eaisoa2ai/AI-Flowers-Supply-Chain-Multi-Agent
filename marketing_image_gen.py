"""
Bonus: Generate marketing images for identified flowers using OpenAI GPT-4o with DALL-E 3
"""
from openai import OpenAI
from src.config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_marketing_image(
    species_name: str, 
    common_name: str, 
    style: str = "professional"
) -> str:
    """
    Generate a marketing image for a flower species using GPT-4o + DALL-E 3
    
    Args:
        species_name: Scientific name
        common_name: Common name
        style: Image style (professional, artistic, minimal)
        
    Returns:
        URL to generated image
    """
    
    # Style prompts
    style_prompts = {
        "professional": "professional product photography, studio lighting, white background, high detail, commercial quality, crisp focus",
        "artistic": "beautiful artistic oil painting, impressionist style, elegant composition, soft vibrant colors, museum quality",
        "minimal": "minimalist design, clean aesthetic, simple solid color background, modern photography, elegant simplicity"
    }
    
    prompt = f"""A stunning {common_name} ({species_name}) flower, {style_prompts.get(style, style_prompts['professional'])}. 
Perfect for FloraHolland auction catalog. High-resolution, photorealistic."""
    
    print(f"🎨 Generating marketing image with GPT-4o + DALL-E 3...")
    print(f"Species: {common_name} ({species_name})")
    print(f"Style: {style}")
    print(f"Prompt: {prompt}\n")
    
    try:
        # Using DALL-E 3 via OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )
        
        image_url = response.data[0].url
        
        print(f"✅ Image generated successfully!")
        print(f"URL: {image_url}\n")
        
        return image_url
    
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return None

def enhance_prompt_with_gpt4o(species_name: str, common_name: str, auction_data: dict = None) -> str:
    """
    Optional: Use GPT-4o to create an enhanced, context-aware image prompt
    
    Args:
        species_name: Scientific name
        common_name: Common name
        auction_data: Optional auction data for context
        
    Returns:
        Enhanced prompt for DALL-E 3
    """
    
    context = f"""Create a detailed, professional image generation prompt for:
    
Flower: {common_name} ({species_name})
"""
    
    if auction_data:
        context += f"""
Auction Context:
- Origin: {auction_data.get('origin', 'Unknown')}
- Quality Grade: {auction_data.get('quality_grade', 'A1')}
- Target Market: Wholesale buyers at FloraHolland
"""
    
    context += """

Generate a DALL-E 3 prompt (max 200 words) for a professional marketing image that:
1. Highlights the flower's premium quality
2. Uses professional photography style
3. Emphasizes commercial appeal for florists
4. Maintains botanical accuracy

Return ONLY the prompt, no explanation."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": context}],
            temperature=0.7,
            max_tokens=300
        )
        
        enhanced_prompt = response.choices[0].message.content
        print(f"🧠 GPT-4o enhanced prompt:\n{enhanced_prompt}\n")
        
        return enhanced_prompt
    
    except Exception as e:
        print(f"⚠️  Could not enhance prompt: {e}")
        return f"{common_name} ({species_name}) professional photography"

def main():
    """Demo marketing image generation"""
    print("🌺 FloraHolland Marketing Image Generator (GPT-4o + DALL-E 3)\n")
    print("="*70)
    
    # Example: Generate images for identified species
    examples = [
        ("Rosa hybrid tea", "Tea Rose", "professional"),
        ("Tulipa gesneriana", "Garden Tulip", "artistic"),
        ("Helianthus annuus", "Sunflower", "minimal")
    ]
    
    for scientific, common, style in examples:
        print(f"\n{'='*70}")
        print(f"Species: {common} ({scientific})")
        print(f"Style: {style}")
        print('='*70)
        
        # Option 1: Direct generation
        image_url = generate_marketing_image(scientific, common, style)
        
        # Option 2: Enhanced with GPT-4o (commented out - use if needed)
        # enhanced_prompt = enhance_prompt_with_gpt4o(scientific, common)
        # response = client.images.generate(model="dall-e-3", prompt=enhanced_prompt, size="1024x1024", quality="hd")
        # image_url = response.data[0].url
        
        if image_url:
            print(f"\n💡 Use this image for:")
            print(f"   ✓ FloraHolland auction catalog")
            print(f"   ✓ Social media marketing")
            print(f"   ✓ Wholesale buyer presentations")
            print(f"   ✓ E-commerce listings")
        
        print()

if __name__ == "__main__":
    main()