from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime, date
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.upload_time_service import UploadTimeService
from config import settings

router = APIRouter()

# Pydantic 모델 정의
class UploadTimeResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: str

# 업로드 시간 서비스 인스턴스
upload_time_service = UploadTimeService()

@router.get("/recommend", response_model=UploadTimeResponse)
async def recommend_upload_time(
    content_type: str = Query(default="general", description="콘텐츠 타입 (general, entertainment, education, gaming)")
):
    """
    동영상 업로드 시간 추천 (GET 요청)
    
    서버에서 자동으로 현재 날짜를 확인하여 최적의 업로드 시간을 추천합니다.
    사용자는 아무것도 입력할 필요가 없습니다.
    
    - **content_type**: 콘텐츠 타입 (선택사항, 기본값: general)
    """
    try:
        # 서버에서 현재 날짜 자동 확인
        target_date = date.today()
        
        print(f"📅 업로드 시간 추천 요청 (자동 날짜): {target_date}")
        print(f"📺 콘텐츠 타입: {content_type}")
        
        # 업로드 시간 추천 서비스 호출
        recommendation = await upload_time_service.get_upload_time_recommendation(
            target_date=target_date,
            content_type=content_type
        )
        
        print("✅ 업로드 시간 추천 완료")
        
        return UploadTimeResponse(
            success=True,
            data={
                "date": target_date.isoformat(),
                "dayName": target_date.strftime('%Y년 %m월 %d일 %A'),
                "contentType": content_type,
                "recommendation": recommendation,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as error:
        print(f"❌ 업로드 시간 추천 오류: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"업로드 시간 추천 중 오류가 발생했습니다: {str(error)}"
        )

@router.get("/weekly-recommend", response_model=UploadTimeResponse)
async def recommend_weekly_upload_time(
    content_type: str = Query(default="general", description="콘텐츠 타입 (general, entertainment, education, gaming)")
):
    """
    주간 동영상 업로드 시간 추천 (GET 요청)
    
    서버에서 자동으로 현재 날짜를 기준으로 7일간의 업로드 시간을 추천합니다.
    사용자는 아무것도 입력할 필요가 없습니다.
    
    - **content_type**: 콘텐츠 타입 (선택사항, 기본값: general)
    """
    try:
        # 서버에서 현재 날짜를 주간 시작점으로 자동 설정
        week_start = date.today()
        
        print(f"📅 주간 업로드 시간 추천 요청 (자동 날짜): {week_start}")
        print(f"📺 콘텐츠 타입: {content_type}")
        
        # 주간 추천 서비스 호출
        weekly_recommendation = await upload_time_service.get_weekly_upload_recommendation(
            start_date=week_start,
            content_type=content_type
        )
        
        print("✅ 주간 업로드 시간 추천 완료")
        
        return UploadTimeResponse(
            success=True,
            data={
                "weekStart": week_start.isoformat(),
                "weekStartName": week_start.strftime('%Y년 %m월 %d일 %A'),
                "contentType": content_type,
                "weeklyRecommendation": weekly_recommendation,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as error:
        print(f"❌ 주간 업로드 시간 추천 오류: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"주간 업로드 시간 추천 중 오류가 발생했습니다: {str(error)}"
        )

@router.get("/stats", response_model=UploadTimeResponse)
async def get_upload_time_stats(
    content_type: str = Query(default="general", description="콘텐츠 타입")
):
    """
    업로드 시간 통계 조회
    
    - **content_type**: 콘텐츠 타입 (general, entertainment, education, gaming)
    """
    try:
        print(f"📊 업로드 시간 통계 조회: {content_type}")
        
        stats = await upload_time_service.get_upload_time_stats(content_type)
        
        print("✅ 업로드 시간 통계 조회 완료")
        
        return UploadTimeResponse(
            success=True,
            data={
                "contentType": content_type,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as error:
        print(f"❌ 업로드 시간 통계 조회 오류: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"업로드 시간 통계 조회 중 오류가 발생했습니다: {str(error)}"
        )
