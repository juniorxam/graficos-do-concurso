import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from random import randint
import io

# ---------- CONFIGURAÇÃO DA PÁGINA ----------
st.set_page_config(page_title="Vagas Saúde TO", layout="wide")

# ---------- FUNÇÃO PARA CARREGAR DADOS (FICTÍCIOS OU IMPORTADOS) ----------
@st.cache_data
def gerar_dados_ficticios():
    """Gera dados fictícios para o protótipo"""
    
    # Municípios com hospitais estaduais (17 unidades)
    municipios = [
        "Palmas", "Araguaína", "Gurupi", "Porto Nacional", "Paraíso do Tocantins",
        "Arraias", "Pedro Afonso", "Guaraí", "Dianópolis", "Alvorada",
        "Miracema do Tocantins", "Xambioá", "Arapoema", "Araguaçu", "Augustinópolis"
    ]

    # 8 REGIÕES DE SAÚDE OFICIAIS DO TOCANTINS (PDR 2014)
    regioes_saude = [
        "Bico do Papagaio",
        "Médio Norte Araguaia",
        "Cerrado Tocantins Araguaia",
        "Cantão",
        "Capim Dourado",
        "Amor Perfeito",
        "Ilha do Bananal",
        "Sudeste"
    ]

    # Mapeamento município -> região
    municipio_regiao = {
        "Palmas": "Capim Dourado",
        "Porto Nacional": "Amor Perfeito",
        "Paraíso do Tocantins": "Cantão",
        "Miracema do Tocantins": "Capim Dourado",
        "Araguaína": "Médio Norte Araguaia",
        "Xambioá": "Médio Norte Araguaia",
        "Arapoema": "Cerrado Tocantins Araguaia",
        "Pedro Afonso": "Cerrado Tocantins Araguaia",
        "Guaraí": "Médio Norte Araguaia",
        "Gurupi": "Ilha do Bananal",
        "Alvorada": "Ilha do Bananal",
        "Araguaçu": "Ilha do Bananal",
        "Dianópolis": "Sudeste",
        "Arraias": "Sudeste",
        "Augustinópolis": "Bico do Papagaio"
    }

    # Dicionário com os nomes dos hospitais
    hospitais_por_municipio = {
        "Palmas": [
            "Hospital Geral de Palmas (HGP) - com ala pediátrica", 
            "Hospital e Maternidade Dona Regina"
        ],
        "Araguaína": ["Hospital Regional de Araguaína", "Hospital Materno Infantil Tia Dedé"],
        "Gurupi": ["Hospital Regional de Gurupi"],
        "Porto Nacional": ["Hospital Regional de Porto Nacional"],
        "Paraíso do Tocantins": ["Hospital Regional de Paraíso do Tocantins"],
        "Augustinópolis": ["Hospital Regional de Augustinópolis"],
        "Dianópolis": ["Hospital Regional de Dianópolis"],
        "Arraias": ["Hospital Regional de Arraias"],
        "Guaraí": ["Hospital Regional de Guaraí"],
        "Pedro Afonso": ["Hospital Regional de Pedro Afonso"],
        "Miracema do Tocantins": ["Hospital Regional de Miracema"],
        "Xambioá": ["Hospital Regional de Xambioá"],
        "Alvorada": ["Hospital Regional de Alvorada"],
        "Araguaçu": ["Hospital Regional de Araguaçu"],
        "Arapoema": ["Hospital e Maternidade Irmã Rita"]
    }

    # Cargos conforme Lei 2.670/2012
    cargos = [
        "Analista em Controle de Zoonoses", "Assistente Social", "Biólogo em Saúde",
        "Biomédico", "Enfermeiro", "Farmacêutico", "Farmacêutico-Bioquímico",
        "Fonoaudiólogo", "Nutricionista", "Psicólogo", "Tecnólogo",
        "Cirurgião-Dentista", "Médico", "Fisioterapeuta", "Terapeuta Ocupacional",
        "Administrador Hospitalar", "Auditor em Saúde", "Engenheiro Clínico",
        "Executivo em Saúde", "Inspetor em Vigilância Sanitária",
        "Pesquisador Docente em Saúde Pública", "Gestor em Saúde", "Físico",
        "Instrumentador Cirúrgico", "Técnico em Imobilização Ortopédica",
        "Técnico de Saúde Bucal", "Técnico em Enfermagem", "Técnico em Laboratório",
        "Técnico em Radiologia", "Assistente de Serviços de Saúde",
        "Auxiliar de Serviços de Saúde", "Auxiliar de Enfermagem", "Auxiliar de Laboratório"
    ]

    # Gerar dados
    dados = []
    for municipio in municipios:
        regiao = municipio_regiao[municipio]
        hospitais = hospitais_por_municipio[municipio]
        
        if municipio in ["Palmas", "Araguaína", "Gurupi"]:
            max_vagas = 25
        elif municipio in ["Porto Nacional", "Paraíso do Tocantins", "Augustinópolis"]:
            max_vagas = 15
        else:
            max_vagas = 10
            
        for hospital in hospitais:
            for cargo in cargos:
                if cargo in ["Médico", "Enfermeiro", "Técnico em Enfermagem"]:
                    vagas = randint(2, max_vagas)
                elif cargo in ["Auxiliar de Enfermagem", "Auxiliar de Laboratório"]:
                    vagas = randint(0, 3)
                elif cargo in ["Gestor em Saúde", "Executivo em Saúde", "Pesquisador Docente em Saúde Pública"]:
                    vagas = randint(0, 2)
                else:
                    vagas = randint(0, max_vagas//2)
                    
                if vagas > 0:
                    dados.append([municipio, regiao, hospital, cargo, vagas])

    return pd.DataFrame(dados, columns=["Município", "Região de Saúde", "Hospital", "Cargo", "Vagas"])

# ---------- FUNÇÃO PARA VALIDAR DADOS IMPORTADOS ----------
def validar_dados_importados(df):
    """Verifica se o DataFrame importado tem a estrutura correta"""
    
    colunas_esperadas = ["Município", "Região de Saúde", "Hospital", "Cargo", "Vagas"]
    colunas_recebidas = df.columns.tolist()
    
    # Verificar se todas as colunas esperadas existem
    for col in colunas_esperadas:
        if col not in colunas_recebidas:
            return False, f"Coluna '{col}' não encontrada. Colunas encontradas: {colunas_recebidas}"
    
    # Verificar se há dados
    if df.empty:
        return False, "O arquivo está vazio"
    
    # Verificar se a coluna Vagas é numérica
    if not pd.api.types.is_numeric_dtype(df["Vagas"]):
        return False, "A coluna 'Vagas' deve conter apenas números"
    
    # Verificar se há valores negativos
    if (df["Vagas"] < 0).any():
        return False, "A coluna 'Vagas' não pode conter valores negativos"
    
    return True, "Dados válidos"

# ---------- TÍTULO PRINCIPAL ----------
st.title("🏥 Distribuição de Vagas - Concurso Secretaria da Saúde do Tocantins")

# ---------- SIDEBAR: FONTE DOS DADOS ----------
st.sidebar.header("📁 Fonte dos Dados")

opcao_dados = st.sidebar.radio(
    "Selecionar origem dos dados:",
    ["📊 Usar dados fictícios (protótipo)", "📤 Importar planilha própria"]
)

df = None
fonte_dados = "ficticios"

if opcao_dados == "📊 Usar dados fictícios (protótipo)":
    df = gerar_dados_ficticios()
    st.sidebar.success("✅ Usando dados fictícios")
    fonte_dados = "ficticios"
else:
    st.sidebar.markdown("### 📤 Upload da planilha")
    st.sidebar.markdown("""
    **Formato esperado:**
    - Colunas: `Município`, `Região de Saúde`, `Hospital`, `Cargo`, `Vagas`
    - Arquivos: Excel (.xlsx) ou CSV (.csv)
    """)
    
    arquivo = st.sidebar.file_uploader(
        "Escolher arquivo",
        type=['xlsx', 'csv'],
        help="Faça upload de uma planilha com os dados do concurso"
    )
    
    if arquivo is not None:
        try:
            # Tentar ler o arquivo
            if arquivo.name.endswith('.csv'):
                df_importado = pd.read_csv(arquivo)
            else:
                df_importado = pd.read_excel(arquivo)
            
            # Validar estrutura
            valido, mensagem = validar_dados_importados(df_importado)
            
            if valido:
                df = df_importado
                st.sidebar.success(f"✅ Arquivo carregado! {len(df)} registros encontrados.")
                fonte_dados = "importado"
            else:
                st.sidebar.error(f"❌ Erro no formato: {mensagem}")
                
                # Mostrar exemplo do formato esperado
                st.sidebar.markdown("### 📋 Exemplo do formato esperado:")
                exemplo = pd.DataFrame({
                    "Município": ["Palmas", "Araguaína"],
                    "Região de Saúde": ["Capim Dourado", "Médio Norte Araguaia"],
                    "Hospital": ["Hospital Geral de Palmas", "Hospital Regional de Araguaína"],
                    "Cargo": ["Médico", "Enfermeiro"],
                    "Vagas": [10, 15]
                })
                st.sidebar.dataframe(exemplo, use_container_width=True)
                
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao ler arquivo: {str(e)}")
    
    # Se não carregou arquivo, volta para dados fictícios
    if df is None:
        df = gerar_dados_ficticios()
        st.sidebar.info("ℹ️ Nenhum arquivo carregado. Usando dados fictícios.")
        fonte_dados = "ficticios"

# ---------- FILTROS LATERAIS (baseados nos dados carregados) ----------
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros")

# Listas únicas para filtros
regioes_unicas = sorted(df["Região de Saúde"].unique())
municipios_unicos = sorted(df["Município"].unique())
hospitais_unicos = sorted(df["Hospital"].unique())
cargos_unicos = sorted(df["Cargo"].unique())

# Filtro de Região
regioes = ["Todas"] + regioes_unicas
regiao_selecionada = st.sidebar.selectbox("Região de Saúde", regioes)

# Filtrar municípios baseado na região
if regiao_selecionada != "Todas":
    municipios_filtrados = sorted(df[df["Região de Saúde"] == regiao_selecionada]["Município"].unique())
else:
    municipios_filtrados = municipios_unicos

# Filtro de Município
municipios_lista = ["Todos"] + municipios_filtrados
municipio_selecionado = st.sidebar.selectbox("Município", municipios_lista)

# Filtrar hospitais baseado no município
if municipio_selecionado != "Todos":
    hospitais_filtrados = sorted(df[df["Município"] == municipio_selecionado]["Hospital"].unique())
elif regiao_selecionada != "Todas":
    hospitais_filtrados = sorted(df[df["Região de Saúde"] == regiao_selecionada]["Hospital"].unique())
else:
    hospitais_filtrados = hospitais_unicos

# Filtro de Hospital
hospitais_lista = ["Todos"] + hospitais_filtrados
hospital_selecionado = st.sidebar.selectbox("Hospital", hospitais_lista)

# Filtro de Cargo
cargos_lista = ["Todos"] + cargos_unicos
cargo_selecionado = st.sidebar.selectbox("Cargo", cargos_lista)

# ---------- APLICAR FILTROS ----------
df_filtrado = df.copy()
if regiao_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Região de Saúde"] == regiao_selecionada]
if municipio_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Município"] == municipio_selecionado]
if hospital_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Hospital"] == hospital_selecionado]
if cargo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Cargo"] == cargo_selecionado]

# ---------- MÉTRICAS RESUMO ----------
st.markdown(f"**Fonte:** {'Dados fictícios' if fonte_dados == 'ficticios' else 'Planilha importada'}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Vagas", df_filtrado["Vagas"].sum())
with col2:
    st.metric("Hospitais", df_filtrado["Hospital"].nunique())
with col3:
    st.metric("Municípios", df_filtrado["Município"].nunique())
with col4:
    st.metric("Cargos", df_filtrado["Cargo"].nunique())

# ---------- TABELA DE DADOS ----------
st.subheader("📋 Detalhamento das Vagas")
st.dataframe(df_filtrado, use_container_width=True, height=400)

# ---------- GRÁFICOS ----------
st.subheader("📊 Visualizações")

# Abas para organizar os diferentes tipos de gráfico
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "📊 Barras", 
    "🔥 Mapa de Calor", 
    "🥧 Pizza/Rosca", 
    "📚 Barras Empilhadas", 
    "🌳 Treemap"
])

