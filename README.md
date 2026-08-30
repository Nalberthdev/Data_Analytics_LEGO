# Data Analytics LEGO — Trabalho de Estatística

Análise estatística do dataset **LEGO Sets** (Maven Analytics): coleta e análise
de dados, tipos de variáveis, tabelas de frequência e gráficos (barras,
setores/pizza e linhas).

## Estrutura do projeto

```
Data_Analytics_LEGO/
├── analise_lego.py            # script de análise: classificação de variáveis + tabelas de frequência
├── requirements.txt           # dependências (usado no deploy)
├── base_de_dados/
│   ├── lego_sets.csv          # dataset (18.457 conjuntos, 1970–2022)
│   └── lego_sets_data_dictionary.csv
├── saidas/                    # gerada ao rodar analise_lego.py (tabelas .csv)  [ignorada pelo git]
└── frontend/
    ├── app.py                 # dashboard interativo (Streamlit + Altair)
    ├── requirements.txt
    ├── .streamlit/config.toml
    ├── README.md              # instruções específicas de deploy
    └── base_de_dados/         # cópia do dataset (deixa a pasta autossuficiente)
```

## Pré-requisitos

- Python 3.10 ou superior
- `pip`

## Instalação

```bash
# (opcional, recomendado) criar um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# instalar as dependências
pip install -r requirements.txt
```

## Como executar

### 1. Script de análise (terminal)

Gera no terminal a classificação das variáveis e as tabelas de frequência
(fi, fr, %), e salva as tabelas em `saidas/*.csv`.

```bash
python analise_lego.py
```

### 2. Dashboard interativo (navegador)

Abre o painel com filtros, tabelas de frequência, gráficos e a galeria de
imagens dos conjuntos.

```bash
streamlit run frontend/app.py
```

Depois abra <http://localhost:8501> no navegador (o Streamlit costuma abrir
sozinho). Para encerrar, `Ctrl+C` no terminal.

## Publicar o dashboard na internet

Streamlit **não roda na Vercel** (precisa de servidor sempre ligado). Use o
**Streamlit Community Cloud** (gratuito). Passo a passo completo em
[`frontend/README.md`](frontend/README.md).

Resumo: subir para o GitHub → <https://share.streamlit.io> → *Create app* →
Main file path: `frontend/app.py` → *Deploy*.

## Dependências

| Pacote | Uso |
|---|---|
| `pandas` | leitura do CSV e cálculo das frequências |
| `streamlit` | interface web do dashboard |
| `altair` | gráficos interativos (barras, pizza, linhas) |

## Fonte dos dados

LEGO Sets — [Maven Analytics](https://www.mavenanalytics.io/data-playground).
Imagens dos conjuntos: brickset.com.
