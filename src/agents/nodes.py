"""
LangGraph node implementations
"""
import json
from typing import Dict
from src.agents.state import FloraState
from src.models.clients import gemini_client, openrouter_client
from src.utils.database import query_chromadb
from src.utils.pricing import get_dynamic_auction_data

async def vision_node(state: FloraState) -> Dict:
    """
    Node 1: Extract visual features using Gemini 2.0 Flash
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with visual description
    """
    try:
        prompt = """Analyze this flower image with botanical precision:

1. **PRIMARY COLOR**: Main color(s) and patterns
2. **PETALS**: Count (exact or range), shape, arrangement
3. **LEAVES**: Shape, texture, edge pattern
4. **SIZE**: Estimate (small/medium/large)
5. **DISTINCTIVE FEATURES**: Thorns, center structure, unique characteristics
6. **GROWTH PATTERN**: Single bloom, cluster, spray

Return as structured text for botanical identification."""
        
        description = gemini_client.analyze_image(
            state['image_path'],
            prompt
        )
        
        return {
            "visual_description": [{
                "description": description,
                "source": "gemini-2.0-flash"
            }]
        }
    
    except Exception as e:
        return {"error": f"Vision analysis failed: {str(e)}"}


async def species_identification_node(state: FloraState) -> Dict:
    """Node 2: Identify species using ChromaDB RAG + DeepSeek reasoning"""
    try:
        print("🔍 [Node 2] Starting species identification...")
        
        # Check if visual description exists
        if not state.get('visual_description'):
            print("❌ [Node 2] No visual description in state!")
            return {"error": "No visual description available"}
        
        # Get visual description
        visual_desc = state['visual_description'][-1]['description']
        print(f"✅ [Node 2] Got visual description: {visual_desc[:100]}...")
        
        # Query ChromaDB for similar species
        print("🔍 [Node 2] Querying ChromaDB...")
        rag_results = query_chromadb(visual_desc, n_results=5)
        
        # Check if we got results
        if not rag_results.get('metadatas') or not rag_results['metadatas'][0]:
            print("❌ [Node 2] No ChromaDB results!")
            return {"error": "No matching species found in database"}
        
        print(f"✅ [Node 2] Got {len(rag_results['metadatas'][0])} ChromaDB matches")
        
        # DeepSeek reasoning
        print("🤖 [Node 2] Calling DeepSeek for reasoning...")
        prompt = f"""You are a botanical expert at FloraHolland auction house.

                VISUAL ANALYSIS:
                {visual_desc}

                TOP MATCHES FROM BOTANICAL DATABASE:
                {json.dumps(rag_results['metadatas'][0], indent=2)}

                TASK:
                Determine the most likely species identification.

                RESPOND WITH JSON:
                {{
                "scientific_name": "...",
                "common_name": "...",
                "confidence": 0.XX,
                "reasoning": "Why this species matches the visual features",
                "distinguishing_features": ["feature1", "feature2"]
                }}

                Only JSON, no preamble."""
        
        response = openrouter_client.generate(
            prompt,
            system_prompt="You are a botanical expert. Always respond with valid JSON only.",
            temperature=0.3
        )
        
        print(f"✅ [Node 2] Got DeepSeek response: {response[:100]}...")
        
        # Parse JSON response - strip markdown fences if present
        response_clean = response.strip()
        if response_clean.startswith('```'):
            # Remove ```json and closing ```
            response_clean = response_clean.split('\n', 1)[1]  # Remove first line
            response_clean = response_clean.rsplit('```', 1)[0]  # Remove closing ```
            response_clean = response_clean.strip()
        
        species_data = json.loads(response_clean)
        species_data['rag_matches'] = rag_results
        
        print(f"✅ [Node 2] Identified: {species_data['common_name']}")
        
        return {
            "species_candidates": [species_data]
        }
    
    except Exception as e:
        print(f"❌ [Node 2] Error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Species identification failed: {str(e)}"}


async def auction_intelligence_node(state: FloraState) -> Dict:
    """
    Node 3: Generate FloraHolland auction data with dynamic pricing
    
    Args:
        state: Current graph state with species identification
        
    Returns:
        Updated state with auction data
    """
    try:
        # Check if species candidates exist
        if not state.get('species_candidates') or len(state['species_candidates']) == 0:
            return {"error": "No species identification available"}
        
        # Extract species info
        species_info = state['species_candidates'][-1]
        scientific_name = species_info['scientific_name']
        
        # Get dynamic auction data
        auction_data = get_dynamic_auction_data(scientific_name)
        
        return {"auction_data": auction_data}
    
    except Exception as e:
        return {"error": f"Auction data generation failed: {str(e)}"}


async def synthesis_node(state: FloraState) -> Dict:
    """
    Node 4: Create professional FloraHolland market report
    
    Args:
        state: Complete graph state
        
    Returns:
        Final market intelligence report
    """
    try:
        # Validate required data
        if not state.get('visual_description') or len(state['visual_description']) == 0:
            return {"error": "No visual description available"}
        
        if not state.get('species_candidates') or len(state['species_candidates']) == 0:
            return {"error": "No species identification available"}
        
        if not state.get('auction_data'):
            return {"error": "No auction data available"}
        
        visual_desc = state['visual_description'][-1]['description']
        species_info = state['species_candidates'][-1]
        auction_data = state['auction_data']
        
        prompt = f"""Create a professional FloraHolland market intelligence report.

DATA AVAILABLE:

VISUAL ANALYSIS:
{visual_desc}

SPECIES IDENTIFICATION:
{json.dumps(species_info, indent=2)}

AUCTION DATA:
{json.dumps(auction_data, indent=2)}

REPORT STRUCTURE:

# BOTANICAL IDENTITY
[Scientific name, common name, family, confidence level]

# ORIGIN & CULTIVATION
[Native region, growing conditions, harvest indicators]

# QUALITY ASSESSMENT
[Current grade: {auction_data['quality_grade']}, freshness: {auction_data['freshness_days']} days]
[Visual quality indicators from analysis]

# MARKET INTELLIGENCE
[Current price: €{auction_data['auction_price_eur']}/stem]
[Price trend: {auction_data['price_trend']}]
[Daily volume: {auction_data['daily_volume_stems']} stems]
[Key buyers: {', '.join(auction_data['buyer_countries'])}]

# CARE INSTRUCTIONS
[Storage temperature, water requirements, shelf life optimization]

Write professionally for wholesale flower buyers at FloraHolland."""
        
        report = openrouter_client.generate(
            prompt,
            system_prompt="You are FloraHolland's AI market analyst.",
            temperature=0.7
        )
        
        return {"final_response": report}  # ← FIXED: Added return statement
    
    except Exception as e:
        return {"error": f"Report synthesis failed: {str(e)}"}  # ← FIXED: Added return statement