"""
LangGraph workflow construction
"""
from langgraph.graph import StateGraph, END
from src.agents.state import FloraState
from src.agents.nodes import (
    vision_node,
    species_identification_node,
    auction_intelligence_node,
    synthesis_node
)

def create_flora_agent():
    """
    Build the complete LangGraph workflow
    
    Returns:
        Compiled graph
    """
    
    # Initialize graph
    workflow = StateGraph(FloraState)
    
    # Add nodes
    workflow.add_node("vision", vision_node)
    workflow.add_node("identify_species", species_identification_node)
    workflow.add_node("auction_intel", auction_intelligence_node)
    workflow.add_node("synthesize", synthesis_node)
    
    # Define edges (linear flow)
    workflow.set_entry_point("vision")
    workflow.add_edge("vision", "identify_species")
    workflow.add_edge("identify_species", "auction_intel")
    workflow.add_edge("auction_intel", "synthesize")
    workflow.add_edge("synthesize", END)
    
    # Compile
    return workflow.compile()

# Create global agent instance
flora_agent = create_flora_agent()