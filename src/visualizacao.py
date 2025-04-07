import plotly.express as px
import plotly.graph_objects as go

# Atualização do esquema de cores
COLOR_SCHEME = ['#CC092F', '#005FAB', '#87BBA2', '#5CA4A9']  # Vermelho Sicredi e Azul Sicredi
TEXT_COLOR = "#FFFFFF"  # Texto branco para contraste
GRID_COLOR = "#444444"  # Cinza escuro para grids

def plot_segment_distribution(df):
    fig = px.sunburst(
        df,
        path=['Segmento_PF', 'Canal_Atendimento'],
        color='Segmento_PF',
        color_discrete_sequence=COLOR_SCHEME,
        width=800,
        height=600
    )
    fig.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
        plot_bgcolor="#222222",  # Fundo escuro
        paper_bgcolor="#222222",  # Fundo escuro
        font=dict(color=TEXT_COLOR)  # Texto branco
    )
    return fig

def grafico_medias_segmentos(dados, theme="default"):
    # Define themes com base no Manual de Identidade
    themes = {
        "default": {
            "chart_colors": COLOR_SCHEME,
            "background_color": "#222222",  # Fundo escuro
            "grid_color": GRID_COLOR
        },
        "light": {
            "chart_colors": COLOR_SCHEME,
            "background_color": "#FFFFFF",
            "grid_color": "#E5E5E5"
        }
    }

    # Ensure the theme is a valid dictionary
    if isinstance(theme, str):
        theme = themes.get(theme, themes["default"])

    # Use the theme dictionary for styling
    fig = px.bar(
        dados,
        x="Segmento_PF",
        y="Renda_Mensal",
        color="Segmento_PF",
        color_discrete_sequence=theme['chart_colors']
    )
    fig.update_layout(
        plot_bgcolor=theme['background_color'],
        paper_bgcolor=theme['background_color'],
        xaxis=dict(gridcolor=theme['grid_color']),
        yaxis=dict(gridcolor=theme['grid_color']),
        font=dict(color=TEXT_COLOR)  # Texto branco
    )
    return fig

def grafico_boxplots(dados, theme="default"):
    # Define themes com base no Manual de Identidade
    themes = {
        "default": {"chart_colors": COLOR_SCHEME},
        "light": {"chart_colors": COLOR_SCHEME},
    }

    # Ensure theme is a dictionary
    if isinstance(theme, str):
        theme = themes.get(theme, themes["default"])

    fig = px.box(
        dados,
        x="Segmento_PF",
        y="Investimentos",
        color="Segmento_PF",
        color_discrete_sequence=theme['chart_colors']
    )
    fig.update_layout(
        plot_bgcolor="#222222",  # Fundo escuro
        paper_bgcolor="#222222",  # Fundo escuro
        font=dict(color=TEXT_COLOR)  # Texto branco
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
        height=300,
        plot_bgcolor="#222222",  # Fundo escuro
        paper_bgcolor="#222222",  # Fundo escuro
        font=dict(color=TEXT_COLOR)  # Texto branco
    )
    return fig