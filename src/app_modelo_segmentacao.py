import streamlit as st

# ---- Configuração Inicial ----
st.set_page_config(
    page_title="Segmentação PF | Sicredi Vanguarda",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn import tree
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
import sys
from pathlib import Path
from theme import THEME_LIGHT, THEME_DARK

# Adiciona o diretório pai ao caminho de importação
current_dir = Path(__file__).parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

# Ensure 'warning' key exists in the theme dictionaries
THEME_LIGHT['warning'] = '#FFA500'  # Example: Orange color for warnings
THEME_DARK['warning'] = '#FF4500'   # Example: Darker orange for warnings

# Ensure 'success' key exists in the theme dictionaries
THEME_LIGHT['success'] = '#28a745'  # Example: Green color for success
THEME_DARK['success'] = '#218838'   # Example: Darker green for success

# Configurações de tema e layout
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

def toggle_theme():
    st.session_state['theme'] = 'dark' if st.session_state['theme'] == 'light' else 'light'

current_theme = THEME_LIGHT if st.session_state['theme'] == 'light' else THEME_DARK

st.sidebar.button(
    "Alternar Tema 🌗",
    on_click=toggle_theme,
    help="Alterne entre os modos claro e escuro"
)

st.markdown(f"""
<style>
    body {{
        background-color: {current_theme['background']};
        color: {current_theme['text']};
        font-family: 'Open Sans', sans-serif;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Montserrat', sans-serif;
    }}
    .css-1vq4p4l {{
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: {current_theme['card_background']};
    }}
    .metric-card:hover {{
        transform: scale(1.02);
        transition: all 0.2s ease-in-out;
    }}
</style>
""", unsafe_allow_html=True)

# ---- Header com Logo ----
logo_path = "c:/Users/João P. Reis/Desktop/Sicredi_Segmentacao_PF/assets/sicredi_logo.png"
try:
    st.sidebar.image(logo_path, use_container_width=True)
except FileNotFoundError:
    st.sidebar.error("Erro: Logo não encontrado. Verifique o caminho do arquivo.")

st.sidebar.markdown(f"<h3 style='color: {current_theme['primary']};'>Segmentação PF</h3>", unsafe_allow_html=True)

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
st.title("🔍 Análise de Segmentação de Clientes PF")
st.markdown(f"""
<div style="border-left: 4px solid {current_theme['primary']}; padding-left: 1rem; margin: 1rem 0;">
    Explore os padrões de comportamento e simule cenários de classificação de clientes
</div>
""", unsafe_allow_html=True)

# Métricas Resumo
with st.container():
    cols = st.columns(4)
    metrics = [
        ("Total Clientes", len(dados_clientes), None),
        ("Canal Físico", dados_clientes[dados_clientes['Canal_Atendimento'] == 'Agência'].shape[0], "+12%"),
        ("Canal Digital", dados_clientes[dados_clientes['Canal_Atendimento'] == 'Digital'].shape[0], "-4%"),
        ("Invest. Médio", f"R${dados_clientes['Investimentos'].mean():.2f}", "±0.5%")
    ]
    
    for col, (title, value, variation) in zip(cols, metrics):
        with col:
            def create_metric_card(title, value, variation):
                st.markdown(f"""
                <div class="metric-card" style="padding: 1rem; text-align: center; border: 1px solid {current_theme['border']};">
                    <h4 style="margin: 0; color: {current_theme['primary']};">{title}</h4>
                    <p style="font-size: 1.5rem; margin: 0; color: {current_theme['text']};">{value}</p>
                    <small style="color: {current_theme['secondary']};">{variation if variation else ''}</small>
                </div>
                """, unsafe_allow_html=True)
            
            create_metric_card(title, value, variation)
            st.metric(label=title, value=value, delta=variation)

# Abas Principais
aba1, aba2, aba3, aba4 = st.tabs([
    "🌍 Análise Geográfica", 
    "🤖 Classificação Automática", 
    "⚙️ Engrenagem do Modelo",
    "🎮 Simulador Interativo"
])

# Aba 1 - Análise Geográfica
with aba1:
    st.header("Análise por Localização Geográfica")
    
    with st.expander("🔍 Filtros Avançados", expanded=True):
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
                fig = grafico_medias_segmentos(dados_filtrados, current_theme)
                st.plotly_chart(fig, use_container_width=True)
            with tab2:
                fig = grafico_boxplots(dados_filtrados, current_theme)
                st.plotly_chart(fig, use_container_width=True)

# Aba 2 - Modelo Preditivo
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
                <div style="padding: 1.5rem; background: {current_theme['success']}15; border-radius: 10px; margin-top: 1rem;">
                    <h3 style="color: {current_theme['success']}; margin: 0 0 0.5rem 0;">Resultado:</h3>
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
                color_discrete_sequence=current_theme['chart_colors'],
                hover_data=['Regiao'],
                title="Posicionamento no Contexto Geral"
            )
            fig.update_layout(
                paper_bgcolor=current_theme['background'],
                plot_bgcolor=current_theme['card_background'],
                font=dict(color=current_theme['text'])
            )
            fig.add_trace(go.Scatter(
                x=[nova_renda],
                y=[novo_investimento],
                mode='markers',
                marker=dict(color=current_theme['accent'], size=12),
                name='Cliente Simulado'
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div style="padding: 1.5rem; background: {current_theme['warning']}15; border-radius: 10px;">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: {current_theme['text']};">Classificação</h4>
                        <div class="segment-badge">{segmento}</div>
                    </div>
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: {current_theme['text']};">Canal Ideal</h4>
                        <div class="segment-badge" style="background: {current_theme['accent']}20; color: {current_theme['accent']};">{canal}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ---- Sidebar com informações ----
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1rem; background: {current_theme['primary']}10; border-radius: 10px;">
        <h3 style="color: {current_theme['primary']};">ℹ️ Como usar</h3>
        <ol style="margin: 0; padding-left: 1rem;">
            <li>Selecione a aba de análise desejada</li>
            <li>Ajuste os filtros conforme necessário</li>
            <li>Interaja com os gráficos para detalhes</li>
            <li>Use o simulador para cenários hipotéticos</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**🔧 Última atualização:**\n\n2024-05-20")
    st.markdown("**📦 Versão do modelo:**\n\n1.2.0-rc1")
    st.markdown("**🧠 Algoritmo:**\n\nÁrvore de Decisão (Profundidade=5)")

if __name__ == "__main__":
    pass