# Setup — Libbro Marketing App

## Rodando localmente

### 1. Clone o repositório
```bash
git clone <repo-url>
cd libbro-marketing
```

### 2. Configure as variáveis de ambiente
```bash
cp backend/config/.env.example backend/.env
# Edite backend/.env com suas API keys
```

### 3. Inicie tudo
```bash
chmod +x start.sh
./start.sh
```

### Ou manualmente:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Dashboard: http://localhost:3000
```

## Deploy no Railway

1. Crie conta em railway.app
2. Conecte o repositório GitHub
3. Configure as variáveis de ambiente no Railway
4. Deploy automático a cada push

## API Keys necessárias

| Variável | Serviço | Obrigatório |
|---|---|---|
| OPENAI_API_KEY | GPT-4o + DALL-E 3 | Sim (Fase 1) |
| ANTHROPIC_API_KEY | Claude | Opcional |
| YOUTUBE_API_KEY | YouTube Data API | Fase 3 |
| RUNWAY_API_KEY | Geração de vídeo | Fase 2 |
| ELEVENLABS_API_KEY | Voz | Fase 2 |
| STABILITY_API_KEY | Stable Diffusion | Fase 2 |
