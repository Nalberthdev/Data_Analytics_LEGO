# -*- coding: utf-8 -*-
"""
FRONT-END — DASHBOARD DE ESTATÍSTICA DO DATASET LEGO
===================================================

Dashboard interativo (Streamlit) — código SEPARADO e autossuficiente:
não depende do 'analise_lego.py'. Apresenta:
  - classificação das variáveis
  - tabelas de frequência (fi, fr, %)
  - gráficos de barras, setores/pizza e linhas (Apache ECharts)
  - galeria com as imagens reais dos conjuntos (pelas URLs do dataset)

Como executar localmente (de qualquer pasta):
    streamlit run frontend/app.py

Deploy: ver o README.md (Streamlit Community Cloud).
"""

import os

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts

# ----------------------------------------------------------------------
# CAMINHO DO DATASET
# Calculado a partir da localização deste arquivo, então funciona
# independente de onde o comando for executado (local ou na nuvem).
# ----------------------------------------------------------------------

PASTA_DESTE_ARQUIVO = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.dirname(PASTA_DESTE_ARQUIVO)

# procura o CSV em dois lugares: dentro de frontend/ ou na raiz do projeto
CAMINHOS_POSSIVEIS = [
    os.path.join(PASTA_DESTE_ARQUIVO, "base_de_dados", "lego_sets.csv"),
    os.path.join(RAIZ_PROJETO, "base_de_dados", "lego_sets.csv"),
]


@st.cache_data
def carregar_conjuntos():
    """Lê o CSV do dataset LEGO e devolve um DataFrame do pandas."""
    for caminho in CAMINHOS_POSSIVEIS:
        if os.path.exists(caminho):
            return pd.read_csv(caminho)
    raise FileNotFoundError(
        "Arquivo 'base_de_dados/lego_sets.csv' não encontrado. "
        "Coloque-o em 'frontend/base_de_dados/' ou na raiz do projeto."
    )


# ----------------------------------------------------------------------
# FUNÇÕES AUXILIARES DE ESTATÍSTICA
# ----------------------------------------------------------------------

def montar_tabela_frequencia(serie, incluir_vazios=True, ordenar_por_indice=False):
    """
    Tabela de frequência de uma coluna:
      fi           = frequência absoluta (contagem)
      fr           = frequência relativa (fi / n)
      %            = frequência percentual (fr * 100)
      fi_acumulada = frequência absoluta acumulada
    """
    fi = serie.value_counts(dropna=not incluir_vazios)
    fr = serie.value_counts(dropna=not incluir_vazios, normalize=True)

    tabela = pd.DataFrame({
        "fi": fi,
        "fr": fr.round(4),
        "%": (fr * 100).round(2),
    })
    if ordenar_por_indice:
        tabela = tabela.sort_index()
    tabela["fi_acumulada"] = tabela["fi"].cumsum()
    tabela.index.name = serie.name
    return tabela


# ----------------------------------------------------------------------
# APARÊNCIA
# ----------------------------------------------------------------------

COR_PRINCIPAL = "#D01012"   # vermelho LEGO
COR_SECUNDARIA = "#F5C518"  # amarelo LEGO
FONTE = "Fonte: LEGO Sets — Maven Analytics"

st.set_page_config(page_title="Estatística LEGO", page_icon="🧱", layout="wide")

