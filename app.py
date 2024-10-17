import streamlit as st
import pandas as pd
from itertools import combinations

# Configurações iniciais da página
st.set_page_config(page_title="Campeonato de Karatê", layout="wide")

st.markdown("<h1 style='text-align: center;'>Campeonato de Karatê Shubu-dô</h1>", unsafe_allow_html=True)

image_url = "https://i.ibb.co/NYCJMsm/campeonato.jpg"
# st.image(image_url, width=200)

# Exibe a imagem centralizada
st.markdown(
    f"""
    <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
        <img src="{image_url}" width="250">
    </div>

    """,
    unsafe_allow_html=True
)

# Descrição
st.write("""
#### Informações:
    Campeonato de Luta e Katá  
    Dia: 20/10/2024  
    Horário: a partir das 09:00h  
    Local: Ginásio de Esportes Gurizão  
    Endereço: R. São João, 1042 – Santa Terezinha, Fazenda Rio Grande – PR, 83829-248
""")

# Define o endereço
endereco = "R. São João, 1042 – Santa Terezinha, Fazenda Rio Grande – PR, 83829-248 - Ginásio de Esportes Gurizão "

# Cria a URL do Google Maps com o endereço
google_maps_url = f"https://www.google.com/maps/search/?api=1&query={endereco.replace(' ', '+')}"

# Exibe o link estilizado como um botão
st.markdown(f"""
    <a href="{google_maps_url}" target="_blank" style="text-decoration: none;">
        <button style="
            display: inline-block;
            padding: 0.5em 1em;
            font-size: 1em;
            font-weight: bold;
            color: white;
            background-color: #D0312D;
            border: none;
            border-radius: 0.25em;
            cursor: pointer;
        ">
            Abrir no Google Maps
        </button>
    </a>
""", unsafe_allow_html=True)

st.write("")

# Carregar os dados
@st.cache_data
def load_data(file_path, estilo):
    df = pd.read_csv(file_path)
    df = df[df.estilo == estilo.lower()]
    return df

# Carregar os dados
@st.cache_data
def load_data_completo(file_path):
    df = pd.read_csv(file_path)
    return df

file_path = "df_completo.csv"

estilo = st.radio(
    "Selecione a Modalidade:",
    ["Kata", "Luta"],
    horizontal=True
)
df = load_data_completo(file_path)

atletas_ambos_estilos = df.groupby('atleta').agg({'estilo':'nunique'}).query("estilo > 1").shape[0]

data = load_data(file_path, estilo)

# Listas únicas para filtros, ordenadas
atletas_unicos = sorted(data['atleta'].dropna().unique())
academias_unicas = sorted(data['academia'].dropna().unique())

# Filtros principais, exibidos antes da tabela
st.write("")
academia = st.multiselect("Academia", options=academias_unicas, placeholder='Selecionar Academia')
atleta = st.multiselect("Atleta", options=atletas_unicos, placeholder='Selecionar Atleta')

# Aplicar filtros nos dados
filtered_data = data

if academia:
    filtered_data = filtered_data[filtered_data['academia'].isin(academia)]

if atleta:
    grupos_atleta = data[data['atleta'].isin(atleta)]['categoria'].unique()
    filtered_data = filtered_data[filtered_data['categoria'].isin(grupos_atleta)]

# Exibir tabela de dados filtrados
st.markdown(f"<h2 style='text-align: center; font-size: 28px;'>Tabela Completa de {estilo}s</h2>", unsafe_allow_html=True)
st.write(f"**Selecionados:**", len(filtered_data))
st.dataframe(filtered_data[['categoria', 'atleta', 'local', 'academia', 'faixa']], hide_index=True)

# Estatísticas adicionais
st.markdown("<h2 style='text-align: center; font-size: 28px;'>Estatísticas do Campeonato</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.write("**Total de Atletas:**")
    st.write(
        f"""
        - {df[df.estilo == estilo.lower()].categoria.nunique()} {estilo}s
        - {df[df.estilo == estilo.lower()].atleta.nunique()} atletas participarão do Campeonato de {estilo}. \n
        - {atletas_ambos_estilos} paticiparão de ambas as modalidades, Kata e Luta
        """
    )

with col2:
    st.write("**Distribuição de Atletas por Gênero:**")
    st.write(
        f"""
        - {df[(df.estilo == estilo.lower()) & (df.sexo == 'Masculino')].atleta.nunique()} atletas do sexo Masculino. \n
        - {df[(df.estilo == estilo.lower()) & (df.sexo == 'Feminino')].atleta.nunique()} atletas do sexo Feminino.
        """
    )


col1, col2 = st.columns(2)

with col1:
    st.write("**Quantidade de atletas por academia:**")
    st.write(
        filtered_data.groupby('academia').agg({
            'atleta': 'nunique',
            'categoria': 'nunique'
        }).rename(columns={
            'atleta': 'Atletas',
            'categoria': 'Ouros Possíveis'
        }).sort_values('Atletas', ascending=False)
        
    )

with col2:
    st.write("**Contagem de Confrontos entre Academias**")

    # Agrupa os dados por 'categoria' para obter confrontos entre academias na mesma categoria
    confrontos = []
    for _, grupo in filtered_data.groupby('categoria'):
        academias = grupo['academia'].unique()
        # Gera combinações únicas entre academias na mesma categoria
        for a1, a2 in combinations(sorted(academias), 2):
            confrontos.append((a1, a2))

    # Converte em DataFrame e conta os confrontos
    confrontos_df = pd.DataFrame(confrontos, columns=['Academia 1', 'Academia 2'])
    confrontos_df_final = confrontos_df.value_counts().reset_index(name='Confrontos')
    st.dataframe(confrontos_df_final, hide_index=True)

col1, col2 = st.columns(2)
with col1:
    st.write("**Distribuição de atletas por faixa etária:**")
    st.write(filtered_data['idade'].value_counts())
with col2:
    st.write("**Distribuição por Graduação:**")
    st.write(filtered_data['faixa'].value_counts())


st.markdown('<p style="text-align: center; color: gray; font-size: small;">Powered by <strong>Academia Master - Paranaguá</strong></p>', unsafe_allow_html=True)
