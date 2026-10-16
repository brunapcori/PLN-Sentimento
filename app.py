"""
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator

# Configuração da página
st.set_page_config(
    page_title="Analisador de Sentimentos Offline",
    page_icon="🧠",
    layout="centered"
)

# Cabeçalho da aplicação
st.title("🧠 Analisador de Sentimentos Offline")
st.caption(
    "Esta é uma versão 'Offline' (sem APIs proprietárias como OpenAI/Google Cloud) "
    "baseada em bibliotecas tradicionais de PLN em Python (TextBlob)."
)

st.markdown(
    """
    Insira uma frase ou avaliação abaixo para analisar a polaridade do sentimento.  
    *O texto é traduzido em segundo plano para o inglês para garantir máxima precisão com o léxico padrão do **TextBlob**.*
    """
)

# Entrada do usuário
user_text = st.text_area(
    label="Texto para análise:",
    placeholder="Ex.: O atendimento foi excelente, fiquei impressionado com a agilidade!",
    height=140
)

col_btn, _ = st.columns([1, 4])
with col_btn:
    btn_analisar = st.button("Analisar", type="primary", use_container_width=True)

if btn_analisar:
    texto_limpo = user_text.strip()
    
    if not texto_limpo:
        st.warning("⚠️ Por favor, insira algum texto antes de clicar em Analisar.")
    else:
        with st.spinner("Processando texto e calculando polaridade..."):
            try:
                # Tradução invisível para o inglês (língua nativa das regras lexicais do TextBlob)
                tradutor = GoogleTranslator(source="auto", target="en")
                texto_processado = tradutor.translate(texto_limpo)
            except Exception:
                # Fallback defensivo em caso de indisponibilidade momentânea
                texto_processado = texto_limpo

            # Processamento de Linguagem Natural com TextBlob
            blob = TextBlob(texto_processado)
            polaridade = blob.sentiment.polarity
            subjetividade = blob.sentiment.subjectivity

            st.divider()
            st.subheader("Resultado da Análise")

            # Classificação baseada no score de polaridade
            # Limiares: > 0.1 (Positivo), < -0.1 (Negativo), intermediário (Neutro)
            if polaridade > 0.1:
                st.success("✨ **Sentimento Detectado:** Positivo 😊")
            elif polaridade < -0.1:
                st.error("⚠️ **Sentimento Detectado:** Negativo 🙁")
            else:
                st.warning("⚖️ **Sentimento Detectado:** Neutro 😐")

            # Indicadores numéricos complementares
            col_pol, col_sub = st.columns(2)
            with col_pol:
                st.metric(
                    label="Score de Polaridade",
                    value=f"{polaridade:.2f}",
                    help="Varia de -1.0 (totalmente negativo) a +1.0 (totalmente positivo)."
                )
            with col_sub:
                st.metric(
                    label="Nível de Subjetividade",
                    value=f"{subjetividade:.2f}",
                    help="Varia de 0.0 (fato puramente objetivo) a 1.0 (opinião puramente subjetiva)."
                )
