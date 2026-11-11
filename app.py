import streamlit as st
import os
from google import genai

# Configuração da página
st.set_page_config(
    page_title="LicenseShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ LicenseShield AI")
st.subheader("Auditor Inteligente de Licenças e Direitos Autorais")
st.write("Analise termos de uso, licenças e contratos para garantir conformidade e evitar avisos de Copyright/Content ID.")

# Barra lateral para chave de API
st.sidebar.header("Configurações")
api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

if not api_key:
    # Tenta carregar dos segredos do ambiente/Streamlit se disponível
    api_key = os.environ.get("GEMINI_API_KEY", "")

# Entrada do Usuário
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Cole o texto da Licença ou Contrato")
    license_text = st.text_area(
        "Insira aqui os termos de uso, texto da licença (CC, Envato, Pixabay, etc.) ou regras do distribuidor:",
        height=250,
        placeholder="Cole o texto legal aqui..."
    )

with col2:
    st.markdown("### 🎯 Contexto de Uso (Opcional)")
    usage_context = st.text_area(
        "Como você pretende usar esse conteúdo?",
        height=250,
        placeholder="Exemplo: Quero usar uma música de fundo num vídeo monetizado do YouTube e alterar o tom do áudio."
    )

analyze_button = st.button("🚀 Analisar Licença e Gerar Relatório", type="primary")

# Lógica de Análise de IA
if analyze_button:
    if not api_key:
        st.error("Por favor, insira uma API Key do Gemini na barra lateral para prosseguir.")
    elif not license_text.strip():
        st.warning("Por favor, insira o texto da licença antes de realizar a análise.")
    else:
        with st.spinner("Analisando termos legais e mapeando riscos de copyright..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Você é um especialista jurídico sênior e auditor de Direitos Autorais, Licenciamento Digital e Creative Commons.
                Análise o seguinte texto de licença/termo e o contexto de uso fornecido.

                --- TEXTO DA LICENÇA ---
                {license_text}

                --- CONTEXTO DE USO DO USUÁRIO ---
                {usage_context if usage_context else 'Uso geral em conteúdo digital.'}

                Forneça um relatório de conformidade em Markdown estritamente no seguinte formato:

                ## 📊 Resumo da Licença
                - **Nome/Tipo da Licença Identificada:** 
                - **Nível de Risco de Copyright/Content ID:** [Baixo 🟢 / Médio 🟡 / Alto 🔴]

                ## ✅ Permissões (O que PODE fazer)
                - Liste em marcadores as ações permitidas.

                ## ⚠️ Restrições e Obrigações (Atenção)
                - Exige atribuição/créditos? Se sim, como?
                - Modificações/Obras derivadas são permitidas?

                ## ❌ Proibições (O que NÃO PODE fazer)
                - Liste em marcadores o que é expressamente proibido (ex: revenda, reivindicar Content ID, uso não comercial).

                ## 📝 Texto Sugerido para Atribuição (Créditos)
                > Crie o texto de crédito pronto para colar na descrição do vídeo/post caso a licença exija.

                ## ⚖️ Parecer Final de Conformidade
                Uma breve conclusão sobre se o uso desejado pelo usuário é seguro ou se há risco legal.
                """

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )

                st.success("Análise concluída com sucesso!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar a análise: {e}")
