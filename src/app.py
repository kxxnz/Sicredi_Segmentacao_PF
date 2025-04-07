import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

COLOR_SCHEME = ['#2A4C7D', '#3E7CB1', '#5CA4A9', '#87BBA2']

def grafico_medias_segmentos(df):
    agg_df = df.groupby('Segmento_PF').agg({
        'Renda_Mensal': 'mean',
        'Investimentos': 'mean'
    }).reset_index()
    
    fig = px.bar(agg_df, 
                 x='Segmento_PF', 
                 y=['Renda_Mensal', 'Investimentos'],
                 barmode='group',
                 color_discrete_sequence=[COLOR_SCHEME[0], COLOR_SCHEME[2]],
                 labels={'value': 'Valor Médio (R$)', 'variable': 'Métrica'},
                 height=400)
    
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def grafico_boxplots(df):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Renda Mensal", "Investimentos"))
    
    for i, col in enumerate(['Renda_Mensal', 'Investimentos']):
        fig.add_trace(
            go.Box(
                y=df[col],
                x=df['Segmento_PF'],
                name=col,
                marker_color=COLOR_SCHEME[i],
                boxpoints='outliers'
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        margin=dict(t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def grafico_importancia(modelo, features):
    importance = modelo.feature_importances_
    fig = px.bar(x=features, y=importance, 
                 labels={'x': 'Variáveis', 'y': 'Importância'},
                 color=importance,
                 color_continuous_scale=[COLOR_SCHEME[1], COLOR_SCHEME[3]])
    
    fig.update_layout(
        title="Relevância das Variáveis na Decisão",
        height=300,
        margin=dict(t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig