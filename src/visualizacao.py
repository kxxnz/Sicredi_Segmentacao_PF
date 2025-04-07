import plotly.express as px
import seaborn as sns
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def plot_segment_distribution(df):
    fig = px.sunburst(
        df, 
        path=['Segmento_PF', 'Canal_Atendimento'],  # Nomes corretos das colunas
        color='Segmento_PF',
        color_discrete_sequence=['#2A4C7D', '#3E7CB1', '#5CA4A9', '#87BBA2'],
        width=800,
        height=600
    )
    fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

def grafico_medias_segmentos(df, coluna1='Renda_Mensal', coluna2='Investimentos'):
    media1 = df.groupby('Segmento_PF')[coluna1].mean()
    media2 = df.groupby('Segmento_PF')[coluna2].mean()

    fig, ax = plt.subplots()
    index = np.arange(len(media1))
    bar_width = 0.35

    ax.bar(index, media1, bar_width, alpha=0.8, label=f'{coluna1} Média', color='steelblue')
    ax.bar(index + bar_width, media2, bar_width, alpha=0.8, label=f'{coluna2} Média', color='seagreen')
    ax.set_xlabel('Segmento PF')
    ax.set_ylabel('Valor (R$)')
    ax.set_title(f'Média de {coluna1} e {coluna2} por Segmento')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(media1.index)
    ax.legend()
    return fig

def grafico_boxplots(df):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    sns.boxplot(x='Segmento_PF', y='Renda_Mensal', data=df, palette='Set2', ax=axes[0])
    axes[0].set_title("Renda Mensal por Segmento")
    sns.boxplot(x='Segmento_PF', y='Investimentos', data=df, palette='Set3', ax=axes[1])
    axes[1].set_title("Investimentos por Segmento")
    return fig

def grafico_importancia(importances, features):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(features, importances, color='skyblue')
    ax.set_xlabel("Importância")
    ax.set_title("Importância das Variáveis no Modelo")
    return fig

custom_theme = {
    'secondaryBackgroundColor': '#f0f0f0',
    'primaryColor': '#3498db',
    'textColor': '#2c3e50'
}

def create_metric_card(title, value, variation=None):
    html = f"""
    <div style="
        padding: 20px;
        background: {custom_theme['secondaryBackgroundColor']};
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px;">
        <h3 style="color: {custom_theme['primaryColor']}; margin:0;">{title}</h3>
        <h1 style="color: {custom_theme['textColor']}; margin:0;">{value}</h1>
        {f'<span style="color: #27ae60;">{variation}</span>' if variation else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
