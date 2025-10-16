from typing import Dict, Any, Optional, List
from datetime import date, datetime, timedelta
import sys
import os
import re

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.openai_service import OpenAIService
from config import settings

class UploadTimeService:
    def __init__(self):
        """업로드 시간 서비스 초기화"""
        self.openai_service = OpenAIService()
        
        # 한국의 명절 및 특별한 날짜 정보
        self.korean_holidays = {
            # 2024년 명절
            '2024-01-01': {'name': '신정', 'type': 'holiday'},
            '2024-02-09': {'name': '설날 연휴', 'type': 'holiday'},
            '2024-02-10': {'name': '설날', 'type': 'holiday'},
            '2024-02-11': {'name': '설날 연휴', 'type': 'holiday'},
            '2024-02-12': {'name': '설날 연휴', 'type': 'holiday'},
            '2024-04-10': {'name': '국회의원선거', 'type': 'election'},
            '2024-05-05': {'name': '어린이날', 'type': 'holiday'},
            '2024-05-15': {'name': '부처님오신날', 'type': 'holiday'},
            '2024-06-06': {'name': '현충일', 'type': 'holiday'},
            '2024-08-15': {'name': '광복절', 'type': 'holiday'},
            '2024-09-16': {'name': '추석 연휴', 'type': 'holiday'},
            '2024-09-17': {'name': '추석', 'type': 'holiday'},
            '2024-09-18': {'name': '추석 연휴', 'type': 'holiday'},
            '2024-10-03': {'name': '개천절', 'type': 'holiday'},
            '2024-10-09': {'name': '한글날', 'type': 'holiday'},
            '2024-12-25': {'name': '크리스마스', 'type': 'holiday'},
            
            # 2025년 명절
            '2025-01-01': {'name': '신정', 'type': 'holiday'},
            '2025-01-28': {'name': '설날 연휴', 'type': 'holiday'},
            '2025-01-29': {'name': '설날', 'type': 'holiday'},
            '2025-01-30': {'name': '설날 연휴', 'type': 'holiday'},
            '2025-05-05': {'name': '어린이날', 'type': 'holiday'},
            '2025-05-15': {'name': '부처님오신날', 'type': 'holiday'},
            '2025-06-06': {'name': '현충일', 'type': 'holiday'},
            '2025-08-15': {'name': '광복절', 'type': 'holiday'},
            '2025-10-05': {'name': '추석 연휴', 'type': 'holiday'},
            '2025-10-06': {'name': '추석', 'type': 'holiday'},
            '2025-10-07': {'name': '추석 연휴', 'type': 'holiday'},
            '2025-10-08': {'name': '추석 연휴', 'type': 'holiday'},
            '2025-10-03': {'name': '개천절', 'type': 'holiday'},
            '2025-10-09': {'name': '한글날', 'type': 'holiday'},
            '2025-12-25': {'name': '크리스마스', 'type': 'holiday'}
        }
        
        # 콘텐츠 타입별 피크 시간 정보
        self.content_type_peak_times = {
            'general': {
                'weekday': {'peak': '20:00-22:00', 'secondary': '12:00-14:00', 'late': '22:00-24:00'},
                'weekend': {'peak': '14:00-16:00', 'secondary': '20:00-22:00', 'late': '22:00-24:00'},
                'holiday': {'peak': '15:00-17:00', 'secondary': '20:00-22:00', 'late': '22:00-24:00'}
            },
            'entertainment': {
                'weekday': {'peak': '19:00-21:00', 'secondary': '12:00-14:00', 'late': '21:00-23:00'},
                'weekend': {'peak': '15:00-17:00', 'secondary': '19:00-21:00', 'late': '21:00-23:00'},
                'holiday': {'peak': '14:00-16:00', 'secondary': '19:00-21:00', 'late': '21:00-23:00'}
            },
            'education': {
                'weekday': {'peak': '20:00-22:00', 'secondary': '19:00-21:00', 'late': '22:00-24:00'},
                'weekend': {'peak': '10:00-12:00', 'secondary': '14:00-16:00', 'late': '20:00-22:00'},
                'holiday': {'peak': '14:00-16:00', 'secondary': '10:00-12:00', 'late': '20:00-22:00'}
            },
            'gaming': {
                'weekday': {'peak': '21:00-23:00', 'secondary': '19:00-21:00', 'late': '23:00-01:00'},
                'weekend': {'peak': '15:00-17:00', 'secondary': '20:00-22:00', 'late': '22:00-24:00'},
                'holiday': {'peak': '14:00-16:00', 'secondary': '20:00-22:00', 'late': '22:00-24:00'}
            }
        }

    def convert_24h_to_12h(self, hour: int) -> tuple[str, int]:
        """
        24시간 형식을 12시간 형식으로 변환합니다.
        
        Args:
            hour: 24시간 형식의 시간 (0-23)
            
        Returns:
            (오전/오후, 12시간 형식 시간) 튜플
        """
        if hour == 0:
            return "오전", 12
        elif hour < 12:
            return "오전", hour
        elif hour == 12:
            return "오후", 12
        else:
            return "오후", hour - 12

    def extract_time_from_text(self, text: str) -> Optional[str]:
        """
        텍스트에서 시간 정보를 추출합니다.
        
        Args:
            text: 시간이 포함된 텍스트
            
        Returns:
            추출된 시간 문자열 또는 None
        """
        try:
            # 다양한 시간 패턴 매칭 (우선순위 순서)
            time_patterns = [
                # 오후 6시, 오전 9시 (이미 오전/오후가 있는 경우)
                (r'(오전|오후)\s*(\d{1,2})시', lambda m: f"{m[0]} {m[1]}시"),
                # 오후 6-8시, 오전 9-11시
                (r'(오전|오후)\s*(\d{1,2})-(\d{1,2})시', lambda m: f"{m[0]} {m[1]}-{m[2]}시"),
                # 오후 6시경, 오전 9시경
                (r'(오전|오후)\s*(\d{1,2})시경', lambda m: f"{m[0]} {m[1]}시경"),
                # 오후 6시~8시, 오전 9시~11시
                (r'(오전|오후)\s*(\d{1,2})시~(\d{1,2})시', lambda m: f"{m[0]} {m[1]}시~{m[2]}시"),
                # 18:00, 20:30 (24시간 형식)
                (r'(\d{1,2}):(\d{2})', lambda m: self._convert_time_format(m[0], m[1])),
                # 18시, 20시 (24시간 형식)
                (r'(\d{1,2})시', lambda m: self._convert_single_hour(m[0])),
                # 6-8시, 18-20시 (시간 범위)
                (r'(\d{1,2})-(\d{1,2})시', lambda m: self._convert_time_range(m[0], m[1])),
                # 6시경, 18시경
                (r'(\d{1,2})시경', lambda m: self._convert_single_hour(m[0]) + "경"),
                # 6시~8시, 18시~20시
                (r'(\d{1,2})시~(\d{1,2})시', lambda m: self._convert_time_range(m[0], m[1], "~"))
            ]
            
            for pattern, formatter in time_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    match = matches[0]
                    if isinstance(match, tuple):
                        return formatter(match)
                    else:
                        return formatter([match])
            
            return None
            
        except Exception as error:
            print(f"시간 추출 오류: {error}")
            return None

    def _convert_time_format(self, hour_str: str, min_str: str) -> str:
        """시간:분 형식을 오전/오후 형식으로 변환"""
        hour = int(hour_str)
        period, hour_12 = self.convert_24h_to_12h(hour)
        return f"{period} {hour_12}시{min_str}분"

    def _convert_single_hour(self, hour_str: str) -> str:
        """단일 시간을 오전/오후 형식으로 변환"""
        hour = int(hour_str)
        period, hour_12 = self.convert_24h_to_12h(hour)
        return f"{period} {hour_12}시"

    def _convert_time_range(self, start_hour_str: str, end_hour_str: str, separator: str = "-") -> str:
        """시간 범위를 오전/오후 형식으로 변환"""
        start_hour = int(start_hour_str)
        end_hour = int(end_hour_str)
        
        start_period, start_hour_12 = self.convert_24h_to_12h(start_hour)
        end_period, end_hour_12 = self.convert_24h_to_12h(end_hour)
        
        # 같은 오전/오후인 경우
        if start_period == end_period:
            return f"{start_period} {start_hour_12}{separator}{end_hour_12}시"
        else:
            # 다른 오전/오후인 경우
            return f"{start_period} {start_hour_12}시{separator}{end_period} {end_hour_12}시"

    def is_holiday(self, target_date: date) -> Optional[Dict[str, str]]:
        """
        날짜가 명절인지 확인
        
        Args:
            target_date: 확인할 날짜
            
        Returns:
            명절 정보 또는 None
        """
        date_str = target_date.isoformat()
        return self.korean_holidays.get(date_str)

    def get_day_type(self, target_date: date) -> str:
        """
        요일 타입 결정 (weekday, weekend, holiday)
        
        Args:
            target_date: 확인할 날짜
            
        Returns:
            요일 타입
        """
        holiday = self.is_holiday(target_date)
        if holiday:
            return 'holiday'
        
        day_of_week = target_date.weekday()
        return 'weekend' if day_of_week >= 5 else 'weekday'

    async def get_upload_time_recommendation(
        self, 
        target_date: date, 
        content_type: str = 'general'
    ) -> Dict[str, Any]:
        """
        특정 날짜의 업로드 시간 추천
        
        Args:
            target_date: 분석할 날짜
            content_type: 콘텐츠 타입
            
        Returns:
            업로드 시간 추천 정보 (텍스트와 추출된 시간 포함)
        """
        try:
            day_type = self.get_day_type(target_date)
            holiday = self.is_holiday(target_date)
            date_str = target_date.isoformat()
            day_name = target_date.strftime('%Y년 %m월 %d일 %A')

            # 기본 피크 시간 정보
            peak_times = self.content_type_peak_times.get(content_type, self.content_type_peak_times['general'])
            current_peak_times = peak_times[day_type]

            # 간결한 프롬프트 작성
            prompt = f"""현재 날짜: {day_name} ({date_str})
콘텐츠 타입: {content_type}
요일 타입: {day_type}
{('특별한 날: ' + holiday['name']) if holiday else ''}

한국의 일반적인 동영상 시청 패턴:
- 평일: 저녁 8-10시가 피크, 점심 12-2시가 보조 피크
- 주말: 오후 2-4시가 피크, 저녁 8-10시가 보조 피크  
- 명절/휴일: 오후 3-5시가 피크, 저녁 8-10시가 보조 피크

위 정보를 바탕으로 한 줄로 간결하게 업로드 시간을 추천해주세요.

예시 형식: "보통 한국은 저녁 8~10시가 피크지만, 이번주는 명절이라 오후 3시에도 조회수가 급증할것으로 보입니다. 따라서 이번 주는 오후 3~5시 업로드를 추천드립니다."

반드시 한 줄로만 답변해주세요."""

            print("🤖 ChatGPT에 업로드 시간 추천 요청 중...")

            # ChatGPT API 호출
            response = await self.openai_service.chat_with_gpt(
                message=prompt,
                model=settings.DEFAULT_MODEL,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )

            # 응답에서 시간 추출
            recommendation_text = response["message"]
            extracted_time = self.extract_time_from_text(recommendation_text)
            
            return {
                "text": recommendation_text,
                "extractedTime": extracted_time
            }

        except Exception as error:
            print(f"업로드 시간 추천 서비스 오류: {error}")
            raise error

    async def get_weekly_upload_recommendation(
        self, 
        start_date: date, 
        content_type: str = 'general'
    ) -> Dict[str, Any]:
        """
        주간 업로드 시간 추천
        
        Args:
            start_date: 주간 시작 날짜
            content_type: 콘텐츠 타입
            
        Returns:
            주간 추천 정보
        """
        try:
            weekly_recommendations = []
            
            # 7일간의 추천 생성
            for i in range(7):
                current_date = start_date + timedelta(days=i)
                recommendation_data = await self.get_upload_time_recommendation(current_date, content_type)
                weekly_recommendations.append({
                    "date": current_date.isoformat(),
                    "dayName": current_date.strftime('%Y년 %m월 %d일 %A'),
                    "dayType": self.get_day_type(current_date),
                    "holiday": self.is_holiday(current_date),
                    "recommendation": recommendation_data["text"],
                    "extractedTime": recommendation_data["extractedTime"]
                })

            # 주간 전체 분석을 위한 프롬프트
            week_dates = [r["date"] for r in weekly_recommendations]
            holidays = [r["holiday"]["name"] for r in weekly_recommendations if r["holiday"]]
            
            weekly_prompt = f"""분석 기간: {', '.join(week_dates)}
콘텐츠 타입: {content_type}
{('포함된 명절/특별한 날: ' + ', '.join(holidays)) if holidays else ''}

이 주간의 동영상 업로드 전략을 한 줄로 간결하게 추천해주세요.

예시 형식: "이번 주는 명절 연휴가 포함되어 있어 평소보다 오후 시간대 시청이 증가할 것으로 예상됩니다. 따라서 오후 3~5시 업로드를 추천드립니다."

반드시 한 줄로만 답변해주세요."""

            weekly_analysis = await self.openai_service.chat_with_gpt(
                message=weekly_prompt,
                model=settings.DEFAULT_MODEL,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )

            # 주간 분석에서도 시간 추출
            weekly_analysis_text = weekly_analysis["message"]
            weekly_extracted_time = self.extract_time_from_text(weekly_analysis_text)

            return {
                "weekStart": start_date.isoformat(),
                "contentType": content_type,
                "dailyRecommendations": weekly_recommendations,
                "weeklyAnalysis": {
                    "text": weekly_analysis_text,
                    "extractedTime": weekly_extracted_time
                },
                "summary": {
                    "totalDays": 7,
                    "holidayDays": len(holidays),
                    "weekendDays": len([r for r in weekly_recommendations if r["dayType"] == "weekend"]),
                    "weekdayDays": len([r for r in weekly_recommendations if r["dayType"] == "weekday"])
                }
            }

        except Exception as error:
            print(f"주간 업로드 시간 추천 서비스 오류: {error}")
            raise error

    async def get_upload_time_stats(self, content_type: str = 'general') -> Dict[str, Any]:
        """
        업로드 시간 통계 조회
        
        Args:
            content_type: 콘텐츠 타입
            
        Returns:
            업로드 시간 통계
        """
        try:
            stats = {
                "contentType": content_type,
                "peakTimes": self.content_type_peak_times.get(content_type, self.content_type_peak_times['general']),
                "generalStats": {
                    "averagePeakTime": "20:00-22:00",
                    "secondaryPeakTime": "12:00-14:00",
                    "lateNightTime": "22:00-24:00",
                    "weekendShift": "14:00-16:00",
                    "holidayShift": "15:00-17:00"
                },
                "recommendations": {
                    "bestUploadDays": ["화요일", "수요일", "목요일"],
                    "avoidDays": ["월요일", "금요일"],
                    "holidayStrategy": "명절 전후 3일간은 오후 시간대 집중",
                    "weekendStrategy": "주말은 오후 시간대가 더 효과적"
                }
            }

            return stats

        except Exception as error:
            print(f"업로드 시간 통계 조회 오류: {error}")
            raise error
