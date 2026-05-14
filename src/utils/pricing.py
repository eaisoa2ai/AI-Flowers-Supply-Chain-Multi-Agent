"""
Dynamic auction pricing simulation for FloraHolland
"""
import random
from datetime import datetime
from typing import Dict

# Base price ranges by plant family (€ per stem)
FAMILY_PRICE_RANGES = {
    'Rosaceae': (0.35, 0.95),
    'Orchidaceae': (1.20, 3.50),
    'Liliaceae': (0.45, 1.20),
    'Asteraceae': (0.15, 0.40),
    'Iridaceae': (0.25, 0.65),
    'Ranunculaceae': (0.30, 0.70),
    'Primulaceae': (0.20, 0.50),
    'Default': (0.20, 0.60)
}

# Origin patterns by family
FAMILY_ORIGINS = {
    'Rosaceae': ['Kenya', 'Ecuador', 'Colombia', 'Ethiopia'],
    'Orchidaceae': ['Thailand', 'Netherlands', 'Taiwan', 'Colombia'],
    'Liliaceae': ['Netherlands', 'Israel', 'New Zealand', 'South Africa'],
    'Iridaceae': ['Netherlands', 'South Africa', 'France'],
    'Default': ['Netherlands', 'Kenya', 'Colombia', 'Ecuador']
}

def get_dynamic_auction_data(scientific_name: str, family: str = 'Default') -> Dict:
    """
    Generate realistic FloraHolland auction data with dynamic pricing
    
    Args:
        scientific_name: Scientific name of the species
        family: Plant family
        
    Returns:
        Dictionary with auction data including dynamic pricing
    """
    
    # Get base price range
    base_min, base_max = FAMILY_PRICE_RANGES.get(family, FAMILY_PRICE_RANGES['Default'])
    
    # DYNAMIC PRICING FACTORS
    hour = datetime.now().hour
    day_of_week = datetime.now().weekday()
    month = datetime.now().month
    day = datetime.now().day
    
    # 1. Time-of-day multiplier (morning auction peak)
    time_multiplier = 1.2 if 6 <= hour <= 9 else 0.95 if 14 <= hour <= 17 else 1.0
    
    # 2. Weekend premium
    weekend_multiplier = 1.15 if day_of_week >= 5 else 1.08 if day_of_week == 4 else 1.0
    
    # 3. Seasonal demand
    seasonal_multiplier = 1.0
    if month == 2 and 10 <= day <= 14:  # Valentine's
        seasonal_multiplier = 1.5
    elif month == 5 and 1 <= day <= 10:  # Mother's Day
        seasonal_multiplier = 1.4
    elif month == 12 and 15 <= day <= 25:  # Christmas
        seasonal_multiplier = 1.25
    
    # 4. Market volatility
    volatility = random.uniform(0.85, 1.15)
    
    # 5. Quality grade
    quality_grade = random.choices(
        ['A1', 'A2', 'B1', 'B2'],
        weights=[0.3, 0.4, 0.2, 0.1]
    )[0]
    quality_multipliers = {'A1': 1.15, 'A2': 1.0, 'B1': 0.9, 'B2': 0.8}
    quality_multiplier = quality_multipliers[quality_grade]
    
    # Calculate final price
    base_price = random.uniform(base_min, base_max)
    final_price = base_price * time_multiplier * weekend_multiplier * seasonal_multiplier * volatility * quality_multiplier
    
    # Price trend
    trend_change = (final_price - base_price) / base_price * 100
    trend_direction = "↑" if trend_change > 0 else "↓"
    price_trend = f"{trend_direction} {abs(trend_change):.1f}% vs 30-day avg"
    
    # Origin and buyers
    origins = FAMILY_ORIGINS.get(family, FAMILY_ORIGINS['Default'])
    origin = random.choice(origins)
    all_buyers = ['Germany', 'France', 'UK', 'Italy', 'Spain', 'Poland', 'Belgium']
    buyer_countries = random.sample(all_buyers, k=random.randint(3, 5))
    
    return {
    'species': scientific_name,
    'origin': origin,
    'auction_price_eur': round(final_price, 2),
    'price_trend': price_trend,
    'daily_volume_stems': random.randint(5000, 50000),  # ← CHANGED from volume_stems
    'quality_grade': quality_grade,
    'freshness_days': random.randint(5, 12),
    'last_updated': datetime.now().isoformat(),
    'buyer_countries': buyer_countries
}