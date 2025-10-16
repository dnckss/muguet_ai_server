import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class Settings:
    # OpenAI API 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o")
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "gpt-4o-mini")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # 서버 설정
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS 설정
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3001")

# 전역 설정 인스턴스
settings = Settings()
