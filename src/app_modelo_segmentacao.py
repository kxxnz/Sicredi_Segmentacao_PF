import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.tree import export_text
from dados import gerar_dados
from classificacao import classificar_pf, definir_canal
from modelos import preparar_dados_modelo, treinar_modelo_arvore, avaliar_modelo
from visualizacao import (
    plot_segment_distribution,
    grafico_medias_segmentos,
    grafico_boxplots,
    grafico_importancia
)
from pathlib import Path
import sys

# ---- Configuração Inicial ----
st.set_page_config(
    page_title="Segmentação PF | Sicredi Vanguarda",
    page_icon="📈",
    layout="wide"
)

# Adiciona o diretório pai ao caminho de importação
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

# ---- Importação de fontes e estilos ----
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
    body {
        background-color: #1C1C1C; /* Fundo escuro */
        font-family: 'Open Sans', sans-serif; /* Tipografia padrão */
        color: #FFFFFF; /* Texto branco */
    }
    h1, h2, h3, h4 {
        font-family: 'Open Sans', sans-serif;
        color: #CC092F; /* Vermelho Sicredi */
    }
    .header {
        background-color: #005FAB; /* Azul Sicredi */
        padding: 20px 40px;
        border-bottom: 3px solid #CC092F;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 1000;
        display: flex;
        align-items: center;
    }
    .header img {
        height: 60px;
    }
    .card {
        background-color: #2E2E2E; /* Fundo dos cards */
        border-radius: 10px;
        padding: 20px;
        margin: 30px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .button {
        background-color: #CC092F;
        color: #FFFFFF;
        border: none;
        padding: 12px 25px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button:hover {
        background-color: #005FAB;
    }
    .segment-badge {
        background-color: #005FAB;
        color: #FFFFFF;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 14px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ---- Funções e Dados ----
@st.cache_data
def load_data():
    dados = gerar_dados(n=1000)
    dados['Segmento_PF'] = dados.apply(
        lambda x: classificar_pf(x['Renda_Mensal'], x['Investimentos']), axis=1
    )
    dados['Canal_Atendimento'] = dados['Segmento_PF'].apply(definir_canal)
    return dados

dados_clientes = load_data()

# ---- Interface Principal ----
st.title("Análise de Segmentação de Clientes PF")
st.markdown("""
<div class="card">
    <p>Explore os padrões de comportamento e simule cenários de classificação de clientes.</p>
</div>
""", unsafe_allow_html=True)

# ---- Abas Principais ----
aba1, aba2, aba3, aba4 = st.tabs([
    "Análise Geográfica", 
    "Classificação Automática", 
    "Engrenagem do Modelo",
    "Simulador Interativo"
])

# Aba 1 - Análise Geográfica
with aba1:
    st.header("Análise por Localização Geográfica")
    with st.expander("Filtros Avançados", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            regiao = st.selectbox("Região:", options=sorted(dados_clientes['Regiao'].unique()))
        with col2:
            segmentos = st.multiselect("Segmentos:", options=dados_clientes['Segmento_PF'].unique(),
                                        default=dados_clientes['Segmento_PF'].unique())
        with col3:
            canal = st.multiselect("Canal:", options=dados_clientes['Canal_Atendimento'].unique(),
                                    default=dados_clientes['Canal_Atendimento'].unique())

    dados_filtrados = dados_clientes[
        (dados_clientes['Regiao'] == regiao) &
        (dados_clientes['Segmento_PF'].isin(segmentos)) &
        (dados_clientes['Canal_Atendimento'].isin(canal))
    ]

    with st.container():
        col_viz1, col_viz2 = st.columns([1, 2])
        with col_viz1:
            st.subheader("Distribuição Hierárquica")
            plot_segment_distribution(dados_filtrados)

        with col_viz2:
            st.subheader("Comparativo Financeiro")
            tab1, tab2 = st.tabs(["Médias", "Distribuição"])
            with tab1:
                fig = grafico_medias_segmentos(dados_filtrados, theme="default")  # Added 'theme' argument
                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                fig = grafico_boxplots(dados_filtrados, theme="default")  # Added 'theme' argument
                st.plotly_chart(fig, use_container_width=True)

# Aba 2 - Classificação Automática
with aba2:
    st.header("Classificação Automática por Machine Learning")
    if 'modelo' not in st.session_state:
        X_treino, X_teste, y_treino, y_teste, encoder = preparar_dados_modelo(
            dados_clientes,
            ['Renda_Mensal', 'Investimentos'],
            'Segmento_PF'
        )
        modelo = treinar_modelo_arvore(X_treino, y_treino)
        st.session_state.update({
            'modelo': modelo,
            'encoder': encoder,
            'X_teste': X_teste,
            'y_teste': y_teste
        })

    with st.container():
        col_model1, col_model2 = st.columns([2, 1])

        with col_model1:
            st.subheader("Teste o Modelo")
            with st.form(key='prediction_form'):
                c1, c2 = st.columns(2)
                with c1:
                    renda = st.slider("Renda Mensal (R$)", 500, 20000, 3500, step=100,
                                      help="Valor líquido após descontos")
                with c2:
                    investimento = st.slider("Investimentos (R$)", 0, 500000, 50000, step=1000,
                                             help="Total acumulado em produtos de investimento")

                if st.form_submit_button("Executar Classificação"):
                    previsao = st.session_state.modelo.predict([[renda, investimento]])
                    segmento = st.session_state.encoder.inverse_transform(previsao)[0]
                    st.session_state.resultado = segmento

            if 'resultado' in st.session_state:
                st.markdown(f"""
                <div style="padding: 1.5rem; background: #DFF0D8; border-radius: 10px; margin-top: 1rem;">
                    <h3 style="color: #3C763D; margin: 0 0 0.5rem 0;">Resultado:</h3>
                    <div class="segment-badge">{st.session_state.resultado}</div>
                    <p style="margin: 0.5rem 0 0 0;">Canal recomendado: <strong>{definir_canal(st.session_state.resultado)}</strong></p>
                </div>
                """, unsafe_allow_html=True)

        with col_model2:
            st.subheader("Desempenho")
            report, cm, rules = avaliar_modelo(
                st.session_state.modelo,
                st.session_state.X_teste,
                st.session_state.y_teste,
                st.session_state.encoder
            )

            st.metric("Acurácia Geral", f"{round(float(report.split()[-4]), 2)}%")
            st.write("**Matriz de Confusão:**")
            st.dataframe(pd.DataFrame(cm,
                                      columns=st.session_state.encoder.classes_,
                                      index=st.session_state.encoder.classes_
                                      ), use_container_width=True)

# Aba 3 - Detalhes do Modelo
with aba3:
    st.header("Arquitetura do Modelo de Classificação")
    with st.container():
        col_det1, col_det2 = st.columns([1, 1])

        with col_det1:
            st.subheader("Árvore de Decisão")
            tree_rules = export_text(
                st.session_state.modelo,
                feature_names=['Renda_Mensal', 'Investimentos'],
                class_names=st.session_state.encoder.classes_
            )
            st.code(tree_rules, language='text')

        with col_det2:
            st.subheader("Importância das Variáveis")
            fig = grafico_importancia(
                st.session_state.modelo,
                ['Renda_Mensal', 'Investimentos']
            )
            st.plotly_chart(fig, use_container_width=True)

# Aba 4 - Simulador
with aba4:
    st.header("Simulação de Cenários")
    with st.container():
        col_sim1, col_sim2 = st.columns([2, 3])

        with col_sim1:
            st.subheader("Parâmetros")
            nova_renda = st.slider(
                "Renda Mensal Simulada (R$)",
                500, 20000, 6000,
                key="sim_renda",
                help="Projeção de renda líquida mensal"
            )
            novo_investimento = st.slider(
                "Projeção de Investimentos (R$)",
                0, 500000, 75000,
                key="sim_invest",
                help="Valor total estimado em investimentos"
            )

        with col_sim2:
            st.subheader("Resultados")
            segmento = classificar_pf(nova_renda, novo_investimento)
            canal = definir_canal(segmento)

            fig = px.scatter(
                dados_clientes,
                x='Renda_Mensal',
                y='Investimentos',
                color='Segmento_PF',
                hover_data=['Regiao'],
                title="Posicionamento no Contexto Geral"
            )
            fig.add_trace(go.Scatter(
                x=[nova_renda],
                y=[novo_investimento],
                mode='markers',
                marker=dict(color='#FF5733', size=12),
                name='Cliente Simulado'
            ))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
            <div style="padding: 1.5rem; background: #FCF8E3; border-radius: 10px;">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #8A6D3B;">Classificação</h4>
                        <div class="segment-badge">{segmento}</div>
                    </div>
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #8A6D3B;">Canal Ideal</h4>
                        <div class="segment-badge" style="background: #FF5733; color: #FFFFFF;">{canal}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---- Responsividade e Acessibilidade ----
st.markdown("""
<script>
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    if (mediaQuery.matches) {
        document.querySelector('.nav-menu').style.flexDirection = 'column';
    }
</script>
""", unsafe_allow_html=True)