with aba1:
    # GRÁFICO 1: BARRAS
    st.markdown("### Total de Vagas por Categoria")
    tipo_grafico = st.radio("Agrupar por:", ("Município", "Cargo", "Região de Saúde", "Hospital"), horizontal=True, key="bar_radio")
    
    if tipo_grafico == "Município":
        df_group = df_filtrado.groupby("Município")["Vagas"].sum().reset_index()
        x_label = "Município"
        titulo = "Total de Vagas por Município"
    elif tipo_grafico == "Cargo":
        df_group = df_filtrado.groupby("Cargo")["Vagas"].sum().reset_index()
        x_label = "Cargo"
        titulo = "Total de Vagas por Cargo"
    elif tipo_grafico == "Região de Saúde":
        df_group = df_filtrado.groupby("Região de Saúde")["Vagas"].sum().reset_index()
        x_label = "Região de Saúde"
        titulo = "Total de Vagas por Região de Saúde"
    else:
        df_group = df_filtrado.groupby("Hospital")["Vagas"].sum().reset_index()
        x_label = "Hospital"
        titulo = "Total de Vagas por Hospital"
    
    df_group = df_group.sort_values("Vagas", ascending=False)
    
    fig = px.bar(
        df_group, 
        x=x_label, 
        y="Vagas",
        title=titulo,
        text="Vagas",
        color_discrete_sequence=["#1f77b4"]
    )
    
    fig.update_traces(
        textposition="outside",
        textfont_size=11,
        cliponaxis=False,
        marker_line_width=0,
        opacity=0.8
    )
    
    altura = 500 + max(0, (len(df_group) - 10) * 15)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Número de Vagas",
        xaxis_tickangle=-45 if len(df_group) > 5 else 0,
        height=altura,
        margin=dict(l=80, r=80, t=100, b=150),
        showlegend=False,
        yaxis=dict(range=[0, df_group["Vagas"].max() * 1.15])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Total de vagas por {tipo_grafico.lower()}")
    st.dataframe(df_group, use_container_width=True, height=200)

