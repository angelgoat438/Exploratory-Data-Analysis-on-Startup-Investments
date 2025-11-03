import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def grafico_ciudades (df_graf):
    fig = px.scatter_mapbox(
        df_graf,
        lat="lat",
        lon="lon",
        hover_name="ciudad",
        hover_data=["pais"],
        color="pais",           # Colorea por país
        size_max=80,            # Tamaño máximo de los puntos
        zoom=2, 
        width=500,              # Nivel de zoom inicial (1 = vista global)
        height=400
        
    )

    fig.update_layout(
        mapbox_style="open-street-map",   # Mapa limpio y profesional
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig 

# numero de exitos por pais -----------------------------------------------

def numero_exitos(df):

    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=(5,4))  # Crear figura y ejes
    sns.barplot(
        data=df,
        x="country_code",
        y="count",
        hue="status",
        palette={"success":"#45CF38","fail":"#CC2D2D"},
        ax=ax
    )
    ax.set_title("Nº éxitos vs fracasos")
    ax.set_xlabel("Países")
    ax.set_ylabel("Nº Empresas")
    ax.tick_params(axis='x', rotation=45)
    return fig

# Tipo de financiación por país --------------------------------------------
def tipo_finanzacion(df):
    fig = px.bar(
    df,
    x="country_code",
    y="Millones USD",
    color="Tipo de inversión",
    color_discrete_map={
        "angel": "#38C2CF",  # verde
        "grant": "#1D42C5"   # rojo
    },
    title="Inversiones por país (Millones $)",
    width=600,
    height=400
)
    return fig

# Industrias más exitosas ----------------------------------------------------

def sector_exitoso(df):
   
    sns.set_style("whitegrid")
    
    fig, ax = plt.subplots(figsize=(4,3))  
    
    sns.boxplot(
        data=df,
        x="market",
        y="funding_total_usd",
        palette="crest",
        hue="market",
        legend=False,
        ax=ax
    )
    ax.set_yscale("log")  # Escala logaritmica
    ax.set_title("Sectores más volumne de financiación")
    ax.set_xlabel("Tipo mercado")
    ax.set_ylabel("Financiación adquirida (USD)")
    ax.tick_params(axis='x', rotation=45)
    
    return fig

# Que pais tiene la industria más exitosa ?
def locoliza_exitosa (df):
    fig = px.pie(
        df, 
        names='country_code',             
        values='count',                 
        title='Startups exitosas en Biotecnología por país',
        width= 600,
        height= 500,
        color_discrete_sequence=px.colors.diverging.RdBu_r
        
    )
    fig.update_traces(textinfo='percent+label', pull=[0.05, 0.05, 0.05, 0.05])

    return fig

# Influyen el numero de rondas ?

def rondas_financiacion(df_pivot):
    
    # Crear figura y eje
    fig, ax = plt.subplots(figsize=(5,3.5))

    # Gráfico de barras apiladas
    df_pivot.plot(
        kind="bar", 
        stacked=True, 
        ax=ax, 
        color=["cornflowerblue", "skyblue"]
    )

    # Títulos y etiquetas
    ax.set_title("Número de empresas por rondas de financiación y estado", fontsize=14, fontweight='bold')
    ax.set_xlabel("Número de rondas", fontsize=12)
    ax.set_ylabel("Cantidad de empresas", fontsize=12)
    ax.legend(title="Status")
    ax.tick_params(axis='x', rotation=0)

    # Bordes más marcados
    for spine in ax.spines.values():
        spine.set_color('black')   
        spine.set_linewidth(1.5)

    return fig