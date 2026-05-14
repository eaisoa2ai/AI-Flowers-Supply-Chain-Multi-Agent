"""
Configuration management for FloraHolland AI Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

# Load environment variables from MyAPIKeys.env
env_path = Path(__file__).parent.parent / "MyAPIKeys.env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """Application settings"""
    
    # Required API Keys for this project
    GEMINI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Model Configuration
    VISION_MODEL: str = "gemini-3-pro-preview"
    REASONING_MODEL: str = "deepseek/deepseek-chat"
    DATA_GEN_MODEL: str = "openai:gpt-4o-mini"
    IMAGE_GEN_MODEL: str = "gpt-image-1.5"
    
    # Gemini 3 Pro Vision Settings
    MEDIA_RESOLUTION: str = "high"
    THINKING_LEVEL: str = "high"
    
    # OpenRouter Config
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_APP_NAME: str = "FloraHolland-AI"
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    AUCTION_DATA_DIR: Path = DATA_DIR / "auction"
    FLORA_IMAGES_DIR: Path = PROJECT_ROOT / "flora_images"
    
    # ChromaDB
    CHROMA_PERSIST_DIR: Path = PROJECT_ROOT / "flora_db"
    CHROMA_COLLECTION_NAME: str = "botanical_taxonomy"
    
    # Agent Settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2048
    
    model_config = ConfigDict(
        env_file="MyAPIKeys.env",
        case_sensitive=True,
        extra='ignore'  # THIS IS THE FIX - ignore extra env vars
    )
    
    def validate_keys(self):
        """Ensure required API keys are present"""
        missing_keys = []
        
        if not self.GEMINI_API_KEY:
            missing_keys.append("GEMINI_API_KEY")
        if not self.OPENROUTER_API_KEY:
            missing_keys.append("OPENROUTER_API_KEY")
        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        
        if missing_keys:
            raise ValueError(
                f"Missing API keys in MyAPIKeys.env: {', '.join(missing_keys)}\n"
                f"Required keys: GEMINI_API_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY"
            )
        
        print(f"✅ All API keys loaded from: {env_path}")
    
    def setup_directories(self):
        """Create necessary directories"""
        for dir_path in [
            self.DATA_DIR,
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.AUCTION_DATA_DIR,
            self.FLORA_IMAGES_DIR,
            self.CHROMA_PERSIST_DIR
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()

# Validate on import
settings.validate_keys()
settings.setup_directories()