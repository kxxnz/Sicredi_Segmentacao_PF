import plotly.express as px
import plotly.graph_objects as go

COLOR_SCHEME = ['#2A4C7D', '#3E7CB1', '#5CA4A9', '#87BBA2']

def plot_segment_distribution(df):
    fig = px.sunburst(
        df,
        path=['Segmento_PF', 'Canal_Atendimento'],
        color='Segmento_PF',
        color_discrete_sequence=COLOR_SCHEME,
        width=800,
        height=600
    )
    fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    return fig

def grafico_medias_segmentos(dados, theme):
    fig = px.bar(
        dados,
        x='Segmento_PF',
        y='Investimentos',
        color='Segmento_PF',
        color_discrete_sequence=theme['chart_colors']
    )
    fig.update_layout(
        paper_bgcolor=theme['background'],
        plot_bgcolor=theme['card_background'],
        font=dict(color=theme['text'])
    )
    return fig

def grafico_boxplots(dados, theme):
    fig = px.box(
        dados,
        x='Segmento_PF',
        y='Investimentos',
        color='Segmento_PF',
        color_discrete_sequence=theme['chart_colors']
    )
    fig.update_layout(
        paper_bgcolor=theme['background'],
        plot_bgcolor=theme['card_background'],
        font=dict(color=theme['text'])
    )
    return fig

def grafico_importancia(modelo, features):
    importancia = modelo.feature_importances_
    fig = px.bar(
        x=features,
        y=importancia,
        labels={'x': 'Variáveis', 'y': 'Importância'},
        color=importancia,
        color_continuous_scale=COLOR_SCHEME
    )
    fig.update_layout(
        title_text="Importância das Variáveis",
        showlegend=False,
        height=300
    )
    return fig