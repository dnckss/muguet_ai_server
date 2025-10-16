# ChatGPT API 서버 (FastAPI)

OpenAI의 ChatGPT API를 사용하여 동영상 업로드 시간을 추천하는 FastAPI 서버입니다.

## 🚀 시작하기

### 1. Python 환경 설정
```bash
# Python 3.8+ 필요
python --version

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here

# 서버 설정
PORT=8000
HOST=0.0.0.0
DEBUG=True

# CORS 설정
FRONTEND_URL=http://localhost:3001

# ChatGPT 모델 설정 (최고 성능)
DEFAULT_MODEL=gpt-4o
FALLBACK_MODEL=gpt-4o-mini

# API 설정
MAX_TOKENS=4000
TEMPERATURE=0.7
```

### 4. 서버 실행
```bash
# 개발 모드 (자동 재시작)
python main.py

# 또는 uvicorn 직접 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API 엔드포인트

### 1. 기본 메시지 전송
**POST** `/api/chat/message`

```json
{
  "message": "안녕하세요!",
  "model": "gpt-4o",
  "max_tokens": 4000,
  "temperature": 0.7
}
```

### 2. 대화 히스토리와 함께 대화
**POST** `/api/chat/conversation`

```json
{
  "messages": [
    {
      "role": "user",
      "content": "안녕하세요!"
    },
    {
      "role": "assistant", 
      "content": "안녕하세요! 무엇을 도와드릴까요?"
    },
    {
      "role": "user",
      "content": "오늘 날씨가 어때요?"
    }
  ],
  "model": "gpt-4o",
  "max_tokens": 4000
}
```

### 3. 사용 가능한 모델 목록 조회
**GET** `/api/chat/models`

### 4. 동영상 업로드 시간 추천 (GET 요청)
**GET** `/api/upload-time/recommend?content_type=general`

서버에서 자동으로 현재 날짜를 확인하여 최적의 업로드 시간을 추천합니다.
사용자는 아무것도 입력할 필요가 없습니다.

**쿼리 파라미터:**
- `content_type` (선택사항): 콘텐츠 타입 (general, entertainment, education, gaming)

**응답:**
```json
{
  "success": true,
  "data": {
    "date": "2024-01-15",
    "dayName": "2024년 01월 15일 Monday",
    "contentType": "general",
    "recommendation": "보통 한국은 저녁 8~10시가 피크지만, 이번주는 명절이라 오후 3시에도 조회수가 급증할것으로 보입니다. 따라서 이번 주는 오후 3~5시 업로드를 추천드립니다.",
    "timestamp": "2024-01-15T10:30:00.000000"
  },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

### 5. 주간 업로드 시간 추천 (GET 요청)
**GET** `/api/upload-time/weekly-recommend?content_type=entertainment`

서버에서 자동으로 현재 날짜를 기준으로 7일간의 업로드 시간을 추천합니다.
사용자는 아무것도 입력할 필요가 없습니다.

**쿼리 파라미터:**
- `content_type` (선택사항): 콘텐츠 타입 (general, entertainment, education, gaming)

### 6. 업로드 시간 통계
**GET** `/api/upload-time/stats?content_type=general`

### 7. 헬스 체크
**GET** `/health`

## 🔧 설정

### 지원하는 모델 (최고 성능 순)
- `gpt-4o` (기본값) - 가장 최신이고 강력한 모델
- `gpt-4o-mini` - 빠르고 효율적인 모델
- `gpt-4-turbo` - 이전 최고 성능 모델
- `gpt-4` - 안정적인 고성능 모델
- `gpt-3.5-turbo` - 빠르고 경제적인 모델

### 콘텐츠 타입
- `general` - 일반 콘텐츠
- `entertainment` - 엔터테인먼트
- `education` - 교육 콘텐츠
- `gaming` - 게임 콘텐츠

### CORS 설정
프론트엔드 URL을 `.env` 파일의 `FRONTEND_URL`에 설정하면 CORS가 자동으로 구성됩니다.

## 🛠️ 개발

### 프로젝트 구조
```
server/
├── main.py                    # FastAPI 메인 애플리케이션
├── config.py                  # 환경변수 설정
├── requirements.txt           # Python 의존성
├── routers/
│   ├── __init__.py
│   ├── chat.py               # ChatGPT API 라우트
│   └── upload_time.py        # 업로드 시간 추천 라우트
└── services/
    ├── __init__.py
    ├── openai_service.py     # OpenAI API 서비스
    └── upload_time_service.py # 업로드 시간 분석 서비스
```

### API 문서
서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📝 사용 예시

### Python (requests)
```python
import requests

# 업로드 시간 추천 (GET 요청)
response = requests.get('http://localhost:8000/api/upload-time/recommend')
data = response.json()
print(data['data']['recommendation'])

# 특정 콘텐츠 타입으로 추천
response = requests.get('http://localhost:8000/api/upload-time/recommend?content_type=entertainment')
data = response.json()
print(data['data']['recommendation'])
```

### JavaScript (Fetch API)
```javascript
// 업로드 시간 추천 (GET 요청)
const response = await fetch('http://localhost:8000/api/upload-time/recommend');
const data = await response.json();
console.log(data.data.recommendation);

// 특정 콘텐츠 타입으로 추천
const response2 = await fetch('http://localhost:8000/api/upload-time/recommend?content_type=entertainment');
const data2 = await response2.json();
console.log(data2.data.recommendation);
```

### React 예시
```jsx
import { useState, useEffect } from 'react';

function UploadTimeRecommendation() {
  const [recommendation, setRecommendation] = useState('');

  const getRecommendation = async () => {
    try {
      // GET 요청으로 간단하게 추천 받기
      const response = await fetch('http://localhost:8000/api/upload-time/recommend');
      const data = await response.json();
      setRecommendation(data.data.recommendation);
    } catch (error) {
      console.error('오류:', error);
    }
  };

  // 컴포넌트 마운트 시 자동으로 추천 받기
  useEffect(() => {
    getRecommendation();
  }, []);

  return (
    <div>
      <h2>오늘의 업로드 시간 추천</h2>
      <button onClick={getRecommendation}>새로고침</button>
      <div>{recommendation}</div>
    </div>
  );
}
```

## 🔒 보안 주의사항

1. **API 키 보안**: `.env` 파일을 `.gitignore`에 추가하여 API 키가 노출되지 않도록 하세요.
2. **CORS 설정**: 프로덕션 환경에서는 적절한 CORS 설정을 하세요.
3. **요청 제한**: 필요에 따라 rate limiting을 구현하세요.

## 🚀 배포

### Docker 사용
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku 배포
```bash
# Procfile 생성
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Heroku에 배포
git add .
git commit -m "FastAPI 서버 배포"
git push heroku main
```

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. OpenAI API 키가 올바른지 확인
2. Python 버전이 3.8+ 인지 확인
3. 모든 의존성이 설치되었는지 확인
4. 서버 로그 확인

## 🎯 주요 특징

- ⚡ **FastAPI**: 고성능, 자동 문서화, 타입 힌트 지원
- 🤖 **GPT-4o**: 최신 최고 성능 모델 사용
- 📅 **한국 특화**: 명절, 요일별 시청 패턴 분석
- 🎬 **전문적 추천**: 사진과 같은 분석적 톤의 추천
- 🔧 **타입 안전성**: Pydantic 모델로 데이터 검증
- 📚 **자동 문서화**: Swagger UI와 ReDoc 지원
- 🚀 **GET 요청만**: 사용자 입력 없이 자동으로 현재 날짜 기준 추천
