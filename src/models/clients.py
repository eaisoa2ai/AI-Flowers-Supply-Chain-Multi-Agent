"""
API clients for Gemini and OpenRouter
"""
import google.generativeai as genai
from openai import OpenAI
from typing import Optional
from PIL import Image
from src.config import settings

class GeminiClient:
    """Wrapper for Google Gemini API"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.VISION_MODEL)
    
    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        Analyze image with Gemini
        
        Args:
            image_path: Path to image file
            prompt: Analysis prompt
            
        Returns:
            Analysis text
        """
        img = Image.open(image_path)
        response = self.model.generate_content([prompt, img])
        return response.text

class OpenRouterClient:
    """Wrapper for OpenRouter API (DeepSeek)"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL
        )
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate text with DeepSeek
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=settings.REASONING_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_headers={
                "HTTP-Referer": settings.OPENROUTER_APP_NAME,
                "X-Title": "FloraHolland AI Agent"
            }
        )
        
        return response.choices[0].message.content

# Global instances
gemini_client = GeminiClient()
openrouter_client = OpenRouterClient()