"""
LangGraph state definition
"""
from typing import TypedDict, Annotated, List
import operator

class FloraState(TypedDict):
    """
    State object passed between LangGraph nodes
    
    State accumulates information as it flows through:
    vision → species_id → auction → synthesis
    """
    
    # Input
    image_path: str
    
    # Node 1: Vision Analysis
    visual_description: Annotated[List[dict], operator.add]
    
    # Node 2: Species Identification
    species_candidates: Annotated[List[dict], operator.add]
    
    # Node 3: Auction Intelligence
    auction_data: dict
    
    # Node 4: Final Report
    final_response: str
    
    # Error Handling
    error: str