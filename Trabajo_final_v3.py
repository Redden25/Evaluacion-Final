#Se importan las librerías necesarias
import streamlit as st
import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
import plotly.express as px

#Permite poner el ícono de cine en el visualizador de pestaña 
título_ventana = "Alva Cciara_Trabajo Final"
emoji_ventana = ":clapper:"
st.set_page_config(page_title=título_ventana, page_icon=emoji_ventana, layout="wide")

#Se escoge los colores para la página
# Fondo: stAppViewContainer
# Header: stHeader
# Barra lateral: stSidebar
# Selectores: select
# h1, h2, h3: Todos los subtítulos

estilos = """
<style>
[data-testid="stAppViewContainer"] {background-color: #292828;}
[data-testid="stHeader"] {background-color: #292828;}

h1, h2, h3 {color: #c95353;}

.stSelectbox > label {color: #FFFFFF;}

div[data-baseweb="select"] > div{
background-color: #222222;
border-color: #292828;
color: #FFFFFF;
}

</style>
"""
color_texto = "#FFFFFF"

#Se asignan los colores a la página
st.markdown(estilos,unsafe_allow_html=True)

# ----------------------------------- Lectura de datos -----------------------------------

#Se puede leer el excel
df = pd.read_excel("database.xlsx")
df.set_index("ID")

#Se guardan los nombres alternativos de la columna para llamarlos al castellano
nombre_columnas = {
    "Title": "Título",
    "Genre": "Género",
    "Description": "Descripción",
    "Actors": "Actores",
    "Year": "Año",
    "Runtime (Minutes)": "Duración (min)",
    "Votes": "Votos",
    "Revenue_shortM": "Recaudación (millones de dólares)",
    "Revenue_full": "Recaudación Total",
    "Metascore": "Metascore",
    "Production_Country": "Países de producción",
    "Filming_Location": "Lugar de filmación representativo",
    "Production_Studio": "Estudios de producción",
    "Studio_1": "Estudio principal"
}

# ----------------------------------- Introducción -----------------------------------

#Se asigna el título
titulo = "CineMetrics"
st.markdown(f"<h1 style='text-align: justify; font-weight: bold'>{titulo}</h1", unsafe_allow_html=True)

#Se aplica diseño al parrafo introductorio
texto_introductorio = "Introducción"
st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_introductorio}</div><br>", unsafe_allow_html=True)

#Muestra de manera preliminar la data a utilizar. Son los cinco primeros que aparecen el database
st.dataframe(df.head(5).rename(columns=nombre_columnas), hide_index=True)

texto_1 = """En un mundo donde el cine no solo es una forma de entretenimiento sino también una industria multimillonaria, la capacidad de analizar y comprender las tendencias de revenue es importante. Estudios y productoras de cine, necesitan datos precisos detrás del éxito de diferentes géneros cinematográficos, para tomar decisiones informadas sobre futuras producciones y estrategias de lanzamiento. Del mismo modo, los fans del cine disfrutan explorando y comparando el éxito de sus géneros y películas favoritas. Por estos motivos, a continuación, se presenta un visualizador de datos sobre el revenue de diferentes películas distribuidas por género, metascore, director y país de origen."""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_1}</div><br>", unsafe_allow_html=True)

#Se crean columnas. El [2,1] hace que una columna sea más ancha que la primera
col1, col2 = st.columns([2,1])

# # ----------------------------------- Gráfico de barras estático -----------------------------------

#Se quitan las filas donde el revenue está vacío
df_norev = df.dropna(subset=["Revenue_full"])

#Separa el valor género en partes lógicas para filtrar de manera más eficiente la información
df_expandido = df_norev.assign(Genre=df_norev["Genre"].str.split(',')).explode("Genre")

#Se agrupan los generos por las variables revenue_full y revenue_shortM de manera independiente y al final se orden de mayor a menor.
revenue_gen = df_expandido.groupby("Genre")["Revenue_shortM"].sum().reset_index().sort_values(by="Revenue_shortM", ascending=False)
revenue_gen_f = df_expandido.groupby("Genre")["Revenue_full"].sum().reset_index().sort_values(by="Revenue_full", ascending=False)

