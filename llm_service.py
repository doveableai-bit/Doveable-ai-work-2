import os
from typing import Optional, Dict, Any, List
from openai import OpenAI
from groq import Groq
import google.generativeai as genai

class LLMService:
    def __init__(self):
        self.emergent_key = os.getenv("EMERGENT_LLM_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.groq_client = None
        self.openai_client = None
        self.emergent_client = None
        
        if self.groq_key:
            self.groq_client = Groq(api_key=self.groq_key)
        
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        
        if self.emergent_key:
            self.emergent_client = OpenAI(
                api_key=self.emergent_key,
                base_url="https://api.emergentmethods.ai/v1"
            )
        
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
    
    async def generate_with_groq(
        self,
        prompt: str,
        model: str = "mixtral-8x7b-32768",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        if not self.groq_client:
            raise ValueError("Groq API key not configured")
        
        try:
            completion = self.groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    async def generate_with_openai(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            completion = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_with_emergent(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        if not self.emergent_client:
            raise ValueError("Emergent LLM API key not configured")
        
        try:
            completion = self.emergent_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Emergent LLM API error: {str(e)}")
    
    async def generate_with_gemini(
        self,
        prompt: str,
        model: str = "gemini-pro",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        if not self.gemini_key:
            raise ValueError("Google Gemini API key not configured")
        
        try:
            model_instance = genai.GenerativeModel(model)
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            response = model_instance.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def generate(
        self,
        prompt: str,
        provider: str = "auto",
        model: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        if provider == "auto":
            if self.groq_client:
                provider = "groq"
            elif self.gemini_key:
                provider = "gemini"
            elif self.emergent_client:
                provider = "emergent"
            elif self.openai_client:
                provider = "openai"
            else:
                raise ValueError("No LLM provider configured")
        
        try:
            if provider == "groq":
                model = model or "mixtral-8x7b-32768"
                response = await self.generate_with_groq(prompt, model, max_tokens, temperature)
            elif provider == "gemini":
                model = model or "gemini-pro"
                response = await self.generate_with_gemini(prompt, model, max_tokens, temperature)
            elif provider == "emergent":
                model = model or "gpt-3.5-turbo"
                response = await self.generate_with_emergent(prompt, model, max_tokens, temperature)
            elif provider == "openai":
                model = model or "gpt-3.5-turbo"
                response = await self.generate_with_openai(prompt, model, max_tokens, temperature)
            else:
                raise ValueError(f"Unknown provider: {provider}")
            
            return {
                "success": True,
                "response": response,
                "provider": provider,
                "model": model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": provider
            }
    
    def get_available_providers(self) -> List[str]:
        providers = []
        if self.groq_client:
            providers.append("groq")
        if self.gemini_key:
            providers.append("gemini")
        if self.emergent_client:
            providers.append("emergent")
        if self.openai_client:
            providers.append("openai")
        return providers
