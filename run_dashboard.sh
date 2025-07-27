#!/bin/bash

# Streamlit 대시보드 실행 스크립트

echo "🚀 무신사 마케팅 분석 대시보드를 시작합니다..."
echo ""
echo "브라우저에서 자동으로 열립니다."
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

# Streamlit 실행
python3 -m streamlit run app.py --server.port 8501