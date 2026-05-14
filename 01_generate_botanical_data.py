"""
Generate botanical database using Pydantic AI
"""
import json
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_ai import Agent
from src.models.schemas import BotanicalInfo
from src.config import settings

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


async def main():
    """Generate botanical database for all 102 species"""
    print("🌺 Generating Botanical Database using Pydantic AI\n")
    print(f"Model: {settings.DATA_GEN_MODEL}")
    print(f"Total species: {len(OXFORD_FLOWERS_CATEGORIES)}\n")
    
    # Initialize Pydantic AI agent
    agent = Agent(
        settings.DATA_GEN_MODEL,
        result_type=BotanicalInfo,
        system_prompt="You are a botanical expert. Provide accurate scientific information."
    )
    
    botanical_database = []
    
    # Generate data for all 102 species
    for category_id, common_name in OXFORD_FLOWERS_CATEGORIES.items():
        print(f"[{category_id+1}/102] {common_name}...", end=" ")
        
        try:
            # Run agent
            result = await agent.run(
                f"""For the flower "{common_name}", provide:
- scientific_name: binomial nomenclature
- family: botanical family name
- native_region: geographic origin
- description: 150-200 words on visual characteristics, leaf structure, growth habit"""
            )
            
            # Get structured output
            data = result.output.model_dump()
            data['common_name'] = common_name
            data['category_id'] = category_id  # Add category ID for matching with images
            
            botanical_database.append(data)
            print(f"✅ {data['scientific_name']}")
            
        except Exception as e:
            print(f"❌ {e}")
    
    # Save to JSON
    output_file = settings.PROCESSED_DATA_DIR / "botanical_database.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(botanical_database, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {len(botanical_database)} species")
    print(f"💾 Saved to: {output_file}")
    print(f"💰 Estimated cost: ~${len(botanical_database) * 0.003:.2f}")


if __name__ == "__main__":
    asyncio.run(main())