#Se inserta un gráfico de barras
color_elementos_1 = "white"
color_barras = "lightblue"

fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(revenue_gen["Genre"], revenue_gen["Revenue_shortM"], color=color_barras)

ax.set_title("Recaudación Total por género de película (2006-2016)", color=color_elementos_1, fontsize=15)
ax.set_xlabel("Género", color=color_elementos_1, fontsize=12)
ax.set_ylabel("Recaudación Total (millones de dólares)", color=color_elementos_1, fontsize=12)

ax.tick_params(axis="x", colors=color_elementos_1, labelrotation=45)
ax.tick_params(axis="y", colors=color_elementos_1)

ax.spines["left"].set_color(color_elementos_1)
ax.spines["right"].set_color(color_elementos_1)
ax.spines["top"].set_color(color_elementos_1)
ax.spines["bottom"].set_color(color_elementos_1)

#Se guarda como trasparente para que tenga fondo blanco y se muestra la figura.
fig.savefig("fig1_barras.png", transparent=True)
col1.image("fig1_barras.png")

# # ----------------------------------- Lista de recaudaciones -----------------------------------

#Cambia el formato de revenue_full para que aparezca con el símbolo US$ y que tenga dos decimales
revenue_gen_f["Revenue_full"] = revenue_gen_f["Revenue_full"].apply(lambda x: f"US$  {x:,.2f}")

#Se manda el dataframe de revenues
col2.markdown("<br><br>", unsafe_allow_html=True)
col2.dataframe(revenue_gen_f.rename(columns=nombre_columnas), hide_index=True, width=350)

texto_2 = """A través del siguiente gráfico, podemos observar la recaudación total por género, mostrando que las películas de acción son quienes más recaudan y las de género musical quienes menos."""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_2}</div><br>", unsafe_allow_html=True)

#Una divisón entre zonas de la página. Tiene fin estético
st.divider()

# ----------------------------------- Sección 1 -----------------------------------

seccion_1 = "Escoje tu género favorito..."
st.markdown(f"<h2 style='text-align: justify; font-weight: bold'>{seccion_1}</h2>", unsafe_allow_html=True)

texto_3 = """Del género escojido se analizará su Top 10 películas con mayor revenue y su relación con la puntuación máxima en Metascore"""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_3}</div><br>", unsafe_allow_html=True)

# # ----------------------------------- Selector por género -----------------------------------

#Se crea una lista de géneros únicos
generos = df["Genre"].str.split(",").explode().unique()

#Se crea la caja de selección para el género
generoSel = st.selectbox("Seleccione un género de película para analizar", py.sort(generos))

#Se quitan las filas donde el revenue y el metascore están vacíos 
df_noempty = df.dropna(subset=["Revenue_full", "Metascore"])

#Un dataframe filtrado por el génerop seleccionado. apply(lambda x: generoSel in x.split(',')) = permite buscar cada género separado por comas
df_gen = df_noempty[df_noempty["Genre"].apply(lambda x: generoSel in x.split(','))].sort_values(by="Revenue_full", ascending=False)

# # ----------------------------------- Subtítulo 1 -----------------------------------

subtitulo_1 = "TOP 10"
st.markdown(f"<h3 style='text-align: justify; font-weight: bold'>{subtitulo_1}</h3>", unsafe_allow_html=True)

texto_4 = """Aquí puedes ver el nombre de la película con mayor revenue; su sinopsis, director, año, duración y recaudación total."""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_4}</div><br>", unsafe_allow_html=True)

# # # ----------------------------------- Información General -----------------------------------

