# 📊 Controller Project BI — Gestão Ágil de Projetos com Dashboard Interativo

> Sistema completo de acompanhamento de projetos com Kanban board local (Planka/Jira-like), BI Dashboard interativo com métricas de WIP, KPI, OKR, ROI, Trade-off e Previsibilidade Operacional — tudo integrado e rodando localmente via Docker.

---

## 🎯 Objetivo do Projeto

Demonstrar como um **Analista / Agilista** controla múltiplos projetos simultâneos com uma visão orientada a dados, tomando decisões baseadas em métricas reais — e não em feeling.

O projeto simula um portfólio de **5 projetos de TI** reais/fictícios com seus respectivos boards Kanban populados, métricas calculadas e um BI customizado que consolida tudo em uma interface interativa.

---

## 🏗️ Arquitetura

```
Controller_Project_BI/
│
├── bi-dashboard/
│   └── index.html          # BI Dashboard (HTML + CSS + JS + ApexCharts)
│
├── data/
│   └── projetos.json       # Base de dados dos 5 projetos com todas as métricas
│
├── plane/
│   └── docker-compose.yml  # Orquestração do Planka (Kanban board) via Docker
│
└── scripts/
    └── popular_planka.py   # Script Python que popula o Planka via API REST
```

---

## 🛠️ Stack Tecnológica

| Tecnologia | Papel no projeto |
|---|---|
| **Docker** | Orquestração dos containers (Planka + PostgreSQL) |
| **Planka** | Kanban board open-source (alternativa ao Jira), rodando 100% local |
| **PostgreSQL** | Banco de dados do Planka (container Docker) |
| **Python 3** | Scripts de automação — popula o board via API REST |
| **HTML / CSS / JS** | BI Dashboard — sem frameworks, vanilla puro |
| **ApexCharts** | Biblioteca de gráficos interativos (Radar, Burndown, Donut, Radial) |
| **JSON** | Base de dados estruturada com métricas de todos os projetos |
| **Git + GitHub** | Versionamento e portfólio público |

---

## 📦 Como Rodar Localmente

### Pré-requisitos
- Docker Desktop instalado e rodando
- Python 3.x instalado
- `pip install requests`

### 1. Subir o Planka (Kanban Board)
```bash
cd plane/
docker compose up -d
```
Acesse: `http://localhost:3333`
- **Login:** admin@portfolio.com
- **Senha:** Admin@2026

### 2. Popular o board com os 5 projetos
```bash
python scripts/popular_planka.py
```
Isso cria automaticamente **5 projetos** com **145 tasks** distribuídas em colunas Kanban via API REST.

### 3. Abrir o BI Dashboard
Abra o arquivo diretamente no navegador:
```
bi-dashboard/index.html
```
Não requer servidor — é um arquivo HTML auto-contido.

---

## 📊 O que o BI Dashboard exibe

### Visão Geral do Portfólio
- Cards de todos os projetos com progresso visual
- Comparativo de ROI entre projetos
- Distribuição de WIP (Work In Progress) por projeto
- Satisfação dos stakeholders (benchmark: ≥ 85)

### Por Projeto (6 abas interativas)

| Aba | Métricas |
|---|---|
| **Visão Geral** | Status, time, tecnologias, progresso, WIP Kanban, velocidade por sprint |
| **KPIs** | 8 indicadores: cobertura de testes, taxa de defeitos, lead time, cycle time, throughput, deploy frequency, MTTR, satisfação |
| **OKRs** | Objetivo estratégico + 4 Key Results com progresso e status (Atingido / Em andamento / Em risco) |
| **ROI** | Investimento × Valor gerado, lucro líquido, ROI %, detalhamento financeiro |
| **Trade-off** | Radar das 4 dimensões: Custo × Prazo × Escopo × Qualidade + decisão documentada |
| **Previsibilidade** | Burndown real vs ideal, aderência ao prazo, desvio médio, matriz de riscos |

---

## 💡 Como o ROI é calculado

```
ROI (%) = (Valor Gerado − Custo Total) / Custo Total × 100
```

**Custo Total** = horas trabalhadas × taxa horária (variável por senioridade do time)

**Valor Gerado** = soma de: bugs evitados × custo médio por bug, horas manuais eliminadas × taxa/hora, economia de processos, projeção de receita adicional

### Resultados por projeto

| Projeto | Investido | Retorno | ROI |
|---|---|---|---|
| Projeto Saindo do Zero | R$ 42.886 | R$ 119.224 | **178%** |
| Artemis II | R$ 53.586 | R$ 74.820 | **40% ⚠️** |
| Portal RH Digital | R$ 79.716 | R$ 261.480 | **228%** |
| DataLake Corporativo | R$ 31.724 | R$ 83.418 | **163%** |
| App Mobile Vendas | R$ 14.578 | R$ 41.820 | **187%** |

> O **Artemis II com 40% de ROI** é intencional — demonstra que o gestor identifica projetos abaixo do esperado e toma decisões: revisar escopo, antecipar entregas de valor ou renegociar prazo com o sponsor.

---

## 🔍 Decisões de Gestão baseadas nos dados

**WIP acima do limite →** parar de puxar novas tarefas e desobstruir as que estão em andamento antes de avançar.

**Satisfação do stakeholder < 80 →** realinhar expectativas, revisar comunicação ou ajustar escopo antes da próxima sprint review.

**ROI abaixo de 100% →** projeto ainda consome mais do que entrega; escalar urgência ou redefinir prioridades de entrega.

**Burndown descolado do ideal →** desvio acumulado acima de 7 dias pede uma conversa difícil com o sponsor sobre prazo ou escopo.

---

## 🗂️ Projetos Gerenciados

| ID | Projeto | Categoria | Status | Progresso |
|---|---|---|---|---|
| PRJ-001 | Projeto Saindo do Zero | QA & Automação | Em Andamento | 72% |
| PRJ-002 | Artemis II | Data & Analytics | Em Andamento | 54% |
| PRJ-003 | Portal RH Digital | Migração de Sistema | Concluído | 100% |
| PRJ-004 | DataLake Corporativo | Data Engineering | Em Andamento | 38% |
| PRJ-005 | App Mobile Vendas | Mobile & CRM | Planejamento | 15% |

---

## 👤 Autor

**Rinaldo** — Analista de TI | QA | Agilista | DevOps  
[LinkedIn](https://www.linkedin.com/in/rinaldods) · [GitHub](https://github.com/RinaldoDS)

---

## 📄 Licença

MIT — livre para uso, estudo e adaptação.
