#!/usr/bin/env bash

# Render 공식 문서에 따른 Rust 설치 스크립트
echo "🔧 Rust 설치 시작..."

# Rust 설치 (자동으로 yes 응답)
curl https://sh.rustup.rs -sSf | sh -s -- -y

# 환경 변수 설정
export PATH="$HOME/.cargo/bin:$PATH"
export CARGO_HOME="$HOME/.cargo"
export RUSTUP_HOME="$HOME/.rustup"

# Rust 환경 활성화
source "$HOME/.cargo/env"

# Rust 버전 확인
echo "✅ Rust 설치 완료:"
rustc --version
cargo --version

# pip 업그레이드
echo "⬆️ pip 업그레이드 중..."
pip install --upgrade pip

# Python 패키지 설치
echo "📚 Python 패키지 설치 중..."
pip install --no-cache-dir -r requirements.txt

echo "🎉 빌드 완료!"