with aba2:
    # GRÁFICO 2: MAPA DE CALOR
    st.markdown("### 🔥 Mapa de Calor: Vagas por Região de Saúde e Cargo")
    
    # Criar tabela pivô para o heatmap
    heatmap_data = df_filtrado.pivot_table(
        values='Vagas', 
        index='Região de Saúde', 
        columns='Cargo', 
        aggfunc='sum', 
        fill_value=0
    )
    
    # Selecionar top cargos para não poluir visualmente
    top_cargos = df_filtrado.groupby('Cargo')['Vagas'].sum().nlargest(10).index.tolist()
    heatmap_data_top = heatmap_data[top_cargos] if not heatmap_data.empty else heatmap_data
    
    if not heatmap_data_top.empty and heatmap_data_top.shape[0] > 0:
        fig_heatmap = px.imshow(
            heatmap_data_top,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='Blues',
            title="Distribuição de Vagas por Região de Saúde e Cargo (Top 10 Cargos)",
            labels=dict(x="Cargo", y="Região de Saúde", color="Vagas")
        )
        fig_heatmap.update_layout(
            height=500,
            xaxis_tickangle=-45,
            margin=dict(l=150, r=50, t=100, b=150)
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.caption("Quanto mais escuro o azul, maior o número de vagas naquela combinação Região x Cargo")
    else:
        st.info("Selecione menos filtros para visualizar o mapa de calor")

with aba3:
    # GRÁFICO 3: PIZZA/ROSCA
    st.markdown("### 🥧 Distribuição Percentual de Vagas")
    
    col_pizza1, col_pizza2 = st.columns(2)
    
    with col_pizza1:
        # Pizza por Região
        df_regiao = df_filtrado.groupby("Região de Saúde")["Vagas"].sum().reset_index()
        df_regiao = df_regiao.sort_values("Vagas", ascending=False)
        
        if not df_regiao.empty:
            fig_pizza_regiao = px.pie(
                df_regiao,
                values='Vagas',
                names='Região de Saúde',
                title='Distribuição por Região de Saúde',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pizza_regiao.update_traces(textposition='inside', textinfo='percent+label')
            fig_pizza_regiao.update_layout(height=400)
            st.plotly_chart(fig_pizza_regiao, use_container_width=True)
        else:
            st.info("Sem dados para região")
    
    with col_pizza2:
        # Pizza por Cargo (top 8 para não poluir)
        df_cargo = df_filtrado.groupby("Cargo")["Vagas"].sum().reset_index()
        df_cargo = df_cargo.sort_values("Vagas", ascending=False).head(8)
        outros = df_filtrado.groupby("Cargo")["Vagas"].sum().sum() - df_cargo["Vagas"].sum()
        
        if outros > 0:
            df_cargo = pd.concat([df_cargo, pd.DataFrame([{"Cargo": "Outros", "Vagas": outros}])])
        
        if not df_cargo.empty:
            fig_pizza_cargo = px.pie(
                df_cargo,
                values='Vagas',
                names='Cargo',
                title='Distribuição por Cargo (Top 8 + Outros)',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pizza_cargo.update_traces(textposition='inside', textinfo='percent+label', textfont_size=10)
            fig_pizza_cargo.update_layout(height=400)
            st.plotly_chart(fig_pizza_cargo, use_container_width=True)
        else:
            st.info("Sem dados para cargo")

with aba4:
    # GRÁFICO 4: BARRAS EMPILHADAS
    st.markdown("### 📚 Composição de Cargos por Município")
    
    # Preparar dados para barras empilhadas
    df_stack = df_filtrado.groupby(["Município", "Cargo"])["Vagas"].sum().reset_index()
    
    # Selecionar top municípios por total de vagas
    top_municipios = df_filtrado.groupby("Município")["Vagas"].sum().nlargest(8).index.tolist()
    df_stack_top = df_stack[df_stack["Município"].isin(top_municipios)]
    
    if not df_stack_top.empty:
        # Criar gráfico de barras empilhadas
        fig_stack = px.bar(
            df_stack_top,
            x="Município",
            y="Vagas",
            color="Cargo",
            title="Composição de Cargos nos Principais Municípios",
            text_auto=True,
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_stack.update_layout(
            height=500,
            xaxis_tickangle=-45,
            yaxis_title="Número de Vagas",
            margin=dict(l=50, r=50, t=100, b=150),
            legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
        )
        fig_stack.update_traces(textfont_size=10, textposition="inside")
        st.plotly_chart(fig_stack, use_container_width=True)
        st.caption("Cada barra mostra a distribuição de cargos dentro do município")
    else:
        st.info("Selecione menos filtros ou mais municípios para visualizar")

with aba5:
    # GRÁFICO 5: TREEMAP
    st.markdown("### 🌳 Treemap - Hierarquia Região > Município > Vagas")
    
    # Preparar dados hierárquicos
    df_treemap = df_filtrado.groupby(["Região de Saúde", "Município"])["Vagas"].sum().reset_index()
    
    if not df_treemap.empty:
        fig_treemap = px.treemap(
            df_treemap,
            path=["Região de Saúde", "Município"],
            values="Vagas",
            title="Distribuição Hierárquica de Vagas: Região de Saúde > Município",
            color="Vagas",
            color_continuous_scale="Blues",
            hover_data={"Vagas": True}
        )
        fig_treemap.update_layout(height=600, margin=dict(l=25, r=25, t=50, b=25))
        fig_treemap.update_traces(
            textinfo="label+value+percent parent",
            textfont_size=12
        )
        st.plotly_chart(fig_treemap, use_container_width=True)
        st.caption("Área de cada retângulo proporcional ao número de vagas. Clicar para navegar na hierarquia.")
    else:
        st.info("Sem dados suficientes para treemap")

# ---------- RESUMO ESTATÍSTICO ----------
with st.expander("📈 Análise Estatística"):
    col_est1, col_est2 = st.columns(2)
    
    with col_est1:
        st.markdown("#### Municípios com mais vagas")
        top_muni = df_filtrado.groupby("Município")["Vagas"].sum().nlargest(5).reset_index()
        st.dataframe(top_muni, use_container_width=True)
        
        st.markdown("#### Cargos com mais vagas")
        top_cargos = df_filtrado.groupby("Cargo")["Vagas"].sum().nlargest(5).reset_index()
        st.dataframe(top_cargos, use_container_width=True)
    
    with col_est2:
        st.markdown("#### Estatísticas Gerais")
        media_muni = df_filtrado.groupby("Município")["Vagas"].sum().mean()
        mediana_muni = df_filtrado.groupby("Município")["Vagas"].sum().median()
        
        st.metric("Média de vagas por município", f"{media_muni:.1f}")
        st.metric("Mediana de vagas por município", f"{mediana_muni:.1f}")
        st.metric("Total de Hospitais", df_filtrado["Hospital"].nunique())
        st.metric("Total de Cargos distintos", df_filtrado["Cargo"].nunique())
        
        st.markdown("#### Amplitude de vagas")
        st.metric("Mínimo", df_filtrado["Vagas"].min())
        st.metric("Máximo", df_filtrado["Vagas"].max())

# ---------- DOWNLOAD DOS DADOS FILTRADOS ----------
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download dos dados filtrados (CSV)",
    data=csv,
    file_name='vagas_saude_to_filtrado.csv',
    mime='text/csv',
)

# ---------- RODAPÉ ----------
st.markdown("---")
if fonte_dados == "ficticios":
    st.caption("⚠️ **Dados fictícios para protótipo.** Faça upload de uma planilha com dados reais do concurso.")
else:
    st.caption("✅ **Dados importados da planilha.** As informações exibidas são do arquivo carregado.")