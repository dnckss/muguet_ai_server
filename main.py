from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from routers import chat, upload_time

# FastAPI 앱 생성
app = FastAPI(
    title="ChatGPT API 서버",
    description="OpenAI ChatGPT API를 사용한 동영상 업로드 시간 추천 서비스",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:3001", "https://www.muguet.cloud"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(upload_time.router, prefix="/api/upload-time", tags=["upload-time"])

@app.get("/", response_class=JSONResponse)
async def root():
    """기본 엔드포인트"""
    return {
        "message": "ChatGPT API 서버가 실행 중입니다!",
        "endpoints": {
            "chat": "/api/chat/message",
            "uploadTime": "/api/upload-time/recommend",
            "weeklyUploadTime": "/api/upload-time/weekly-recommend",
            "uploadStats": "/api/upload-time/stats",
            "health": "/health",
            "docs": "/docs"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": "development" if settings.DEBUG else "production"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 예외 처리"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """일반 예외 처리"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "서버 내부 오류가 발생했습니다.",
            "message": str(exc) if settings.DEBUG else "알 수 없는 오류가 발생했습니다.",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    print("🚀 FastAPI 서버를 시작합니다...")
    print(f"📡 서버 주소: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API 문서: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"⏰ 업로드 시간 추천: http://{settings.HOST}:{settings.PORT}/api/upload-time/recommend")
    print(f"📅 주간 업로드 시간 추천: http://{settings.HOST}:{settings.PORT}/api/upload-time/weekly-recommend")
    print(f"📊 업로드 통계: http://{settings.HOST}:{settings.PORT}/api/upload-time/stats")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