st.markdown(
    f"""
    <div style="background:{COR_PRINCIPAL};padding:18px 24px;border-radius:10px;margin-bottom:8px">
      <h1 style="color:white;margin:0">🧱 Dashboard de Estatística — Conjuntos LEGO</h1>
      <p style="color:{COR_SECUNDARIA};margin:4px 0 0;font-size:16px">
        Coleta e análise de dados · tipos de variáveis · tabelas de frequência · gráficos
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# DADOS + FILTROS (barra lateral)
# ----------------------------------------------------------------------

conjuntos = carregar_conjuntos()

st.sidebar.header("Filtros")

ano_min, ano_max = int(conjuntos["year"].min()), int(conjuntos["year"].max())
faixa_anos = st.sidebar.slider("Ano de lançamento", ano_min, ano_max, (ano_min, ano_max))

grupos_disponiveis = sorted(conjuntos["themeGroup"].dropna().unique())
grupos_escolhidos = st.sidebar.multiselect(
    "Grupo de tema (themeGroup)", grupos_disponiveis, default=grupos_disponiveis
)

categorias_disponiveis = sorted(conjuntos["category"].dropna().unique())
categorias_escolhidas = st.sidebar.multiselect(
    "Categoria (category)", categorias_disponiveis, default=categorias_disponiveis
)

# aplica os filtros
dados = conjuntos[
    conjuntos["year"].between(*faixa_anos)
    & conjuntos["themeGroup"].isin(grupos_escolhidos)
    & conjuntos["category"].isin(categorias_escolhidas)
].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Conjuntos selecionados", f"{len(dados):,}".replace(",", "."))
st.sidebar.caption(FONTE)

if dados.empty:
    st.warning("Nenhum conjunto corresponde aos filtros escolhidos.")
    st.stop()

# ----------------------------------------------------------------------
# INDICADORES GERAIS
# ----------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nº de conjuntos (n)", f"{len(dados):,}".replace(",", "."))
col2.metric("Temas diferentes", dados["theme"].nunique())
col3.metric("Média de peças", f"{dados['pieces'].mean():.0f}")
col4.metric("Período", f"{faixa_anos[0]}–{faixa_anos[1]}")

st.markdown("---")

# ----------------------------------------------------------------------
# ABAS
# ----------------------------------------------------------------------

aba_var, aba_tab, aba_graf, aba_img = st.tabs(
    ["📋 Variáveis", "🔢 Tabelas de frequência", "📊 Gráficos", "🖼️ Galeria de imagens"]
)

# ---------- ABA 1: CLASSIFICAÇÃO DAS VARIÁVEIS ----------
with aba_var:
    st.subheader("Classificação das variáveis do dataset")
    classificacao = pd.DataFrame(
        [
            ["theme", "Qualitativa", "Nominal", "nomes de temas; sem ordem"],
            ["themeGroup", "Qualitativa", "Nominal", "grupos de temas; sem hierarquia"],
            ["category", "Qualitativa", "Nominal", "tipos de produto; sem ordem"],
            ["year", "Quantitativa", "Discreta", "valores isolados (anos), sem intermediários"],
            ["pieces", "Quantitativa", "Discreta", "contagem de peças"],
            ["minifigs", "Quantitativa", "Discreta", "contagem de bonecos"],
            ["agerange_min", "Quantitativa", "Discreta", "número; pode ser tratada como ordinal (faixa 4+, 6+...)"],
            ["US_retailPrice", "Quantitativa", "Contínua", "valor em dinheiro; admite casas decimais"],
        ],
        columns=["Coluna", "Tipo", "Subtipo", "Justificativa"],
    )
    st.dataframe(classificacao, width="stretch", hide_index=True)

    st.info(
        "**Régua rápida** — Qualitativa: é categoria/nome. Quantitativa: é número que dá para "
        "calcular. | Nominal: sem ordem. Ordinal: tem ordem natural. | "
        "Discreta: você conta. Contínua: você mede."
    )

# ---------- ABA 2: TABELAS DE FREQUÊNCIA ----------
with aba_tab:
    st.subheader("Tabelas de frequência")

    escolha = st.selectbox(
        "Escolha a variável",
        {
            "themeGroup — grupo de tema (qualitativa nominal)": ("themeGroup", False),
            "category — categoria (qualitativa nominal)": ("category", False),
            "agerange_min — idade mínima (quantitativa discreta / ordinal)": ("agerange_min", True),
            "year — ano de lançamento (quantitativa discreta)": ("year", True),
        }.keys(),
    )
    coluna, por_indice = {
        "themeGroup — grupo de tema (qualitativa nominal)": ("themeGroup", False),
        "category — categoria (qualitativa nominal)": ("category", False),
        "agerange_min — idade mínima (quantitativa discreta / ordinal)": ("agerange_min", True),
        "year — ano de lançamento (quantitativa discreta)": ("year", True),
    }[escolha]

    serie = dados[coluna]
    if coluna == "agerange_min":
        serie = serie.dropna().astype(int)

    tabela = montar_tabela_frequencia(serie, incluir_vazios=(coluna == "themeGroup"),
                                      ordenar_por_indice=por_indice)

    st.dataframe(tabela, width="stretch")
    st.caption(f"n = {int(tabela['fi'].sum())}  ·  Σ fi = n  ·  Σ % = 100")

    st.download_button(
        "Baixar tabela em CSV",
        tabela.to_csv().encode("utf-8"),
        file_name=f"tabela_{coluna}.csv",
        mime="text/csv",
    )

    # leitura automática do maior valor
    maior = tabela["fi"].idxmax()
    st.success(
        f"**Interpretação:** a categoria com maior frequência é **{maior}**, com "
        f"fi = {int(tabela.loc[maior, 'fi'])} conjuntos "
        f"({tabela.loc[maior, '%']}% do total selecionado)."
    )

# ---------- ABA 3: GRÁFICOS ----------
with aba_graf:
    st.subheader("Gráficos")

    st.caption("Gráficos interativos (biblioteca Apache ECharts). Passe o mouse para ver os valores.")

    PALETA = [COR_PRINCIPAL, COR_SECUNDARIA, "#0055BF", "#237841", "#8B4513", "#A0A0A0", "#FF8C00"]

    # --- BARRAS: themeGroup ---
    st.markdown("#### Gráfico de barras — conjuntos por grupo de tema")
    st.caption(
        "Barras servem para variável **qualitativa com várias categorias**: fácil comparar "
        "tamanhos e ordenar da maior para a menor."
    )
    barras = dados["themeGroup"].value_counts().sort_values(ascending=True)
    st_echarts(
        {
            "title": {"text": "Conjuntos LEGO por grupo de tema", "left": "center"},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "grid": {"left": 130, "right": 60, "top": 50, "bottom": 40},
            "xAxis": {"type": "value", "name": "fi (nº de conjuntos)"},
            "yAxis": {"type": "category", "data": barras.index.astype(str).tolist()},
            "series": [{
                "type": "bar",
                "data": barras.values.tolist(),
                "itemStyle": {"color": COR_PRINCIPAL},
                "label": {"show": True, "position": "right"},
            }],
        },
        height="480px",
    )

    # --- PIZZA / SETORES: category ---
    st.markdown("#### Gráfico de setores/pizza — distribuição por categoria")
    st.caption(
        "Pizza serve para **poucas categorias** quando queremos mostrar a **parte de um todo**. "
        "Cada fatia é uma categoria; o tamanho é o número de conjuntos (fi)."
    )
    pizza = dados["category"].value_counts()
    st_echarts(
        {
            "title": {"text": "Distribuição dos conjuntos por categoria", "left": "center"},
            "tooltip": {"trigger": "item", "formatter": "{b}: {c} conjuntos"},
            "legend": {"orient": "vertical", "left": "left", "top": "middle"},
            "color": PALETA,
            "series": [{
                "type": "pie",
                "radius": ["35%", "65%"],
                "center": ["58%", "55%"],
                "data": [{"name": str(n), "value": int(v)} for n, v in pizza.items()],
                "label": {"formatter": "{b}\n{c}"},
            }],
        },
        height="460px",
    )

    # --- LINHAS: lançamentos por ano ---
    st.markdown("#### Gráfico de linhas — evolução dos lançamentos ao longo do tempo")
    st.caption(
        "Linhas servem para mostrar a **evolução de uma quantidade ao longo do tempo**: "
        "o eixo X é o ano e a linha revela tendência de crescimento, quedas e picos."
    )
    linha = dados["year"].value_counts().sort_index()
    st_echarts(
        {
            "title": {"text": "Lançamentos de conjuntos LEGO por ano", "left": "center"},
            "tooltip": {"trigger": "axis"},
            "grid": {"left": 60, "right": 30, "top": 50, "bottom": 50},
            "xAxis": {"type": "category", "data": linha.index.astype(int).astype(str).tolist(),
                      "name": "Ano"},
            "yAxis": {"type": "value", "name": "fi (nº de conjuntos)"},
            "series": [{
                "type": "line",
                "data": linha.values.tolist(),
                "smooth": True,
                "areaStyle": {"opacity": 0.15},
                "itemStyle": {"color": COR_PRINCIPAL},
                "lineStyle": {"color": COR_PRINCIPAL, "width": 2},
            }],
        },
        height="420px",
    )

    # --- BARRAS: idade mínima ---
    st.markdown("#### Gráfico de barras — idade mínima recomendada")
    st.caption("Variável quantitativa discreta tratada como faixa ordinal (ordem natural das idades).")
    idade = dados["agerange_min"].dropna().astype(int).value_counts().sort_index()
    st_echarts(
        {
            "title": {"text": "Conjuntos por idade mínima recomendada", "left": "center"},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "grid": {"left": 60, "right": 30, "top": 50, "bottom": 50},
            "xAxis": {"type": "category", "data": idade.index.astype(str).tolist(),
                      "name": "Idade mínima (anos)"},
            "yAxis": {"type": "value", "name": "fi (nº de conjuntos)"},
            "series": [{
                "type": "bar",
                "data": idade.values.tolist(),
                "itemStyle": {"color": COR_SECUNDARIA},
                "label": {"show": True, "position": "top"},
            }],
        },
        height="420px",
    )

# ---------- ABA 4: GALERIA DE IMAGENS ----------
with aba_img:
    st.subheader("Galeria — imagens reais dos conjuntos (pelas URLs do dataset)")

    criterio = st.radio(
        "Ordenar por", ["Mais peças", "Mais minifiguras", "Mais recentes"], horizontal=True
    )
    coluna_ordem = {"Mais peças": "pieces", "Mais minifiguras": "minifigs", "Mais recentes": "year"}[criterio]

    quantidade = st.slider("Quantos conjuntos mostrar", 4, 24, 12, step=4)

    selecao = (
        dados.dropna(subset=["imageURL", coluna_ordem])
        .sort_values(coluna_ordem, ascending=False)
        .head(quantidade)
    )

    colunas_grade = st.columns(4)
    for i, (_, conjunto) in enumerate(selecao.iterrows()):
        with colunas_grade[i % 4]:
            st.image(conjunto["imageURL"], width="stretch")
            st.caption(
                f"**{conjunto['name']}**  \n"
                f"{conjunto['theme']} · {int(conjunto['year'])}  \n"
                f"{int(conjunto['pieces']) if pd.notna(conjunto['pieces']) else '?'} peças"
            )

st.markdown("---")
st.caption(f"Trabalho de Estatística · {FONTE} · imagens: brickset.com")
