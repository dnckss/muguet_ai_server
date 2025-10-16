from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import OpenAIService
from config import settings

router = APIRouter()

# Pydantic 모델 정의
class ChatMessage(BaseModel):
    message: str = Field(..., description="사용자 메시지", min_length=1, max_length=4000)
    model: Optional[str] = Field(default=settings.DEFAULT_MODEL, description="사용할 GPT 모델")
    max_tokens: Optional[int] = Field(default=settings.MAX_TOKENS, description="최대 토큰 수", ge=1, le=8000)
    temperature: Optional[float] = Field(default=settings.TEMPERATURE, description="온도 설정", ge=0.0, le=2.0)

class ConversationMessage(BaseModel):
    role: str = Field(..., description="메시지 역할 (user, assistant, system)")
    content: str = Field(..., description="메시지 내용", min_length=1, max_length=4000)

class ConversationRequest(BaseModel):
    messages: List[ConversationMessage] = Field(..., description="대화 히스토리", min_items=1)
    model: Optional[str] = Field(default=settings.DEFAULT_MODEL, description="사용할 GPT 모델")
    max_tokens: Optional[int] = Field(default=settings.MAX_TOKENS, description="최대 토큰 수", ge=1, le=8000)
    temperature: Optional[float] = Field(default=settings.TEMPERATURE, description="온도 설정", ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: str

# OpenAI 서비스 인스턴스
openai_service = OpenAIService()

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatMessage):
    """
    ChatGPT와 단일 메시지로 대화
    
    - **message**: 사용자 메시지 (필수)
    - **model**: 사용할 GPT 모델 (기본값: gpt-4o)
    - **max_tokens**: 최대 토큰 수 (기본값: 4000)
    - **temperature**: 온도 설정 (기본값: 0.7)
    """
    try:
        print(f"📨 받은 메시지: {request.message}")
        print(f"🤖 사용할 모델: {request.model}")
        
        # ChatGPT API 호출
        response = await openai_service.chat_with_gpt(
            message=request.message,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        print("✅ ChatGPT 응답 성공")
        
        return ChatResponse(
            success=True,
            data={
                "message": response["message"],
                "model": response["model"],
                "usage": response["usage"],
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as error:
        print(f"❌ ChatGPT API 오류: {error}")
        
        # OpenAI API 오류 처리
        if "insufficient_quota" in str(error).lower():
            raise HTTPException(
                status_code=402,
                detail="API 할당량이 부족합니다. OpenAI API 할당량을 확인해주세요."
            )
        
        if "invalid_api_key" in str(error).lower():
            raise HTTPException(
                status_code=401,
                detail="유효하지 않은 API 키입니다. OpenAI API 키를 확인해주세요."
            )
        
        if "rate_limit_exceeded" in str(error).lower():
            raise HTTPException(
                status_code=429,
                detail="API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
            )
        
        # 기타 오류
        raise HTTPException(
            status_code=500,
            detail=f"ChatGPT API 호출 중 오류가 발생했습니다: {str(error)}"
        )

@router.post("/conversation", response_model=ChatResponse)
async def chat_conversation(request: ConversationRequest):
    """
    대화 히스토리와 함께 ChatGPT와 대화
    
    - **messages**: 대화 히스토리 배열 (필수)
    - **model**: 사용할 GPT 모델 (기본값: gpt-4o)
    - **max_tokens**: 최대 토큰 수 (기본값: 4000)
    - **temperature**: 온도 설정 (기본값: 0.7)
    """
    try:
        print(f"📨 받은 대화: {len(request.messages)}개 메시지")
        print(f"🤖 사용할 모델: {request.model}")
        
        # 메시지 형식 검증
        for msg in request.messages:
            if msg.role not in ["user", "assistant", "system"]:
                raise HTTPException(
                    status_code=400,
                    detail="메시지 역할은 'user', 'assistant', 'system' 중 하나여야 합니다."
                )
        
        # ChatGPT API 호출 (대화 히스토리 포함)
        response = await openai_service.chat_with_history(
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        print("✅ ChatGPT 응답 성공")
        
        return ChatResponse(
            success=True,
            data={
                "message": response["message"],
                "model": response["model"],
                "usage": response["usage"],
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as error:
        print(f"❌ ChatGPT API 오류: {error}")
        
        # OpenAI API 오류 처리
        if "insufficient_quota" in str(error).lower():
            raise HTTPException(
                status_code=402,
                detail="API 할당량이 부족합니다. OpenAI API 할당량을 확인해주세요."
            )
        
        if "invalid_api_key" in str(error).lower():
            raise HTTPException(
                status_code=401,
                detail="유효하지 않은 API 키입니다. OpenAI API 키를 확인해주세요."
            )
        
        if "rate_limit_exceeded" in str(error).lower():
            raise HTTPException(
                status_code=429,
                detail="API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
            )
        
        # 기타 오류
        raise HTTPException(
            status_code=500,
            detail=f"ChatGPT API 호출 중 오류가 발생했습니다: {str(error)}"
        )

@router.get("/models", response_model=ChatResponse)
async def get_available_models():
    """
    사용 가능한 GPT 모델 목록 조회
    """
    try:
        print("📋 사용 가능한 모델 목록 조회 중...")
        
        models = await openai_service.get_available_models()
        
        print(f"✅ 모델 목록 조회 완료: {len(models)}개 모델")
        
        return ChatResponse(
            success=True,
            data={
                "models": models,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as error:
        print(f"❌ 모델 목록 조회 오류: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"모델 목록을 가져오는 중 오류가 발생했습니다: {str(error)}"
        )
