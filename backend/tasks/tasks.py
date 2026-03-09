from crewai import Task
from textwrap import dedent


def task_briefing_analysis(agent, briefing: str, conto: str = None):
    return Task(
        description=dedent(f"""
            Analise o seguinte briefing de Paulo e crie um plano de campanha completo:

            BRIEFING: {briefing}
            CONTO: {conto if conto else 'A definir'}

            O plano deve incluir:
            1. Objetivo principal da campanha
            2. Público-alvo
            3. Canais prioritários
            4. Lista de tarefas para cada agente
            5. Cronograma sugerido
            6. KPIs de sucesso
        """),
        agent=agent,
        expected_output="Plano de campanha detalhado em formato estruturado",
    )


def task_market_research(agent, conto: str, objetivo: str):
    return Task(
        description=dedent(f"""
            Faça uma pesquisa de mercado completa para a campanha do conto '{conto}'.

            Objetivo da campanha: {objetivo}

            Pesquise:
            1. Palavras-chave YouTube com maior potencial
            2. Concorrentes diretos e indiretos no nicho de contos/literatura
            3. Tendências de conteúdo relevantes
            4. Melhores horários de publicação no YouTube
            5. Formatos de conteúdo com maior engajamento no nicho
        """),
        agent=agent,
        expected_output="Relatório de pesquisa com palavras-chave, tendências e oportunidades",
    )


def task_content_strategy(agent, pesquisa: str, conto: str):
    return Task(
        description=dedent(f"""
            Com base na pesquisa de mercado abaixo, crie a estratégia de conteúdo
            para a campanha do conto '{conto}'.

            PESQUISA: {pesquisa}

            Entregue:
            1. Proposta de posicionamento
            2. Calendário de conteúdo (30 dias)
            3. Tipos de conteúdo para cada canal
            4. Funil de conteúdo (topo/meio/fundo)
            5. Estratégia de crescimento no YouTube
        """),
        agent=agent,
        expected_output="Estratégia de conteúdo completa com calendário de 30 dias",
    )


def task_copy_creation(agent, estrategia: str, conto: str, tipo: str):
    return Task(
        description=dedent(f"""
            Crie os textos para a campanha do conto '{conto}'.

            ESTRATÉGIA: {estrategia}
            TIPO DE CONTEÚDO: {tipo}

            Entregue:
            1. Título principal do vídeo YouTube (5 opções)
            2. Roteiro completo do vídeo
            3. Descrição otimizada do YouTube
            4. Legenda para Instagram
            5. Post para Twitter/X
            6. Hook para TikTok (15 segundos)
        """),
        agent=agent,
        expected_output="Todos os textos criados prontos para revisão e aprovação",
    )


def task_visual_creation(agent, conto: str, tipo_conteudo: str, assets_path: str):
    return Task(
        description=dedent(f"""
            Crie os materiais visuais para a campanha do conto '{conto}'.

            TIPO DE CONTEÚDO: {tipo_conteudo}
            CAMINHO DOS ASSETS: {assets_path}/ilustracoes-contos/{conto}/

            Processo:
            1. Leia o arquivo estilo.md do conto
            2. Analise as imagens de referência da pasta referencias/
            3. Crie prompts detalhados para:
               - Thumbnail do YouTube (1280x720)
               - Post Instagram (1080x1080)
               - Story Instagram (1080x1920)
            4. Gere as imagens usando DALL-E 3
            5. Documente os prompts usados para futura referência
        """),
        agent=agent,
        expected_output="Imagens geradas + prompts documentados, prontos para aprovação",
    )


def task_video_production(agent, roteiro: str, conto: str, assets_path: str):
    return Task(
        description=dedent(f"""
            Produza o vídeo para o YouTube do conto '{conto}'.

            ROTEIRO: {roteiro}
            ASSETS VISUAIS: {assets_path}/ilustracoes-contos/{conto}/

            Entregue:
            1. Storyboard detalhado (cena por cena)
            2. Prompts para geração de cenas via Runway ML
            3. Sugestão de trilha sonora
            4. Estrutura de edição
            5. Vídeo final gerado (ou instruções detalhadas de geração)
        """),
        agent=agent,
        expected_output="Storyboard completo + prompts de vídeo + estrutura de edição",
    )


def task_seo_optimization(agent, titulo: str, descricao: str, palavras_chave: list):
    return Task(
        description=dedent(f"""
            Otimize o conteúdo para SEO no YouTube.

            TÍTULO ATUAL: {titulo}
            DESCRIÇÃO ATUAL: {descricao}
            PALAVRAS-CHAVE: {', '.join(palavras_chave)}

            Entregue:
            1. Título otimizado (máx 60 caracteres)
            2. Descrição otimizada com keywords naturalmente inseridas
            3. Tags recomendadas (20 tags)
            4. Hashtags para a descrição
            5. Horário ideal de publicação
            6. Sugestões de cards e end screens
        """),
        agent=agent,
        expected_output="Metadados completos otimizados para YouTube",
    )


def task_analysis_report(agent, canal: str, periodo: str):
    return Task(
        description=dedent(f"""
            Gere um relatório de desempenho das campanhas da Libbro.

            CANAL: {canal}
            PERÍODO: {periodo}

            O relatório deve conter:
            1. Métricas principais (views, watch time, CTR, subscribers)
            2. Conteúdos com melhor desempenho
            3. Conteúdos que não performaram bem e por quê
            4. Insights de audiência
            5. Recomendações de próximos passos (top 3)
        """),
        agent=agent,
        expected_output="Relatório de desempenho com insights e recomendações acionáveis",
    )
