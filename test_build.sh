#!/bin/bash

echo "🔍 로컬 빌드 테스트 시작..."

# 가상환경 생성 (이미 있다면 스킵)
if [ ! -d "test_venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv test_venv
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source test_venv/bin/activate

# pip 업그레이드
echo "⬆️ pip 업그레이드 중..."
pip install --upgrade pip

# 의존성 설치
echo "📚 의존성 설치 중..."
pip install --no-cache-dir --prefer-binary -r requirements.txt

# 설치된 패키지 확인
echo "✅ 설치된 패키지 확인:"
pip list

# 서버 테스트 실행
echo "🚀 서버 테스트 실행 중..."
echo "서버를 시작하려면 다음 명령어를 실행하세요:"
echo "source test_venv/bin/activate && python main.py"

echo "🧹 테스트 완료! 가상환경을 정리하려면: rm -rf test_venv"