col3, col4, col5 = st.columns(3)
#Se añaden las imagenes que fueron subidas a Imgur
poster_dict = {
    "Action": "https://i.imgur.com/Pq1z04p.png",
    "Adventure": "https://i.imgur.com/Pq1z04p.png",
    "Animation": "https://i.imgur.com/TwTtdXY.png",
    "Biography": "https://i.imgur.com/AYjyEND.png",
    "Comedy": "https://i.imgur.com/7HbBDaN.png",
    "Crime": "https://i.imgur.com/ovONBjv.png",
    "Drama": "https://i.imgur.com/ovONBjv.png",
    "Family": "https://i.imgur.com/LwgEI2l.png",
    "Fantasy": "https://i.imgur.com/7uRtvyW.png",
    "History": "https://i.imgur.com/PfS3UsK.png",
    "Horror": "https://i.imgur.com/Jy2d3YA.png",
    "Music": "https://i.imgur.com/1JLJw1k.png",
    "Musical": "https://i.imgur.com/O4Nl52v.png",
    "Mystery": "https://i.imgur.com/pGoPb2E.png",
    "Romance": "https://i.imgur.com/UChUND1.png",
    "Sci-Fi": "https://i.imgur.com/jldPU5H.png",
    "Sport": "https://i.imgur.com/Rin1kGC.png",
    "Thriller": "https://i.imgur.com/2Y7s0LS.png",
    "War": "https://i.imgur.com/its0RZw.png",
    "Western": "https://i.imgur.com/31eU9ZD.png"
}
# source: https://imgur.com/a/RGZzIYa

poster = poster_dict[generoSel]

col3.markdown(f"<div style='text-align: center;'><img src=\"{poster}\" style='width: 290px;'></div><br>", unsafe_allow_html=True)
              
#Se le asigna a cada variable el valor de la primera fila de revenue
nombre_Ppelicula = df_gen.iloc[0,df_gen.columns.get_loc("Title")]
desc_Ppelicula = df_gen.iloc[0,df_gen.columns.get_loc("Description")]
director_Ppelicula = df_gen.iloc[0,df_gen.columns.get_loc("Director")]
año_Ppelicula = df_gen.iloc[0,df_gen.columns.get_loc("Year")]
duracion_Ppelicula = df_gen.iloc[0,df_gen.columns.get_loc("Runtime (Minutes)")]
recaudacion_Ppelicula = df_gen.iloc[0,df_gen.columns.get_loc("Revenue_full")]
recaudacion_PpeliculaSM = df_gen.iloc[0,df_gen.columns.get_loc("Revenue_shortM")]
recaudacion_Pformateado = f"US$ {recaudacion_Ppelicula:,.0f}"

#Muestra los datos de la película que recaudó más
col4.markdown(
    f"""
    <div style='font-size:25px; font-weight:bold'>{nombre_Ppelicula}</div><br>
    <div style='font-size:17px; text-align: justify'>{desc_Ppelicula}</div><br>
    <div style='font-size:17px'><strong>Director: </strong>{director_Ppelicula}</div>
    <div style='font-size:17px'><strong>Año: </strong>{año_Ppelicula}</div>
    <div style='font-size:17px'><strong>Duración: </strong>{duracion_Ppelicula} minutos</div><br>
    <div style='font-size:17px; font-weight:bold'>Recaudación:</div>
    <div style='font-size:40px'>{recaudacion_Pformateado}</div>
    """, unsafe_allow_html=True)

#Mostrará las nueve siguiente películas del top. En caso de haber menos, se muestra la totalidad sin romperse la iteración
rango = 9
if len(df_gen) < 9:
    rango = len(df_gen)-1

#Empieza a imprimir elemento por elemento desde la fila dos 
for indice in range(rango):
    i=indice+1
    nombre_Opelicula = df_gen.iloc[i,df_gen.columns.get_loc("Title")]
    recaudacion_Opelicula = df_gen.iloc[i,df_gen.columns.get_loc("Revenue_full")]
    recaudacion_Oformateado = f"US$ {recaudacion_Opelicula:,.0f}"

#Alinea a la derecha la recaudación y el nombre a la izquierda
    col5.markdown(
        f"""
        <div style='display: flex; justify-content: space-between; font-size: 15px;'>
        <span style='text-align: left;'>{i+1}. {nombre_Opelicula}</span>
        <span style='text-align: right;'>{recaudacion_Oformateado}</span>
        </div>
        <br>
        """, unsafe_allow_html=True)
    
