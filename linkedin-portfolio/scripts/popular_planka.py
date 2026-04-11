"""
Script para popular o Planka com 5 projetos fictícios de portfólio LinkedIn.
Usa a API REST do Planka em http://localhost:3333
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
import time

BASE_URL = "http://localhost:3333"
EMAIL = "admin@portfolio.com"
PASSWORD = "Admin@2026"

session = requests.Session()
token = None

def login():
    global token
    resp = session.post(f"{BASE_URL}/api/access-tokens", json={
        "emailOrUsername": EMAIL,
        "password": PASSWORD
    })
    resp.raise_for_status()
    token = resp.json()["item"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    print(f"✅ Login OK — token obtido")

def get_projects():
    resp = session.get(f"{BASE_URL}/api/projects")
    resp.raise_for_status()
    return resp.json()["items"]

def create_project(name, background_color="#6366f1"):
    resp = session.post(f"{BASE_URL}/api/projects", json={
        "name": name,
        "type": "private"
    })
    resp.raise_for_status()
    return resp.json()["item"]

def create_board(project_id, name, position=0):
    resp = session.post(f"{BASE_URL}/api/projects/{project_id}/boards", json={
        "name": name,
        "position": position
    })
    resp.raise_for_status()
    return resp.json()["item"]

def get_board_detail(board_id):
    resp = session.get(f"{BASE_URL}/api/boards/{board_id}")
    resp.raise_for_status()
    return resp.json()

def create_list(board_id, name, position):
    resp = session.post(f"{BASE_URL}/api/boards/{board_id}/lists", json={
        "name": name,
        "position": position,
        "type": "active"
    })
    resp.raise_for_status()
    return resp.json()["item"]

def create_card(list_id, name, position, description="", due_date=None):
    payload = {"name": name, "position": position, "type": "project"}
    if description:
        payload["description"] = description
    if due_date:
        payload["dueDate"] = due_date
    resp = session.post(f"{BASE_URL}/api/lists/{list_id}/cards", json=payload)
    resp.raise_for_status()
    return resp.json()["item"]

def create_label(board_id, name, color):
    resp = session.post(f"{BASE_URL}/api/boards/{board_id}/labels", json={
        "name": name,
        "color": color,
        "position": 0
    })
    resp.raise_for_status()
    return resp.json()["item"]

def add_label_to_card(card_id, label_id):
    resp = session.post(f"{BASE_URL}/api/cards/{card_id}/labels", json={
        "labelId": label_id
    })
    # ignora erro se label já existe
    return resp

# ============================================================
# DADOS DOS PROJETOS
# ============================================================

PROJETOS = [
    {
        "nome": "PRJ-001 | Projeto Saindo do Zero",
        "boards": [
            {
                "nome": "Sprint Board — QA & Automação",
                "listas": [
                    {
                        "nome": "📋 Backlog",
                        "cards": [
                            ("Mapear casos de teste para módulo de relatórios", "Alta prioridade. Cobertura atual: 0%"),
                            ("Implementar testes de acessibilidade WCAG 2.1", "Requisito legal — prazo Q3 2026"),
                            ("Criar testes de performance com k6", "Threshold: < 2s p95"),
                            ("Documentar arquitetura de automação", "Onboarding de novos devs"),
                            ("Revisar fluxos de autenticação OAuth2", "Inclui MFA e SSO"),
                            ("Testes de segurança — OWASP Top 10", "Pentest automatizado"),
                            ("Configurar relatórios Allure no pipeline", "Visibilidade dos resultados"),
                            ("Integrar Playwright com Azure Test Plans", "Rastreabilidade de requisitos"),
                        ]
                    },
                    {
                        "nome": "🔨 Em Desenvolvimento",
                        "cards": [
                            ("Corrigir flakiness nos testes de login", "5 testes instáveis — causa: race condition no token"),
                            ("Implementar Page Object Model — módulo pagamentos", "Refatoração para melhor manutenção"),
                            ("Pipeline CI/CD: adicionar stage de smoke tests", "Jenkins + Azure DevOps"),
                            ("Testes E2E — fluxo de checkout completo", "Playwright — 15 cenários mapeados"),
                        ]
                    },
                    {
                        "nome": "👀 Em Revisão",
                        "cards": [
                            ("PR #47 — Suite de regressão módulo cadastro", "Review pendente com tech lead"),
                            ("Análise de cobertura — relatório Q1 2026", "SonarQube + Istanbul"),
                        ]
                    },
                    {
                        "nome": "✅ Concluído",
                        "cards": [
                            ("Setup inicial Playwright + TypeScript", "Estrutura base do projeto"),
                            ("Integração Jenkins — trigger automático no PR", "Webhook configurado"),
                            ("Testes unitários — camada de serviços", "Cobertura: 91%"),
                            ("Dashboard de métricas de qualidade", "Grafana + InfluxDB"),
                            ("Automação de testes de API — Postman/Newman", "45 endpoints cobertos"),
                            ("Relatório mensal de qualidade — Março 2026", "Enviado para stakeholders"),
                        ]
                    },
                ]
            }
        ]
    },
    {
        "nome": "PRJ-002 | Artemis II — Analytics Aeronáutico",
        "boards": [
            {
                "nome": "Sprint Board — Data & Analytics",
                "listas": [
                    {
                        "nome": "📋 Backlog",
                        "cards": [
                            ("Integrar dados históricos ANAC 2020-2023", "Volume estimado: 2M registros"),
                            ("Implementar alertas por WhatsApp/Telegram", "Notificações críticas em tempo real"),
                            ("Dashboard mobile — versão responsiva", "PWA com service worker"),
                            ("Exportação de relatórios em PDF/Excel", "Demanda dos stakeholders"),
                            ("Análise preditiva de atrasos por rota", "Machine Learning — scikit-learn"),
                            ("Cache Redis para queries pesadas", "Reduzir latência de 4.2 para < 1 min"),
                            ("API pública para parceiros", "Documentação Swagger/OpenAPI"),
                            ("Módulo de auditoria e logs de acesso", "Conformidade LGPD"),
                            ("Testes de carga — 1000 usuários simultâneos", "K6 + Grafana"),
                            ("Mapeamento de rotas internacionais", "Expansão do escopo"),
                            ("Integração com FlightAware API", "Dados complementares"),
                            ("Módulo de comparativos históricos", "YoY por rota/companhia"),
                            ("Scheduler de atualização automática", "Cron job — a cada 3h"),
                            ("Monitoramento com Datadog", "APM e traces distribuídos"),
                            ("Refatorar modelo de dados — normalização", "Performance de queries"),
                        ]
                    },
                    {
                        "nome": "🔨 Em Desenvolvimento",
                        "cards": [
                            ("Scraper ANAC — coleta automática de dados", "Playwright headless — 847 rotas"),
                            ("Dashboard principal — filtros por companhia/rota", "Chart.js + filtros dinâmicos"),
                            ("Retry automático em falhas de API", "Exponential backoff implementado"),
                        ]
                    },
                    {
                        "nome": "👀 Em Revisão",
                        "cards": [
                            ("Validação dos dados coletados vs fonte ANAC", "Precisão: 98.3%"),
                            ("Performance das queries — índices PostgreSQL", "Otimização em andamento"),
                        ]
                    },
                    {
                        "nome": "✅ Concluído",
                        "cards": [
                            ("Arquitetura do sistema — decisão técnica", "ADR documentado"),
                            ("Setup do banco de dados SQLite → PostgreSQL", "Migração concluída"),
                            ("Tela inicial — mapa interativo de rotas", "Leaflet.js"),
                            ("Autenticação e controle de acesso", "JWT + roles"),
                            ("ETL pipeline — versão 1.0", "Python + Pandas"),
                            ("Página ANAC — tabela de voos em tempo real", "atualização a cada 15 min"),
                            ("Testes de integração — pipeline ETL", "Cobertura: 78%"),
                        ]
                    },
                ]
            }
        ]
    },
    {
        "nome": "PRJ-003 | Portal RH Digital",
        "boards": [
            {
                "nome": "Sprint Board — Migração de Sistema",
                "listas": [
                    {
                        "nome": "📋 Backlog",
                        "cards": []
                    },
                    {
                        "nome": "🔨 Em Desenvolvimento",
                        "cards": []
                    },
                    {
                        "nome": "👀 Em Revisão",
                        "cards": []
                    },
                    {
                        "nome": "✅ Concluído — PROJETO ENCERRADO",
                        "cards": [
                            ("Levantamento de requisitos com RH", "450 funcionários impactados"),
                            ("Análise e modelagem do banco de dados", "PostgreSQL — 47 tabelas"),
                            ("Arquitetura da solução — React + Node.js", "Decisão técnica documentada"),
                            ("Setup do ambiente Docker + CI/CD", "GitHub Actions"),
                            ("Módulo de cadastro de funcionários", "CRUD completo + histórico"),
                            ("Sistema de ponto eletrônico", "Integração com relógios Topdata"),
                            ("Módulo de folha de pagamento", "Integração com Domínio Sistemas"),
                            ("Gestão de benefícios — plano de saúde/VT/VR", "Multi-operadora"),
                            ("Portal self-service do funcionário", "App web responsivo"),
                            ("Módulo de férias e afastamentos", "Cálculo automático INSS/FGTS"),
                            ("Relatórios gerenciais — headcount/turnover", "Power BI embarcado"),
                            ("Conformidade LGPD — anonimização de dados", "DPO aprovado"),
                            ("Treinamento de usuários RH", "120 usuários treinados"),
                            ("Go-live e suporte pós-implantação", "Zero incidentes críticos"),
                            ("Encerramento oficial e documentação final", "Aceite do cliente em 28/02/2024"),
                        ]
                    },
                ]
            }
        ]
    },
    {
        "nome": "PRJ-004 | DataLake Corporativo",
        "boards": [
            {
                "nome": "Sprint Board — Data Engineering",
                "listas": [
                    {
                        "nome": "📋 Backlog",
                        "cards": [
                            ("Ingestão — ERP SAP (fonte 8/15)", "Conector nativo + API REST"),
                            ("Ingestão — CRM Salesforce (fonte 9/15)", "Bulk API 2.0"),
                            ("Ingestão — e-commerce Shopify (fonte 10/15)", "Webhooks + polling"),
                            ("Ingestão — ERP Totvs Protheus (fonte 11/15)", "SOAP → REST adapter"),
                            ("Ingestão — Google Analytics 4 (fonte 12/15)", "BigQuery export"),
                            ("Ingestão — Ads Meta/Google (fonte 13/15)", "Marketing data"),
                            ("Ingestão — Sistemas legados (fontes 14-15/15)", "FTP + CSV batch"),
                            ("Camada Gold — modelo dimensional vendas", "Star schema"),
                            ("Camada Gold — modelo dimensional RH", "SCD Type 2"),
                            ("Orquestração Airflow — DAGs produção", "Scheduling robusto"),
                            ("Data catalog — Amundsen/DataHub", "Governança e descoberta"),
                            ("Reduzir relatórios manuais: fase 2 (80% meta)", "Automação BI"),
                            ("Treinamento time de dados — dbt avançado", "5 analistas"),
                            ("Documentação técnica das pipelines", "dbt docs"),
                            ("Monitoramento de qualidade — Great Expectations", "Alertas automáticos"),
                            ("Disaster recovery — backup automatizado", "RTO: 4h / RPO: 1h"),
                            ("Dashboard executivo — CEO/CFO", "Métricas de negócio consolidadas"),
                            ("Implementar CDC — Change Data Capture", "Debezium + Kafka"),
                            ("Migrar para cluster PostgreSQL HA", "Alta disponibilidade"),
                            ("Cost optimization — particionamento de tabelas", "Reduzir storage 40%"),
                            ("Testes de contrato — schema registry", "Evitar schema drift"),
                            ("Auditoria de acesso aos dados", "LGPD compliance"),
                        ]
                    },
                    {
                        "nome": "🔨 Em Desenvolvimento",
                        "cards": [
                            ("Latência ETL — otimização para < 2h", "Atual: 3.1h — profiling em andamento"),
                            ("Camada Silver — transformações DW financeiro", "dbt models"),
                            ("Data quality score — tabelas gold", "Great Expectations — meta 95%"),
                        ]
                    },
                    {
                        "nome": "👀 Em Revisão",
                        "cards": [
                            ("DAG Airflow — pipeline financeiro", "Code review com arquiteto"),
                        ]
                    },
                    {
                        "nome": "✅ Concluído",
                        "cards": [
                            ("Arquitetura do DataLake — Medallion (Bronze/Silver/Gold)", "ADR aprovado"),
                            ("Setup infraestrutura Docker Compose", "PostgreSQL + Airflow + dbt"),
                            ("Ingestão fonte 1 — banco transacional principal", "PostgreSQL → Bronze"),
                            ("Ingestão fonte 2 — sistema financeiro legado", "Oracle → Bronze via JDBC"),
                            ("Ingestão fonte 3 — planilhas Excel mensais", "S3 → Bronze automático"),
                            ("Ingestão fonte 4 — API REST parceiros", "JSON → Bronze normalizado"),
                            ("Ingestão fonte 5 — logs de aplicação", "Fluentd → Bronze"),
                            ("Ingestão fonte 6 — dados de RH", "CSV batch diário"),
                            ("Ingestão fonte 7 — e-mail reports automáticos", "IMAP → parser → Bronze"),
                            ("Camada Bronze — validação e catalogação", "Schema enforcement"),
                            ("Primeiros relatórios automatizados (12/? concluídos)", "Economia: 48h/mês analistas"),
                            ("Pipeline de CI/CD para dbt models", "GitHub Actions"),
                        ]
                    },
                ]
            }
        ]
    },
    {
        "nome": "PRJ-005 | App Mobile Vendas (CRM)",
        "boards": [
            {
                "nome": "Sprint Board — Mobile & CRM",
                "listas": [
                    {
                        "nome": "📋 Backlog",
                        "cards": [
                            ("Integração Salesforce — sincronização bidirecional", "120 vendedores impactados"),
                            ("Módulo de geolocalização — check-in em cliente", "GPS + Google Maps API"),
                            ("Histórico de visitas e interações", "Timeline por cliente"),
                            ("Push notifications — alertas de follow-up", "Firebase Cloud Messaging"),
                            ("Relatório de performance individual", "Metas vs realizado"),
                            ("Modo offline — sincronização ao reconectar", "SQLite local + conflict resolution"),
                            ("Integração com agenda — Google Calendar", "Agendamento de visitas"),
                            ("Dashboard gerencial — visão do time", "Funil de vendas em tempo real"),
                            ("Assinatura digital de propostas", "DocuSign SDK"),
                            ("Chatbot de qualificação de leads", "Dialogflow CX"),
                            ("Submissão para App Store (iOS)", "Guidelines Apple revisados"),
                            ("Submissão para Google Play (Android)", "Policy compliance"),
                            ("Treinamento força de vendas — 120 usuários", "Onboarding gamificado"),
                            ("Módulo de cotação rápida", "Integração com tabela de preços ERP"),
                            ("Analytics de uso — Amplitude", "Funil de adoção"),
                            ("Testes de usabilidade com vendedores reais", "UX research — 10 entrevistas"),
                            ("Modo dark e acessibilidade", "WCAG 2.1 AA"),
                            ("Widget de resumo para tela inicial", "iOS/Android widgets"),
                            ("Integração WhatsApp Business API", "Envio de propostas"),
                            ("Relatório ROI — impacto nas vendas", "KPI: aumento de 15% conversão"),
                            ("Segurança — biometria e criptografia E2E", "LGPD compliance"),
                            ("Suporte multi-empresa — white label", "v2.0 roadmap"),
                            ("Backup automático de dados locais", "Proteção contra perda"),
                            ("A/B testing — variações do pipeline view", "Otimização UX"),
                            ("Internacionalização — en/es", "Expansão Latam"),
                            ("Testes automatizados — Detox", "E2E mobile"),
                            ("Performance — lazy loading e cache de imagens", "< 100ms UI interactions"),
                            ("Configurações por perfil — gerente/vendedor", "RBAC"),
                            ("Importação de contatos do smartphone", "Contatos → Leads"),
                            ("Scanner de cartão de visita — OCR", "Google ML Kit"),
                            ("Gamificação — ranking e conquistas", "Engajamento da equipe"),
                            ("Video call integrada — reuniões remotas", "WebRTC"),
                            ("Mapa de calor — clientes por região", "Heatmap por performance"),
                            ("Aprovação de desconto — workflow digital", "Eliminar aprovação por e-mail"),
                            ("Relatório de pipeline — forecast Q3 2026", "Previsão de receita"),
                        ]
                    },
                    {
                        "nome": "🔨 Em Desenvolvimento",
                        "cards": [
                            ("Tela de lista de leads — filtros e busca", "React Native + FlatList virtualizada"),
                            ("Tela de pipeline — Kanban drag & drop", "react-native-draggable-flatlist"),
                        ]
                    },
                    {
                        "nome": "👀 Em Revisão",
                        "cards": []
                    },
                    {
                        "nome": "✅ Concluído",
                        "cards": [
                            ("Definição do escopo MVP — 3 features core", "Leads + Pipeline + Geo"),
                            ("Arquitetura técnica — React Native + Node.js + MongoDB", "ADR aprovado"),
                            ("Setup do projeto e estrutura de pastas", "Monorepo — Turborepo"),
                            ("Design system — componentes base", "Figma → código"),
                            ("Tela de login e autenticação biométrica", "Face ID / Touch ID"),
                            ("Tela de dashboard — resumo do dia", "Cards de métricas"),
                            ("Navegação e estrutura de tabs", "React Navigation 6"),
                            ("API backend — endpoints CRUD leads", "Node.js + Express + MongoDB"),
                        ]
                    },
                ]
            }
        ]
    },
]

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    print("🚀 Iniciando população do Planka...")
    login()

    # Verificar projetos existentes
    projetos_existentes = get_projects()
    nomes_existentes = [p["name"] for p in projetos_existentes]
    print(f"   Projetos existentes: {nomes_existentes}")

    total_cards = 0

    for proj_data in PROJETOS:
        nome_projeto = proj_data["nome"]

        if nome_projeto in nomes_existentes:
            print(f"   ⚠️  Projeto '{nome_projeto}' já existe, pulando...")
            continue

        print(f"\n📁 Criando projeto: {nome_projeto}")
        projeto = create_project(nome_projeto)
        proj_id = projeto["id"]
        time.sleep(0.5)

        for i, board_data in enumerate(proj_data["boards"]):
            print(f"   📌 Criando board: {board_data['nome']}")
            board = create_board(proj_id, board_data["nome"], position=i * 65536)
            board_id = board["id"]
            time.sleep(0.5)

            for j, lista_data in enumerate(board_data["listas"]):
                print(f"      📂 Criando lista: {lista_data['nome']} ({len(lista_data['cards'])} cards)")
                lista = create_list(board_id, lista_data["nome"], position=j * 65536)
                lista_id = lista["id"]
                time.sleep(0.3)

                for k, card_info in enumerate(lista_data["cards"]):
                    if isinstance(card_info, tuple):
                        card_nome, card_desc = card_info
                    else:
                        card_nome, card_desc = card_info, ""

                    card = create_card(lista_id, card_nome, position=k * 65536, description=card_desc)
                    total_cards += 1
                    time.sleep(0.1)

        print(f"   ✅ Projeto criado com sucesso!")

    print(f"\n🎉 Concluído! Total de cards criados: {total_cards}")
    print(f"🌐 Acesse: http://localhost:3333")
    print(f"👤 Login: admin@portfolio.com / Admin@2026")

if __name__ == "__main__":
    main()
