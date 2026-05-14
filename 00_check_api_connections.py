"""
Quick API connection checker - verify all keys work before running demo
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
import google.generativeai as genai
from openai import OpenAI
import httpx


def check_apis():
    """Check all API connections"""
    print("\n🔧 Checking API Connections...\n")
    
    all_good = True
    
    # Gemini
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        list(genai.list_models())
        print("✅ Gemini API")
    except Exception as e:
        print(f"❌ Gemini API: {e}")
        all_good = False
    
    # OpenAI
    try:
        OpenAI(api_key=settings.OPENAI_API_KEY).models.list()
        print("✅ OpenAI API")
    except Exception as e:
        print(f"❌ OpenAI API: {e}")
        all_good = False
    
    # OpenRouter
    try:
        response = httpx.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}"},
            timeout=10.0
        )
        if response.status_code == 200:
            print("✅ OpenRouter API")
        else:
            print(f"❌ OpenRouter API: Status {response.status_code}")
            all_good = False
    except Exception as e:
        print(f"❌ OpenRouter API: {e}")
        all_good = False
    
    print()
    if all_good:
        print("✅ All APIs working! Ready to run:")
        print("   python scripts/demo_complete_workflow.py\n")
        return True
    else:
        print("❌ Fix API keys in MyAPIKeys.env\n")
        return False


if __name__ == "__main__":
    sys.exit(0 if check_apis() else 1)