# # # ----------------------------------- Gráfico "Scatter Plot" -----------------------------------

color_elementos_2 = "white"
color_puntos = "yellow"
color_grilla = "lightgrey"

fig, ax = plt.subplots(figsize=(15, 10))
ax.scatter(df_gen["Revenue_shortM"], df_gen["Metascore"], color=color_puntos, alpha=0.8)  # Scatter plot

ax.set_xlabel("Recaudación (millones de dólares)", color=color_elementos_2, fontsize=15) 
ax.set_ylabel("Metascore", color=color_elementos_2, fontsize=15)  
ax.set_title("Recaudación vs Metascore (2006 - 2016)", color=color_elementos_2, fontsize=21)  

ax.tick_params(axis="x", colors=color_elementos_2, labelsize=12)
ax.tick_params(axis="y", colors=color_elementos_2, labelsize=12)

ax.spines["left"].set_color(color_elementos_2)
ax.spines["right"].set_color(color_elementos_2)
ax.spines["top"].set_color(color_elementos_2)
ax.spines["bottom"].set_color(color_elementos_2)

#Mostrar una cuadrícula
ax.grid(True, color=color_grilla, linestyle='-', linewidth=0.4)

#Muestra el nombre del que más recaudo y el que tiene el metascore más alto con una flecha
max_metascore_movie = df_gen.loc[df_gen["Metascore"].idxmax(), "Title"]
max_metascore_value = df_gen["Metascore"].max()

ax.annotate(f'{nombre_Ppelicula}', xy=(recaudacion_PpeliculaSM, df_gen.loc[df_gen["Revenue_shortM"].idxmax(), "Metascore"]),
            xytext=(-100, 30), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color=color_elementos_2),color=color_elementos_2, fontsize=12, fontweight='bold')

ax.annotate(f'{max_metascore_movie}', xy=(df_gen.loc[df_gen["Metascore"].idxmax(), "Revenue_shortM"], max_metascore_value),
            xytext=(-100, -30), textcoords='offset points',
            arrowprops=dict(arrowstyle='->', color=color_elementos_2),color=color_elementos_2, fontsize=12, fontweight='bold')

fig.savefig("fig2_scatter.png", transparent=True)
st.image("fig2_scatter.png")

texto_5 = """El presente gráfico hace una comparativa entre la película con mayor recaudación y la mejor valorada en Metascore. Representando como una recaudación exitosa, no significa la valoración positiva del público, ni la calidad del filme. Se entienden los otros puntos en el mapa como lo demás filmes del género"""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_5}</div><br>", unsafe_allow_html=True)

with st.expander("Click para ver los datos completos respecto a los filmes del género"):
    st.dataframe(df_gen.rename(columns=nombre_columnas), hide_index=True)

# # ----------------------------------- Subtítulo 2 -----------------------------------

subtitulo_2 = "Veamos los directores..."
st.markdown(f"<h3 style='text-align: justify; font-weight: bold'>{subtitulo_2}</h3>", unsafe_allow_html=True)

texto_6 = """En el presente gráfico se puede observar entre directores y directoras; los diez nombres con mayor participacón en la creacion de películas del géneero."""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_6}</div><br>", unsafe_allow_html=True)

# # # ----------------------------------- Gráfico de Pastel -----------------------------------

# Calcular la recaudación acumulada por director
revenue_director = df_gen.groupby("Director")["Revenue_full"].sum().reset_index()

# Seleccionar los top 10 directores según la recaudación acumulada
top_directores = revenue_director.nlargest(10, "Revenue_full").rename(columns=nombre_columnas)

#Se añade un gráfico de pastel
fig = px.pie(
    top_directores, 
    values="Recaudación Total", 
    names="Director", 
    title=f"Directores con mayor recaudación total en el género {generoSel} (2006 - 2016)", 
    hole=0.3, 
    color_discrete_sequence=px.colors.sequential.Viridis
)

