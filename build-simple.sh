#!/usr/bin/env bash

# Render 공식 문서의 간단한 해결책
echo "🚀 간단한 빌드 시작..."

# pip 업그레이드
pip install --upgrade pip

# 바이너리 패키지 우선 설치 시도
echo "📦 바이너리 패키지 우선 설치 중..."
pip install --no-cache-dir --prefer-binary -r requirements.txt

echo "✅ 빌드 완료!"
