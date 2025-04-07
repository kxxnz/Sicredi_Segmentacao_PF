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

def grafico_medias_segmentos(df):
    df_agg = df.groupby('Segmento_PF')[['Renda_Mensal', 'Investimentos']].mean().reset_index()
    fig = px.bar(df_agg,
                 x='Segmento_PF',
                 y=['Renda_Mensal', 'Investimentos'],
                 barmode='group',
                 color_discrete_sequence=COLOR_SCHEME[:2])
    return fig

def grafico_boxplots(df):
    fig = go.Figure()
    # Boxplot para Renda Mensal
    fig.add_trace(go.Box(y=df['Renda_Mensal'], x=df['Segmento_PF'], name='Renda'))
    # Boxplot para Investimentos
    fig.add_trace(go.Box(y=df['Investimentos'], x=df['Segmento_PF'], name='Investimentos'))
    fig.update_layout(boxmode='group')
    return fig