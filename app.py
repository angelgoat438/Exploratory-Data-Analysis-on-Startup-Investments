import streamlit as st
import pandas as pd
import plotly.express as px
from graficas import grafico_ciudades,numero_exitos,tipo_finanzacion,sector_exitoso,locoliza_exitosa,rondas_financiacion
from scipy import stats

df_c = pd.read_csv("df_startup.csv")

st.set_page_config(page_title= "Startapp",page_icon=" 🌃 ",layout="wide")

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        padding: 50px;
        border-radius: 15px;
        text-align: center;
        color: white;
    ">
        <h1 style="font-size: 48px;">🌐 Dashboard de Startups</h1>
        <p style="font-size: 20px;">Análisis ejecutivo de inversiones globales</p>
    </div>
    """,
    unsafe_allow_html=True
)


# INTRODUCCIÓN
with st.container():
    
    st.title("Presentación")

    st.header("El objetivo de este dashboard es dar una visión global y destacar los insights claves para invertir de forma objetiva en Startups")
st.write("")   

# mapa de ciudades ----------------------------------------------

st.header("1.Distribución de Startups")

data = {
    "pais": [
        "USA", "USA", "USA", "USA", "USA",
        "CHINA", "CHINA", "CHINA",
        "GBR", "GBR", "GBR",
        "CAN", "CAN", "CAN"
    ],
    "ciudad": [
        "New York City", "Chicago", "Boston", "SF Bay Area", "Seattle",
        "Beijing", "Shanghai", "Guangzhou",
        "Manchester", "London", "Bath",
        "Ottawa", "Toronto", "Vancouver"
    ],
    "lat": [
        40.71427, 41.881832, 42.361145, 37.828724, 47.608013,
        39.916668, 31.224361, 23.128994,
        53.483959, 51.509865, 51.380001,
        45.424721, 43.651070, 49.246292
    ],
    "lon": [
        -74.00597, -87.623177, -71.057083, -122.355537, -122.335167,
        116.383331, 121.469170, 113.253250,
        -2.244644, -0.118092, -2.360000,
        -75.695000, -79.347015, -123.116226
    ]
}

df_ciudades = pd.DataFrame(data)

fig = grafico_ciudades(df_ciudades)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

print(" ")

# -------------------------------------------------------------------------------------------------

# 2. Gráfico de numero de éxito

st.header("2. Número de éxitos por país")

top_sec = df_c.groupby("country_code")["status"].value_counts().groupby(level=0,).head(5)

top_sec = top_sec.reset_index(name="count")

fig2 = numero_exitos(top_sec)
st.pyplot(fig2, use_container_width= False)

st.write("")
# ---------------------------------------------------------------------------------

# 3. Tipos de financiacion por pais

st.header("3. Que tipo de financión recive cada país?")


# importo un dataframe intermedio--------

df_pp = round(df_c.groupby("country_code")[["angel","grant"]].sum()/1e6,2) # Paso el resultado a millones

df_plot = df_pp.reset_index().melt(id_vars = "country_code",
                                    var_name = "Tipo de inversión",    # Creo el dataframe para poder pintar la gráfica
                                    value_name = "Millones USD")

fig3 = tipo_finanzacion(df_plot)
st.plotly_chart(fig3)

st.write("")
# -----------------------------------------------------------------------------

# 4. Importa la cantidad invertida por un angel o seed

st.header("4. Es relevante recibir una alta inversión inicial?")

df_sa = df_c[["name","status","market","funding_total_usd"]].copy()
df_sa["sum_a_s"] = df_c["angel"] + df_c["seed"]

# Conteos
conteo_s = df_sa[df_sa["status"] == "success"]["sum_a_s"]
conteo_f = df_sa[df_sa["status"] == "fail"]["sum_a_s"]

# Contraste t-test
t_stat, p_valor = stats.ttest_ind(conteo_f, conteo_s, equal_var=True)

col1,col2 = st.columns(2)

with col1:
    st.subheader("Contraste t-test entre éxitos y fracasos")
    st.markdown(f"#### -**T-statistic:** {t_stat:.3f}")
    st.markdown(f"#### -**P-value:** {p_valor:.4f}")

with col2:

# Explicación rápida
    
    st.markdown("#### *Partiendo de un supuesto de error no superior a un **0.05**, se da por rechaza la hipótesis*")
    st.markdown("#### *debido a que el valor que nos devuleve p-valor es superior a nuestro error prestablecido.*")

st.write("")
st.write("")

# 5. Sectores con mayor tasa de éxito --------------------------------------------------

st.header("5. Qué indutria percibe más volumen de financiación ? ")
top_5_e = df_c[df_c["status"] == "success"].groupby("market")["status"].count().sort_values(ascending = False).head(5) #se encuentran los sectores con más numero de empresas exitosas
top_5_m = top_5_e.index

df_top5 = df_c[(df_c["market"].isin(top_5_m)) & (df_c["status"] == "success")]

fig4 = sector_exitoso(df_top5)
st.pyplot(fig4,use_container_width=False)
st.write("")

# 6. que pais tiene la industria más exitosa ? ----------------------------------------------------------------

st.header("6. Qué país tiene la industria con mayor demanda de inversión ? ")

colum1 , colum2 = st.columns(2)

biotx = df_c[(df_c["market"]==" Biotechnology ") & (df_c["status"]=="success")].groupby("country_code")["status"].count().sort_values(ascending= False)
biotx_df = biotx.reset_index() # convierto las serie biotx en df
biotx_df.columns = ['country_code','count']

with colum1:

    fig5 = locoliza_exitosa(biotx_df)
    st.plotly_chart(fig5, use_container_width=False)

with colum2:

    st.write("")
    st.markdown("#### *Se puede observar que en USA se concentran la mayoría de startups Biotecnológicas*")
    st.markdown("#### *Podría tener sentido ya que si nos fijamos, anteriormente tenían el mayor porcentaje de subvenciones*")

st.write("")

# 7. Que una empresa tenga rodaje antes de pedir financiación influye ? ------------------------------

st.header("7. Que una empresa tenga rodaje antes de pedir financiación influye ?")

media_f = df_c[df_c["status"]=="fail"]["years_between"]
media_s = df_c[df_c["status"]=="success"]["years_between"]

# al realizar el test se asume un error del 0.05
t_start,p_value = stats.ttest_ind(media_f,media_s,equal_var= True)

co1 ,co2 = st.columns(2)

with co1:
    distribucion = df_c.groupby("status")["years_between"].mean()
    st.dataframe(distribucion)

with co2:
    st.write("#### *Al observar que habia una diferencia visualmente relevante, se decide aplicar un T-test*")

    st.markdown(f"#### - T-test devuelve: {t_start: .3f}")
    st.markdown(f"#### - P-valor devuelve: {p_valor: .4f}")
    st.write("#### *Se concluye que *SÍ* que existe una relación entre el éxito y los años previos a pedir financiación*")

# 8. el numero de rondas influye en el éxito de la empresa ? ----------------------------------
st.markdown("")
st.header("8. Un alto numero de rondas de financiación tiene correlación con el éxito?")

df_counts = df_c.groupby(["funding_rounds", "status"])["status"].count().reset_index(name="count")

# Pivot para tener status como columnas
df_pivot = df_counts.pivot(index="funding_rounds", columns="status", values="count").fillna(0)

fig6 = rondas_financiacion(df_pivot)
st.pyplot(fig6, use_container_width=False)

# Coclusión final----------------------------------------------------

st.title("Conclusión Final 🧠")

st.markdown("#### **Una vez realizado el estudio de los aspectos más relevates de las características,**")
st.markdown("#### **existe una cierta tendecia de éxito a aquellas empresas que se dedican a Biotecnología y**")
st.markdown("#### **aquellas que tienen un recorrido previo antes de empezar las rondas de financiación**")