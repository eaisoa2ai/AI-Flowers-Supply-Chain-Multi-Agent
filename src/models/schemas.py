"""
Pydantic models for structured data
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BotanicalInfo(BaseModel):
    """Botanical information schema for Pydantic AI generation"""
    common_name: str = Field(..., description="Common English name")
    scientific_name: str = Field(..., description="Binomial nomenclature")
    family: str = Field(..., description="Plant family name")
    native_region: str = Field(..., description="Geographic origin")
    description: str = Field(..., description="Botanical description (150-200 words)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "common_name": "Pink Primrose",
                "scientific_name": "Primula vulgaris",
                "family": "Primulaceae",
                "native_region": "Western and Southern Europe",
                "description": "A detailed botanical description..."
            }
        }

class VisualFeatures(BaseModel):
    """Visual analysis from Gemini"""
    color_primary: str
    color_secondary: Optional[str] = None
    petal_count: str
    petal_arrangement: str
    leaf_shape: str
    size_estimate: str
    distinctive_features: List[str]
    
class SpeciesCandidate(BaseModel):
    """Species identification result"""
    scientific_name: str
    common_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    distinguishing_features: List[str]

class AuctionData(BaseModel):
    """FloraHolland auction intelligence"""
    species: str
    origin: str
    auction_price_eur: float
    price_trend: str
    volume_stems: int
    quality_grade: str
    freshness_days: int
    last_updated: datetime
    buyer_countries: List[str]

class MarketReport(BaseModel):
    """Final market intelligence report"""
    botanical_identity: dict
    origin_cultivation: dict
    quality_assessment: dict
    market_intelligence: dict
    care_instructions: dict