import openai
from typing import List, Dict, Any, Optional
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

class OpenAIService:
    def __init__(self):
        """OpenAI 서비스 초기화"""
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        self.default_model = settings.DEFAULT_MODEL
        self.fallback_model = settings.FALLBACK_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    async def chat_with_gpt(
        self, 
        message: str, 
        model: Optional[str] = None, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        ChatGPT와 단일 메시지로 대화
        
        Args:
            message: 사용자 메시지
            model: 사용할 모델 (기본값: gpt-4o)
            max_tokens: 최대 토큰 수 (기본값: 4000)
            temperature: 온도 설정 (기본값: 0.7)
            
        Returns:
            ChatGPT 응답 딕셔너리
        """
        try:
            print("OpenAI API 호출 시작...")
            
            # 기본값 설정
            model = model or self.default_model
            max_tokens = max_tokens or self.max_tokens
            temperature = temperature or self.temperature
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            response = completion.choices[0].message.content
            usage = completion.usage

            print("OpenAI API 응답 완료")
            print(f"사용된 토큰: {usage}")

            return {
                "message": response,
                "model": model,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                }
            }

        except Exception as error:
            print(f"OpenAI API 오류: {error}")
            raise error

    async def chat_with_history(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        ChatGPT와 대화 히스토리와 함께 대화
        
        Args:
            messages: 대화 히스토리 배열 [{"role": "user", "content": "..."}, ...]
            model: 사용할 모델 (기본값: gpt-4o)
            max_tokens: 최대 토큰 수 (기본값: 4000)
            temperature: 온도 설정 (기본값: 0.7)
            
        Returns:
            ChatGPT 응답 딕셔너리
        """
        try:
            print("OpenAI API 호출 시작 (대화 히스토리 포함)...")
            
            # 기본값 설정
            model = model or self.default_model
            max_tokens = max_tokens or self.max_tokens
            temperature = temperature or self.temperature
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            response = completion.choices[0].message.content
            usage = completion.usage

            print("OpenAI API 응답 완료")
            print(f"사용된 토큰: {usage}")

            return {
                "message": response,
                "model": model,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                }
            }

        except Exception as error:
            print(f"OpenAI API 오류: {error}")
            raise error

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        사용 가능한 모델 목록 조회
        
        Returns:
            사용 가능한 모델 목록
        """
        try:
            print("사용 가능한 모델 목록 조회 중...")
            
            models = self.client.models.list()
            available_models = []
            
            for model in models.data:
                if 'gpt' in model.id:
                    available_models.append({
                        "id": model.id,
                        "name": model.id,
                        "created": model.created
                    })

            print(f"모델 목록 조회 완료: {len(available_models)}개 모델")

            return available_models

        except Exception as error:
            print(f"모델 목록 조회 오류: {error}")
            raise error

    async def generate_image(
        self, 
        prompt: str, 
        size: str = "1024x1024", 
        n: int = 1
    ) -> Dict[str, Any]:
        """
        이미지 생성 (DALL-E)
        
        Args:
            prompt: 이미지 생성 프롬프트
            size: 이미지 크기 (기본값: 1024x1024)
            n: 생성할 이미지 수 (기본값: 1)
            
        Returns:
            생성된 이미지 정보
        """
        try:
            print("이미지 생성 시작...")
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=n,
                quality="standard",
                response_format="url"
            )

            print("이미지 생성 완료")

            return {
                "images": [
                    {
                        "url": img.url,
                        "revised_prompt": img.revised_prompt
                    } for img in response.data
                ],
                "model": "dall-e-3"
            }

        except Exception as error:
            print(f"이미지 생성 오류: {error}")
            raise error

    async def create_embedding(
        self, 
        text: str, 
        model: str = "text-embedding-ada-002"
    ) -> Dict[str, Any]:
        """
        텍스트 임베딩 생성
        
        Args:
            text: 임베딩할 텍스트
            model: 사용할 모델 (기본값: text-embedding-ada-002)
            
        Returns:
            임베딩 벡터
        """
        try:
            print("텍스트 임베딩 생성 시작...")
            
            response = self.client.embeddings.create(
                model=model,
                input=text
            )

            print("텍스트 임베딩 생성 완료")

            return {
                "embedding": response.data[0].embedding,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

        except Exception as error:
            print(f"텍스트 임베딩 생성 오류: {error}")
            raise error