fig.update_traces(rotation=-90, textfont_size=16, textinfo="percent")
fig.update_layout(
    width=800,
    height=600,
    margin=dict(l=0, r=0, t=50, b=0),
    legend=dict(font=dict(size=16), xanchor="left", x=0.78, yanchor="top", y=0.75),  
    paper_bgcolor="#292828" 
)

with st.container():
    st.plotly_chart(fig, use_container_width=True)

# # # ----------------------------------- Selector por directores -----------------------------------

#Crea un select box para seleccionar el director
directorSel = st.selectbox("Selecciona un director para ver su listado de películas", top_directores["Director"])
director_maxre_mov = df_gen[df_gen["Director"] == directorSel]

#Añade el formato de dólar a la recaudación
director_maxre_mov["Revenue_full"] = director_maxre_mov["Revenue_full"].apply(lambda x: f"US$  {x:,.2f}")
#Se muestra parte de los datos
st.dataframe(director_maxre_mov.rename(columns=nombre_columnas)[["Título", "Género", "Actores", "Año", "Duración (min)", "Recaudación Total", "Metascore", "Países de producción"]], hide_index=True, width=1500)

texto_7 = """Aquí puede visualizar las películas realizas por el director o directora."""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_7}</div><br>", unsafe_allow_html=True)

# # ----------------------------------- Subtítulo 3 -----------------------------------

subtitulo_3 = "Ahora veamos por país y estudio de producción..."
st.markdown(f"<h3 style='text-align: justify; font-weight: bold'>{subtitulo_3}</h3>", unsafe_allow_html=True)

texto_8 = """En el presente gráfico se puede apreciar la distribución por país en la creación de filmes del género escogido y la casa productora. Además, la recaudación por cada una."""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_8}</div><br>", unsafe_allow_html=True)

# # # ----------------------------------- Gráfico Treemap -----------------------------------

#Separa los países de producción en partes lógicas para filtrar de manera más eficiente la información
df_expandido_pc = df_gen.assign(Production_Country=df_gen["Production_Country"].str.split(',')).explode("Production_Country")
revenue_paisprod = df_expandido_pc.groupby(["Production_Country", "Studio_1"])["Revenue_full"].sum().reset_index()

#Eligue el top ocho de estudios por cada país
top_estudios = revenue_paisprod.groupby('Production_Country').apply(lambda x: x.nlargest(8, 'Revenue_full')).reset_index(drop=True)

color_treemap = "deep"

fig = px.treemap(
    top_estudios, 
    path=[px.Constant("World"), "Production_Country", "Studio_1"], 
    values="Revenue_full",
    color="Revenue_full",
    color_continuous_scale=color_treemap,
    title=f"Distribución de la recaudación por país de producción y estudio en el género {generoSel} (2006 - 2016)"
)

fig.update_traces(textfont_size=16, textinfo="label+value")
fig.update_layout(
    coloraxis_colorbar=dict(title="Recaudación US$"), 
    height=800, 
    paper_bgcolor="#292828"
)

fig.layout.hovermode = False
st.plotly_chart(fig)

texto_9 = """"""

st.markdown(f"<div style='text-align: justify; font-size: 18px; color: {color_texto}'>{texto_9}</div><br>", unsafe_allow_html=True)

# # # ----------------------------------- Selector por país de producción -----------------------------------

#Selector por país
paisSel = st.selectbox("Selecciona un país para ver el listado total de películas", top_estudios["Production_Country"].unique())
pais_maxre = df_gen[df_gen["Production_Country"].str.contains(paisSel)]

pais_maxre["Revenue_full"] = pais_maxre["Revenue_full"].apply(lambda x: f"US$  {x:,.2f}")
st.dataframe(pais_maxre.rename(columns=nombre_columnas)[["Título", "Género", "Año", "Recaudación Total", "Metascore", "Países de producción", "Estudio principal" ]], hide_index=True, width=1500)


