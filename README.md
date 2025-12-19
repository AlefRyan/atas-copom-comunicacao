# Copom Communication Dashboard

Este projeto constrói indicadores quantitativos a partir das atas do Comitê de Política Monetária (Copom) do Banco Central do Brasil, com o objetivo de analisar a comunicação de política monetária ao longo do tempo.

O foco do projeto é transformar o conteúdo textual das atas em medidas numéricas que permitam avaliar:

- a postura monetária comunicada,
- o grau de incerteza do discurso,
- o alinhamento entre comunicação e decisão de política monetária.

---

## 📊 Indicadores Construídos

### Índice Hawk–Dove (HD)

Resume a **direção da postura monetária** implícita na comunicação do Copom.

- Valores positivos indicam viés mais hawkish.
- Valores negativos indicam viés mais dovish.

### Índice de Incerteza Comunicacional

Mede o **grau de cautela, risco e condicionalidade** presente no discurso do Copom.
Picos de incerteza tendem a ocorrer em períodos de crise ou transição de regime.

### Alinhamento Discurso–Ação

Mede o **desalinhamento entre a orientação implícita no discurso de uma ata e a decisão efetiva de política monetária na reunião seguinte**, com base exclusivamente na comunicação textual.

Este indicador não busca avaliar acertos ou erros de política monetária, mas sim identificar episódios de maior ou menor coerência entre discurso e ação.

---

## 🗂️ Dados

- **Fonte:** Banco Central do Brasil
- **Documentos:** Atas das reuniões do Copom
- **Periodicidade:** Reuniões ordinárias e extraordinárias

A coleta dos documentos, extração do texto e limpeza foram realizadas **offline**, antes da etapa de análise e visualização.

---

## ⚙️ Metodologia (resumo)

1. Coleta das atas no site oficial do Banco Central, com Selenium
2. Extração e limpeza do texto
3. Construção de dicionários textuais para postura e incerteza
4. Cálculo dos índices por reunião
5. Visualização interativa via Streamlit

O modelo é deliberadamente parcimonioso, com foco no conteúdo informacional da comunicação, e não busca identificar relações causais.

---

## 🖥️ Aplicação

O projeto inclui uma aplicação interativa desenvolvida em **Streamlit**, que permite visualizar os indicadores ao longo do tempo.

Para rodar localmente:

```bash
pip install -r requirements.txt
streamlit run app.py
```
