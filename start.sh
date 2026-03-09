#!/bin/bash
echo "🚀 Iniciando Libbro Marketing App..."

# Backend
cd backend
pip install -r requirements.txt -q
uvicorn api:app --host 0.0.0.0 --port 8000 --reload &
echo "✅ API rodando em http://localhost:8000"

# Frontend
cd ../frontend
npm install -q
npm run dev &
echo "✅ Frontend rodando em http://localhost:3000"

echo ""
echo "📖 Documentação da API: http://localhost:8000/docs"
wait
