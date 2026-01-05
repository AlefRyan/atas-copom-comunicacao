
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path


# -----------------------------
# Configurações gerais
# -----------------------------
st.set_page_config(
    page_title="Comunicação Copom",
    layout='centered'
)


df = pd.read_parquet(r'construindo-indices/atas.parquet')

# garantir datetime
df["data_reunião"] = pd.to_datetime(df["data_reunião"])
df = df.sort_values("data_reunião")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Comunicação Copom")
page = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Visão Geral",
        "Raspagem de Dados",
        "🧭 Postura Monetária (HD)",
        "⚠️ Incerteza Comunicacional",
        "🔄 Alinhamento Discurso–Ação",
        "ℹ️ Metodologia & Dados",
        "Contato"
    ]
)

# -----------------------------
# 🏠 VISÃO GERAL
# -----------------------------
if page == "🏠 Visão Geral":
    st.title("📊 Comunicação Copom")

    st.markdown("""
    Este painel transforma a comunicação do Comitê de Política Monetária (Copom)
    em **indicadores quantitativos**, permitindo analisar a postura monetária,
    o grau de incerteza do discurso e o alinhamento entre comunicação e decisão.
    """)

    st.subheader("Postura Monetária ao longo do tempo")

    df_plot = df[df["data_reunião"] >= "2004-01-01"]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_plot["data_reunião"], df_plot["hd_index"])
    ax.axhline(0, linestyle="--")
    ax.set_ylabel("Índice Hawk–Dove")
    ax.set_xlabel("Ano")
    st.pyplot(fig)

    st.markdown("""
    **Interpretação**  
    Valores positivos indicam comunicação mais **hawkish**,
    enquanto valores negativos refletem viés **dovish**.
    """)
    

elif page == "Raspagem de Dados":
    st.title("🕷️ Raspagem de Dados – Atas do Copom")

    st.markdown("""
    Esta etapa é responsável pela **coleta automatizada das atas do Copom**
    diretamente do site do Banco Central do Brasil.

    O código abaixo realiza:
    - Navegação automatizada com Selenium
    - Download das atas
    - Extração e organização do texto
    - Armazenamento estruturado para análise posterior
    """)

    

    caminho_codigo = Path("script-coleta-dados/bcb.ipynb")

    with open(caminho_codigo, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    for cell in notebook.get("cells", []):

        # ---- células MARKDOWN ----
        if cell.get("cell_type") == "markdown":
            texto = "".join(cell.get("source", []))
            if texto.strip():
                st.markdown(texto)

        # ---- células CÓDIGO ----
        elif cell.get("cell_type") == "code":
            codigo = "".join(cell.get("source", []))
            if codigo.strip():
                st.code(codigo, language="python")

else:
    st.warning("Notebook de raspagem não encontrado.")

# -----------------------------
# 🧭 POSTURA MONETÁRIA
# -----------------------------
elif page == "🧭 Postura Monetária (HD)":
    st.title("🧭 Postura Monetária (HD)")

    st.markdown("""
    O índice Hawk–Dove resume a **direção da postura monetária**
    implícita na comunicação do Copom.
    """)

    ano_min, ano_max = st.slider(
        "Selecione o período",
        int(df["data_reunião"].dt.year.min()),
        int(df["data_reunião"].dt.year.max()),
        (2004, 2024)
    )

    df_hd = df[
        (df["data_reunião"].dt.year >= ano_min) &
        (df["data_reunião"].dt.year <= ano_max)
    ]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_hd["data_reunião"], df_hd["hd_index"])
    ax.axhline(0, linestyle="--")
    ax.set_ylabel("HD")
    st.pyplot(fig)

    st.info(
        "HD > 0 → viés hawkish | HD < 0 → viés dovish"
    )

# -----------------------------
# ⚠️ INCERTEZA COMUNICACIONAL
# -----------------------------
elif page == "⚠️ Incerteza Comunicacional":
    st.title("⚠️ Incerteza Comunicacional")

    st.markdown("""
    Este indicador mede o **grau de cautela, risco e condicionalidade**
    presente na comunicação do Copom.
    """)
    
    df_plot = df[df["data_reunião"] >= "2004-01-01"]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_plot["data_reunião"], df_plot["un_index"])
    ax.set_ylabel("Índice de Incerteza")
    ax.set_xlabel("Ano")
    st.pyplot(fig)

    st.markdown("""
    Picos de incerteza tendem a ocorrer em períodos de
    **crise, transição de regime ou choques macroeconômicos**.
    """)

# -----------------------------
# 🔄 ALINHAMENTO DISCURSO–AÇÃO
# -----------------------------
elif page == "🔄 Alinhamento Discurso–Ação":
    st.title("🔄 Alinhamento Discurso–Ação")

    st.markdown("""
    Este indicador mede o **desalinhamento entre a orientação implícita
    no discurso do Copom e a decisão efetiva de política monetária
    na reunião seguinte**, com base exclusivamente no texto.
    """)

    df_plot = df[df["data_reunião"] >= "2004-01-01"] 
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_plot["data_reunião"], df_plot["comm_gap"])
    ax.axhline(0, linestyle="--")
    ax.set_ylabel("Alinhamento (ΔSelic observado − implícito)")
    ax.set_xlabel("Ano")
    st.pyplot(fig)

    st.markdown("""
    **Interpretação**
    - Próximo de zero → discurso e decisão alinhados  
    - Positivo → decisão mais hawkish que o discurso  
    - Negativo → decisão mais dovish que o discurso  
    """)

# -----------------------------
# ℹ️ METODOLOGIA & DADOS
# -----------------------------
elif page == "ℹ️ Metodologia & Dados":
    st.title("ℹ️ Metodologia & Dados")

    st.markdown("""
    **Fonte dos dados**  
    - Atas das reuniões do Copom (Banco Central do Brasil)

    **Construção da base**  
    - Coleta e extração de texto realizadas via Web Scrapping com Selenium 
    - Limpeza e normalização do conteúdo textual  

    **Índices**
    - Hawk–Dove: direção da postura monetária  
    - Incerteza: grau de cautela e risco no discurso  
    - Alinhamento: coerência entre discurso passado e decisão futura  

    **Limitações**
    - Os índices são baseados em dicionários textuais  
    - O alinhamento é modelo-dependente  
    - O projeto não busca identificar causalidade  
    """)


elif page == "Contato":
    st.markdown("---")
    st.markdown("Autor: **Alef Ryan Silvino Brasil**")
    st.markdown("Contato: **arsb2@academico.com.br**")
    
