import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import folium
from streamlit_folium import st_folium
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Gestão de Obras Elétricas - Equatorial",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado com responsividade mobile
st.markdown("""
<style>
    /* Estilos gerais */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        text-align: center;
        font-size: 2rem;
    }

    /* Métricas responsivas */
    .metric-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-width: 200px;
        flex: 1;
    }

    /* Cards de projeto */
    .project-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .project-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }

    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .status-em_execucao { background: #dbeafe; color: #1e40af; }
    .status-planejamento { background: #fef3c7; color: #92400e; }
    .status-finalizada { background: #d1fae5; color: #065f46; }

    /* Footer responsivo */
    .footer-content {
        text-align: center;
        color: #666;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 2rem;
    }

    .footer-grid {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        flex-wrap: wrap;
        gap: 1rem;
    }

    /* Responsividade Mobile */
    @media (max-width: 768px) {
        /* Header mobile */
        .main-header {
            padding: 0.75rem;
            margin-bottom: 1rem;
        }
        .main-header h1 {
            font-size: 1.25rem;
            line-height: 1.4;
        }

        /* Colunas do Streamlit */
        .stColumns > div {
            min-width: 0 !important;
            padding: 0 0.25rem !important;
        }

        /* Métricas em mobile */
        .metric-container {
            flex-direction: column;
        }
        .metric-card {
            min-width: 100%;
        }

        /* Selectbox e inputs */
        .stSelectbox, .stTextInput, .stNumberInput, .stDateInput {
            margin-bottom: 0.5rem;
        }

        /* Cards de projeto */
        .project-card {
            padding: 0.75rem;
            margin: 0.25rem 0;
        }

        .project-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }

        /* Gráficos */
        .plotly-graph-div {
            height: 300px !important;
        }

        /* Tabelas */
        .stDataFrame {
            font-size: 0.875rem;
        }

        /* Footer mobile */
        .footer-grid {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }

        /* Sidebar mobile */
        .css-1d391kg { /* Sidebar */
            padding-top: 1rem;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
        }

        /* Botões */
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
        }

        /* Progress bars */
        .stProgress {
            margin: 0.5rem 0;
        }

        /* Maps */
        .folium-map {
            height: 300px !important;
        }
    }

    /* Tablet */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header h1 {
            font-size: 1.75rem;
        }

        .stColumns > div {
            padding: 0 0.5rem !important;
        }

        .plotly-graph-div {
            height: 350px !important;
        }
    }

    /* Desktop grande */
    @media (min-width: 1200px) {
        .main-header {
            padding: 1.5rem;
        }
        .main-header h1 {
            font-size: 2.5rem;
        }
    }

    /* Melhorias de UX */
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }

    /* Loading states */
    .stSpinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }

    /* Alertas responsivos */
    .stAlert {
        margin: 0.5rem 0;
        border-radius: 8px;
    }

    /* Inputs com melhor spacing */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        padding: 0.75rem !important;
        border-radius: 6px !important;
        border: 1px solid #d1d5db !important;
    }

    /* Tooltips mobile friendly */
    [data-testid="stTooltipHoverTarget"] {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


# Função para detectar dispositivo mobile
def is_mobile():
    """Detecta se está sendo executado em dispositivo mobile"""
    # Em produção, você pode usar JavaScript para detectar o user agent
    # Por enquanto, vamos usar o tamanho da tela do Streamlit
    return st.session_state.get('is_mobile', False)


# Função para criar métricas responsivas
def create_responsive_metrics(metrics_data):
    """Cria métricas responsivas para mobile e desktop"""

    # Detectar se é mobile baseado no número de colunas desejado
    if len(metrics_data) <= 2:
        # Para 2 métricas ou menos, usar 2 colunas mesmo em mobile
        cols = st.columns(2)
    elif len(metrics_data) <= 4:
        # Para 3-4 métricas, usar layout responsivo
        cols = st.columns([1, 1, 1, 1])
    else:
        # Para mais métricas, dividir em linhas
        cols = st.columns(4)

    for i, (label, value, delta) in enumerate(metrics_data):
        with cols[i % len(cols)]:
            st.metric(label, value, delta)


# Função para criar cards de projeto responsivos
def create_project_card(project):
    """Cria card de projeto responsivo"""

    status_colors = {
        'em_execucao': '#3B82F6',
        'planejamento': '#F59E0B',
        'finalizada': '#10B981'
    }

    status_labels = {
        'em_execucao': 'Em Execução',
        'planejamento': 'Planejamento',
        'finalizada': 'Finalizada'
    }

    with st.container():
        # Header do card
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**{get_type_icon(project['tipo'])} {project['nome']}**")

        with col2:
            status_color = status_colors.get(project['status'], '#6B7280')
            st.markdown(f"""
                <div style="background: {status_color}20; color: {status_color}; 
                           padding: 0.25rem 0.75rem; border-radius: 12px; 
                           text-align: center; font-size: 0.8rem; font-weight: 500;">
                    {status_labels.get(project['status'], project['status'])}
                </div>
            """, unsafe_allow_html=True)

        # Informações principais - Layout responsivo
        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.write(f"📍 **Local:** {project['endereco']}")
            st.write(f"👨‍💼 **Supervisor:** {project['supervisor']}")
            st.write(f"📅 **Início:** {project['data_inicio']}")

        with info_col2:
            st.write(f"👥 **Equipe:** {project['equipe_size']} pessoas")
            st.write(f"💰 **Orçamento:** R$ {project['orcamento']:,.0f}")
            st.write(f"🏁 **Fim:** {project['data_fim']}")

        # Barra de progresso
        st.write(f"**🎯 Progresso: {project['progresso']}%**")
        st.progress(project['progresso'] / 100)

        # Informações financeiras
        gasto_pct = (project['gasto'] / project['orcamento']) * 100
        saldo = project['orcamento'] - project['gasto']

        fin_col1, fin_col2, fin_col3 = st.columns(3)
        with fin_col1:
            st.metric("Gasto", f"R$ {project['gasto']:,.0f}", f"{gasto_pct:.1f}%")
        with fin_col2:
            st.metric("Saldo", f"R$ {saldo:,.0f}")
        with fin_col3:
            eficiencia = ((project['orcamento'] - project['gasto']) / project['orcamento']) * 100
            st.metric("Eficiência", f"{eficiencia:.1f}%")


# Inicializar session states
def init_session_states():
    if 'evolution_points' not in st.session_state:
        st.session_state.evolution_points = []
    if 'comments' not in st.session_state:
        st.session_state.comments = []
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'custom_forms' not in st.session_state:
        st.session_state.custom_forms = []
    if 'form_responses' not in st.session_state:
        st.session_state.form_responses = []


init_session_states()


# Dados simulados (mantidos os mesmos)
@st.cache_data
def load_projects_data():
    projects_data = {
        'id': [1, 2, 3, 4, 5],
        'nome': [
            'Expansão Rede MT - Bairro Centro',
            'Modernização Subestação Industrial',
            'Manutenção Linha Transmissão',
            'Instalação Transformadores - Cohama',
            'Reforma Subestação Tirirical'
        ],
        'tipo': ['expansao_rede', 'modernizacao', 'manutencao', 'instalacao', 'reforma'],
        'status': ['em_execucao', 'planejamento', 'finalizada', 'em_execucao', 'planejamento'],
        'prioridade': ['alta', 'media', 'alta', 'media', 'baixa'],
        'endereco': [
            'Centro, São Luís/MA',
            'Distrito Industrial, São Luís/MA',
            'Zona Rural, São Luís/MA',
            'Cohama, São Luís/MA',
            'Tirirical, São Luís/MA'
        ],
        'latitude': [-2.5297, -2.5555, -2.4888, -2.5180, -2.4950],
        'longitude': [-44.3028, -44.2525, -44.3555, -44.2660, -44.2380],
        'data_inicio': ['2025-01-15', '2025-08-01', '2025-06-01', '2025-07-10', '2025-09-01'],
        'data_fim': ['2025-03-20', '2025-12-15', '2025-07-15', '2025-09-30', '2025-11-15'],
        'progresso': [65, 15, 100, 45, 8],
        'orcamento': [450000, 850000, 320000, 280000, 180000],
        'gasto': [292500, 127500, 298000, 126000, 14400],
        'supervisor': [
            'Eng. Carlos Oliveira',
            'Eng. Patricia Alves',
            'Eng. Fernando Rocha',
            'Eng. Ana Santos',
            'Eng. Roberto Lima'
        ],
        'equipe_size': [3, 2, 3, 4, 2],
        'template_type': ['rede_mt', 'subestacao', 'manutencao', 'transformador', 'reforma']
    }
    return pd.DataFrame(projects_data)


@st.cache_data
def load_materials_data():
    materials_data = {
        'projeto_id': [1, 1, 1, 2, 2, 3, 3, 4, 4, 5],
        'material': [
            'Cabo 15kV', 'Postes concreto', 'Transformador 150kVA',
            'Disjuntor 138kV', 'Relé proteção',
            'Isoladores', 'Cabo ACSR',
            'Transformador 75kVA', 'Cabo subterrâneo',
            'Chaves seccionadoras'
        ],
        'quantidade': [2500, 15, 2, 3, 6, 50, 1200, 3, 800, 8],
        'unidade': ['m', 'un', 'un', 'un', 'un', 'un', 'm', 'un', 'm', 'un'],
        'usado': [1625, 10, 1, 0, 1, 48, 1150, 2, 360, 1],
        'custo_unitario': [45, 2800, 35000, 125000, 8500, 180, 25, 28000, 85, 4200]
    }
    return pd.DataFrame(materials_data)


@st.cache_data
def load_users_data():
    users_data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8],
        'nome': [
            'Eng. Carlos Oliveira', 'Eng. Patricia Alves', 'Eng. Fernando Rocha',
            'Eng. Ana Santos', 'Eng. Roberto Lima', 'João Silva',
            'Maria Santos', 'Pedro Costa'
        ],
        'email': [
            'carlos.oliveira@equatorial.com', 'patricia.alves@equatorial.com',
            'fernando.rocha@equatorial.com', 'ana.santos@equatorial.com',
            'roberto.lima@equatorial.com', 'joao.silva@equatorial.com',
            'maria.santos@equatorial.com', 'pedro.costa@equatorial.com'
        ],
        'tipo': ['supervisor', 'supervisor', 'supervisor', 'supervisor', 'supervisor', 'tecnico', 'tecnico', 'tecnico'],
        'nivel_acesso': ['gerente', 'gerente', 'gerente', 'gerente', 'gerente', 'campo', 'campo', 'campo'],
        'ativo': [True, True, True, True, True, True, True, True]
    }
    return pd.DataFrame(users_data)


# Funções auxiliares (mantidas as mesmas)
def get_status_color(status):
    colors = {
        'em_execucao': '#3B82F6',
        'planejamento': '#F59E0B',
        'finalizada': '#10B981'
    }
    return colors.get(status, '#6B7280')


def get_status_label(status):
    labels = {
        'em_execucao': 'Em Execução',
        'planejamento': 'Planejamento',
        'finalizada': 'Finalizada'
    }
    return labels.get(status, status)


def get_type_icon(tipo):
    icons = {
        'expansao_rede': '⚡',
        'modernizacao': '⚙️',
        'manutencao': '🔧',
        'instalacao': '➕',
        'reforma': '🏠'
    }
    return icons.get(tipo, '⚡')


def create_map(df_projects_filtered):
    m = folium.Map(
        location=[-2.5297, -44.3028],
        zoom_start=11,
        tiles='OpenStreetMap'
    )

    for idx, row in df_projects_filtered.iterrows():
        icon_map = {
            'expansao_rede': 'flash',
            'modernizacao': 'cog',
            'manutencao': 'wrench',
            'instalacao': 'plus',
            'reforma': 'home'
        }

        popup_text = f"""
        <b>{row['nome']}</b><br>
        Status: {get_status_label(row['status'])}<br>
        Progresso: {row['progresso']}%<br>
        Supervisor: {row['supervisor']}<br>
        Endereço: {row['endereco']}
        """

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row['nome'],
            icon=folium.Icon(
                color='blue' if row['status'] == 'em_execucao' else
                'orange' if row['status'] == 'planejamento' else 'green',
                icon=icon_map.get(row['tipo'], 'flash')
            )
        ).add_to(m)

    return m


# Carregar dados
df_projects = load_projects_data()
df_materials = load_materials_data()
df_users = load_users_data()

# Header principal com responsividade
st.markdown("""
<div class="main-header">
    <h1>⚡ Sistema de Gestão de Obras Elétricas</h1>
    <div style="text-align: center; margin-top: 0.5rem;">
        <small style="color: rgba(255,255,255,0.8);">Equatorial Energia - Dashboard Mobile</small>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar responsiva
with st.sidebar:
    st.title("📋 Menu")

    # Informações do usuário (simulado)
    st.markdown("""
    <div style="background: #f0f2f6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 40px; height: 40px; background: #3b82f6; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                JD
            </div>
            <div>
                <div style="font-weight: bold; font-size: 0.9rem;">João Diretor</div>
                <div style="font-size: 0.8rem; color: #666;">Gerente de Operações</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "Selecione a página:",
        ["🏠 Dashboard", "📊 Projetos", "🗺️ Mapa", "📝 Tarefas", "💬 Comentários", "📋 Formulários", "👥 Usuários",
         "📈 Relatórios"],
        label_visibility="collapsed"
    )

    # Quick stats na sidebar
    st.markdown("### 📊 Quick Stats")
    obras_ativas = len(df_projects[df_projects['status'] != 'finalizada'])
    progresso_medio = df_projects['progresso'].mean()

    st.metric("Obras Ativas", obras_ativas, delta="+2")
    st.metric("Progresso Médio", f"{progresso_medio:.0f}%", delta="+5%")

# ================================
# PÁGINA DASHBOARD - RESPONSIVA
# ================================
if page == "🏠 Dashboard":
    st.header("📊 Dashboard Executivo")

    # Métricas principais com layout responsivo
    metrics_data = [
        ("Obras Ativas", len(df_projects[df_projects['status'] != 'finalizada']), "+2"),
        ("Progresso Médio", f"{df_projects['progresso'].mean():.1f}%", "+5%"),
        ("Orçamento Total", f"R$ {df_projects['orcamento'].sum() / 1000:.0f}K", None),
        ("Profissionais", df_projects['equipe_size'].sum(), "+3")
    ]

    create_responsive_metrics(metrics_data)

    st.divider()

    # Layout responsivo para gráficos
    # Em mobile, os gráficos ficam em coluna única
    # Em desktop, ficam lado a lado

    # Gráfico de progresso
    st.subheader("📊 Progresso dos Projetos")
    fig_progress = px.bar(
        df_projects,
        x='progresso',
        y='nome',
        orientation='h',
        color='status',
        color_discrete_map={
            'em_execucao': '#3B82F6',
            'planejamento': '#F59E0B',
            'finalizada': '#10B981'
        },
        title="Progresso por Projeto (%)"
    )
    # Altura ajustada para mobile
    fig_progress.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12)
    )
    st.plotly_chart(fig_progress, use_container_width=True)

    # Gráfico de status
    st.subheader("🎯 Status das Obras")
    status_counts = df_projects['status'].value_counts()
    fig_pie = px.pie(
        values=status_counts.values,
        names=[get_status_label(s) for s in status_counts.index],
        color_discrete_map={
            'Em Execução': '#3B82F6',
            'Planejamento': '#F59E0B',
            'Finalizada': '#10B981'
        }
    )
    fig_pie.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=12)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Orçamento vs Gasto
    st.subheader("💰 Análise Orçamentária")
    fig_budget = go.Figure()
    fig_budget.add_trace(go.Bar(
        name='Orçamento',
        x=df_projects['nome'],
        y=df_projects['orcamento'],
        marker_color='lightblue'
    ))
    fig_budget.add_trace(go.Bar(
        name='Gasto',
        x=df_projects['nome'],
        y=df_projects['gasto'],
        marker_color='darkblue'
    ))
    fig_budget.update_layout(
        barmode='group',
        title="Orçamento vs Gasto por Projeto",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=10),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_budget, use_container_width=True)

# ================================
# PÁGINA PROJETOS - RESPONSIVA
# ================================
elif page == "📊 Projetos":
    st.header("📋 Gestão de Projetos")

    # Filtros em layout responsivo
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        status_filter = st.selectbox(
            "Status:",
            ["Todos"] + list(df_projects['status'].unique()),
            format_func=lambda x: get_status_label(x) if x != "Todos" else x
        )

    with filter_col2:
        tipo_filter = st.selectbox(
            "Tipo:",
            ["Todos"] + list(df_projects['tipo'].unique())
        )

    # Campo de busca em linha separada para mobile
    search_term = st.text_input("🔍 Buscar projeto:", placeholder="Digite o nome do projeto ou endereço...")

    # Aplicar filtros
    filtered_df = df_projects.copy()

    if status_filter != "Todos":
        filtered_df = filtered_df[filtered_df['status'] == status_filter]

    if tipo_filter != "Todos":
        filtered_df = filtered_df[filtered_df['tipo'] == tipo_filter]

    if search_term:
        filtered_df = filtered_df[
            filtered_df['nome'].str.contains(search_term, case=False, na=False) |
            filtered_df['endereco'].str.contains(search_term, case=False, na=False)
            ]

    st.divider()

    # Header dos resultados
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"📋 Projetos Encontrados: {len(filtered_df)}")
    with col2:
        if st.button("📊 Ver Resumo", type="secondary"):
            st.info(f"Total de {len(filtered_df)} projetos • Orçamento: R$ {filtered_df['orcamento'].sum():,.0f}")

    # Lista de projetos com cards responsivos
    for idx, project in filtered_df.iterrows():
        with st.expander(
                f"{get_type_icon(project['tipo'])} {project['nome']} - {get_status_label(project['status'])}",
                expanded=False
        ):
            create_project_card(project)

            # Materiais do projeto
            project_materials = df_materials[df_materials['projeto_id'] == project['id']]
            if not project_materials.empty:
                st.markdown("**🔧 Materiais do Projeto:**")

                # Layout responsivo para materiais
                for _, material in project_materials.iterrows():
                    usage_pct = (material['usado'] / material['quantidade']) * 100
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(
                            f"• **{material['material']}**: {material['usado']}/{material['quantidade']} {material['unidade']}")

                    with col2:
                        if usage_pct >= 90:
                            st.error(f"{usage_pct:.0f}%")
                        elif usage_pct >= 70:
                            st.warning(f"{usage_pct:.0f}%")
                        else:
                            st.success(f"{usage_pct:.0f}%")

# ================================
# PÁGINA MAPA - RESPONSIVA
# ================================
elif page == "🗺️ Mapa":
    st.header("🗺️ Localização das Obras")

    # Filtros do mapa em layout mobile-friendly
    st.markdown("**Filtros do Mapa:**")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        map_status_filter = st.multiselect(
            "Status:",
            options=df_projects['status'].unique(),
            default=df_projects['status'].unique(),
            format_func=get_status_label
        )

    with filter_col2:
        map_tipo_filter = st.multiselect(
            "Tipos:",
            options=df_projects['tipo'].unique(),
            default=df_projects['tipo'].unique()
        )

    # Seção para adicionar pontos
    with st.expander("📍 Adicionar Ponto de Evolução"):
        add_col1, add_col2 = st.columns(2)

        with add_col1:
            selected_project = st.selectbox(
                "Projeto:",
                options=df_projects['nome'].tolist(),
                key="evolution_project"
            )

            evolution_type = st.selectbox(
                "Tipo:",
                ["Início da Obra", "Marco Intermediário", "Conclusão de Etapa",
                 "Instalação Equipamento", "Teste Final", "Obra Concluída"],
                key="evolution_type"
            )

        with add_col2:
            evolution_date = st.date_input(
                "Data:",
                value=datetime.now().date(),
                key="evolution_date"
            )

            st.write("**Coordenadas:**")
            lat_input = st.number_input("Lat:", value=-2.5297, format="%.6f", key="lat_input")
            lng_input = st.number_input("Lng:", value=-44.3028, format="%.6f", key="lng_input")

        if st.button("📍 Adicionar Ponto", type="primary", key="add_point"):
            new_point = {
                'id': len(st.session_state.evolution_points) + 1,
                'project': selected_project,
                'type': evolution_type,
                'date': evolution_date.strftime("%Y-%m-%d"),
                'latitude': lat_input,
                'longitude': lng_input,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.evolution_points.append(new_point)
            st.success(f"✅ Ponto adicionado: {evolution_type}")
            st.rerun()

    # Filtrar dados para o mapa
    map_df = df_projects[
        (df_projects['status'].isin(map_status_filter)) &
        (df_projects['tipo'].isin(map_tipo_filter))
        ]

    # Criar e exibir mapa com altura responsiva
    if not map_df.empty:
        m = create_map(map_df)
        # Altura do mapa ajustada para mobile
        map_data = st_folium(m, width=None, height=400, key="main_map")

        # Informações do mapa
        st.info(f"📍 Exibindo {len(map_df)} obras no mapa")

        # Legenda mobile-friendly
        with st.expander("🔍 Legenda do Mapa"):
            legend_col1, legend_col2, legend_col3 = st.columns(3)

            with legend_col1:
                st.markdown("**Status:**")
                st.markdown("🔵 Em Execução")
                st.markdown("🟠 Planejamento")
                st.markdown("🟢 Finalizada")

            with legend_col2:
                st.markdown("**Tipos:**")
                st.markdown("⚡ Expansão Rede")
                st.markdown("⚙️ Modernização")
                st.markdown("🔧 Manutenção")

            with legend_col3:
                st.markdown("**Ações:**")
                st.markdown("📍 Clique no marcador")
                st.markdown("🔍 Ver detalhes")
                st.markdown("📊 Acessar dados")
    else:
        st.warning("⚠️ Nenhum projeto corresponde aos filtros selecionados.")

    # Exibir pontos de evolução
    if st.session_state.evolution_points:
        st.divider()
        st.subheader(f"📋 Pontos de Evolução ({len(st.session_state.evolution_points)})")

        for point in st.session_state.evolution_points:
            with st.expander(f"📍 {point['type']} - {point['project']}", expanded=False):
                point_col1, point_col2 = st.columns([3, 1])

                with point_col1:
                    st.write(f"**Projeto:** {point['project']}")
                    st.write(f"**Tipo:** {point['type']}")
                    st.write(f"**Data:** {point['date']}")
                    st.write(f"**Coordenadas:** {point['latitude']:.6f}, {point['longitude']:.6f}")

                with point_col2:
                    if st.button(f"🗑️ Remover", key=f"remove_{point['id']}", type="secondary"):
                        st.session_state.evolution_points = [
                            p for p in st.session_state.evolution_points if p['id'] != point['id']
                        ]
                        st.rerun()

# ================================
# PÁGINA TAREFAS - RESPONSIVA
# ================================
elif page == "📝 Tarefas":
    st.header("📝 Gestão de Tarefas")

    # Simulação de tarefas se não existirem
    if not st.session_state.tasks:
        sample_tasks = [
            {
                'id': 1,
                'projeto': 'Expansão Rede MT - Bairro Centro',
                'titulo': 'Instalação de postes',
                'responsavel': 'João Silva',
                'status': 'Em Andamento',
                'progresso': 60,
                'prioridade': 'Alta',
                'data_limite': '2025-08-15'
            },
            {
                'id': 2,
                'projeto': 'Modernização Subestação Industrial',
                'titulo': 'Teste de relés',
                'responsavel': 'Maria Santos',
                'status': 'Pendente',
                'progresso': 0,
                'prioridade': 'Média',
                'data_limite': '2025-08-20'
            },
            {
                'id': 3,
                'projeto': 'Instalação Transformadores - Cohama',
                'titulo': 'Configuração equipamentos',
                'responsavel': 'Pedro Costa',
                'status': 'Concluída',
                'progresso': 100,
                'prioridade': 'Baixa',
                'data_limite': '2025-08-10'
            }
        ]
        st.session_state.tasks.extend(sample_tasks)

    # Filtros em layout responsivo
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        project_filter = st.selectbox(
            "Projeto:",
            ["Todos"] + df_projects['nome'].tolist()
        )

    with filter_col2:
        status_filter_task = st.selectbox(
            "Status:",
            ["Todos", "Pendente", "Em Andamento", "Concluída"]
        )

    # Botão para adicionar nova tarefa
    if st.button("➕ Nova Tarefa", type="primary"):
        st.info("Funcionalidade de adicionar tarefa será implementada!")

    st.divider()

    # Métricas de tarefas
    tasks_total = len(st.session_state.tasks)
    tasks_concluidas = len([t for t in st.session_state.tasks if t['status'] == 'Concluída'])
    tasks_pendentes = len([t for t in st.session_state.tasks if t['status'] == 'Pendente'])
    tasks_andamento = len([t for t in st.session_state.tasks if t['status'] == 'Em Andamento'])

    task_metrics = [
        ("Total", tasks_total, None),
        ("Concluídas", tasks_concluidas, f"+{tasks_concluidas}"),
        ("Em Andamento", tasks_andamento, None),
        ("Pendentes", tasks_pendentes, f"-{tasks_pendentes}")
    ]

    create_responsive_metrics(task_metrics)

    st.divider()

    # Exibir tarefas com cards responsivos
    filtered_tasks = []
    for task in st.session_state.tasks:
        show_task = True
        if project_filter != "Todos" and task['projeto'] != project_filter:
            show_task = False
        if status_filter_task != "Todos" and task['status'] != status_filter_task:
            show_task = False

        if show_task:
            filtered_tasks.append(task)

    if filtered_tasks:
        st.subheader(f"📋 Tarefas ({len(filtered_tasks)} encontradas)")

        for task in filtered_tasks:
            # Card de tarefa responsivo
            with st.container():
                # Header da tarefa
                task_col1, task_col2 = st.columns([3, 1])

                with task_col1:
                    # Ícone de prioridade
                    priority_icon = "🔴" if task['prioridade'] == 'Alta' else "🟡" if task[
                                                                                        'prioridade'] == 'Média' else "🟢"
                    st.markdown(f"**{priority_icon} {task['titulo']}**")

                with task_col2:
                    # Status badge
                    status_colors = {
                        'Pendente': '#F59E0B',
                        'Em Andamento': '#3B82F6',
                        'Concluída': '#10B981'
                    }
                    status_color = status_colors.get(task['status'], '#6B7280')
                    st.markdown(f"""
                        <div style="background: {status_color}20; color: {status_color}; 
                                   padding: 0.25rem 0.5rem; border-radius: 8px; 
                                   text-align: center; font-size: 0.8rem; font-weight: 500;">
                            {task['status']}
                        </div>
                    """, unsafe_allow_html=True)

                # Detalhes da tarefa
                task_detail_col1, task_detail_col2 = st.columns(2)

                with task_detail_col1:
                    st.write(f"**Projeto:** {task['projeto']}")
                    st.write(f"**Responsável:** {task['responsavel']}")

                with task_detail_col2:
                    st.write(f"**Prioridade:** {task['prioridade']}")
                    st.write(f"**Prazo:** {task['data_limite']}")

                # Barra de progresso
                st.write(f"**Progresso: {task['progresso']}%**")
                progress_color = "#10B981" if task['progresso'] == 100 else "#3B82F6" if task[
                                                                                             'progresso'] > 0 else "#F59E0B"
                st.progress(task['progresso'] / 100)

                # Ações da tarefa
                action_col1, action_col2, action_col3 = st.columns(3)

                with action_col1:
                    if st.button(f"✏️ Editar", key=f"edit_task_{task['id']}", type="secondary"):
                        st.info("Funcionalidade de edição será implementada!")

                with action_col2:
                    if st.button(f"💬 Comentar", key=f"comment_task_{task['id']}", type="secondary"):
                        st.info("Funcionalidade de comentários será implementada!")

                with action_col3:
                    if task['status'] != 'Concluída':
                        if st.button(f"✅ Finalizar", key=f"finish_task_{task['id']}", type="primary"):
                            # Atualizar status da tarefa
                            for i, t in enumerate(st.session_state.tasks):
                                if t['id'] == task['id']:
                                    st.session_state.tasks[i]['status'] = 'Concluída'
                                    st.session_state.tasks[i]['progresso'] = 100
                                    break
                            st.success("Tarefa finalizada!")
                            st.rerun()

                st.divider()
    else:
        st.info("📝 Nenhuma tarefa encontrada com os filtros aplicados.")

# ================================
# PÁGINA COMENTÁRIOS - RESPONSIVA
# ================================
elif page == "💬 Comentários":
    st.header("💬 Sistema de Comentários")

    # Seletor de projeto
    selected_project = st.selectbox(
        "Selecione o Projeto:",
        df_projects['nome'].tolist()
    )

    project_id = df_projects[df_projects['nome'] == selected_project]['id'].iloc[0]

    # Área para novo comentário - responsiva
    with st.expander("✍️ Novo Comentário", expanded=True):
        with st.form("novo_comentario"):
            comment_text = st.text_area(
                "Comentário:",
                height=100,
                placeholder="Digite seu comentário aqui..."
            )

            # Layout responsivo para usuários
            col1, col2 = st.columns([2, 1])

            with col1:
                tagged_users = st.multiselect(
                    "Marcar usuários:",
                    df_users['nome'].tolist(),
                    help="Selecione os usuários que devem ser notificados"
                )

            with col2:
                comment_priority = st.selectbox(
                    "Prioridade:",
                    ["Normal", "Importante", "Urgente"]
                )

            submitted = st.form_submit_button("💬 Adicionar Comentário", type="primary", use_container_width=True)

            if submitted and comment_text:
                new_comment = {
                    'id': len(st.session_state.comments) + 1,
                    'projeto_id': project_id,
                    'texto': comment_text,
                    'usuarios_marcados': tagged_users,
                    'prioridade': comment_priority,
                    'autor': 'João Diretor',  # Simulado
                    'timestamp': datetime.now()
                }
                st.session_state.comments.append(new_comment)
                st.success("✅ Comentário adicionado com sucesso!")
                st.rerun()

    # Exibir comentários do projeto
    project_comments = [c for c in st.session_state.comments if c.get('projeto_id') == project_id]

    if project_comments:
        st.divider()
        st.subheader(f"💬 Comentários do Projeto ({len(project_comments)})")

        # Ordenar comentários por data (mais recentes primeiro)
        project_comments.sort(key=lambda x: x['timestamp'], reverse=True)

        for comment in project_comments:
            # Card de comentário responsivo
            with st.container():
                # Header do comentário
                comment_col1, comment_col2 = st.columns([3, 1])

                with comment_col1:
                    priority_colors = {
                        'Normal': '#6B7280',
                        'Importante': '#F59E0B',
                        'Urgente': '#EF4444'
                    }
                    priority_color = priority_colors.get(comment.get('prioridade', 'Normal'), '#6B7280')

                    st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <div style="font-weight: bold; color: #1f2937;">
                                {comment.get('autor', 'Usuário')}
                            </div>
                            <div style="background: {priority_color}20; color: {priority_color}; 
                                       padding: 0.1rem 0.5rem; border-radius: 4px; font-size: 0.7rem;">
                                {comment.get('prioridade', 'Normal')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                with comment_col2:
                    st.markdown(f"""
                        <div style="text-align: right; font-size: 0.8rem; color: #6b7280;">
                            {comment['timestamp'].strftime('%d/%m/%Y')}<br>
                            {comment['timestamp'].strftime('%H:%M')}
                        </div>
                    """, unsafe_allow_html=True)

                # Conteúdo do comentário
                st.markdown(f"""
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; 
                               border-left: 4px solid {priority_color}; margin: 0.5rem 0;">
                        {comment['texto']}
                    </div>
                """, unsafe_allow_html=True)

                # Usuários marcados
                if comment.get('usuarios_marcados'):
                    st.markdown(f"""
                        <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">
                            👥 <em>Usuários marcados: {', '.join(comment['usuarios_marcados'])}</em>
                        </div>
                    """, unsafe_allow_html=True)

                # Ações do comentário
                action_col1, action_col2, action_col3 = st.columns([1, 1, 2])

                with action_col1:
                    if st.button("👍", key=f"like_{comment['id']}", help="Curtir"):
                        st.success("👍 Curtido!")

                with action_col2:
                    if st.button("💬", key=f"reply_{comment['id']}", help="Responder"):
                        st.info("Funcionalidade de resposta será implementada!")

                st.divider()
    else:
        st.info("📝 Nenhum comentário neste projeto. Seja o primeiro a comentar!")

# ================================
# PÁGINA FORMULÁRIOS - RESPONSIVA
# ================================
elif page == "📋 Formulários":
    st.header("📋 Formulários Customizáveis")

    # Formulários padrão se não existirem
    if not st.session_state.custom_forms:
        default_forms = [
            {
                'id': 1,
                'nome': 'Inspeção de Segurança',
                'tipo': 'seguranca',
                'campos': ['EPIs utilizados', 'Área sinalizada', 'Condições do tempo'],
                'obrigatorio': True,
                'frequencia': 'Diária'
            },
            {
                'id': 2,
                'nome': 'Relatório de Progresso',
                'tipo': 'progresso',
                'campos': ['Atividades realizadas', 'Percentual concluído', 'Próximos passos'],
                'obrigatorio': False,
                'frequencia': 'Semanal'
            },
            {
                'id': 3,
                'nome': 'Controle de Materiais',
                'tipo': 'materiais',
                'campos': ['Material utilizado', 'Quantidade', 'Fornecedor', 'Estado de conservação'],
                'obrigatorio': True,
                'frequencia': 'Por demanda'
            }
        ]
        st.session_state.custom_forms.extend(default_forms)

    # Tabs para organizar melhor
    tab1, tab2, tab3 = st.tabs(["📝 Formulários Disponíveis", "➕ Criar Formulário", "📊 Respostas"])

    with tab1:
        st.subheader("Formulários Disponíveis")

        # Filtros
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            tipo_form_filter = st.selectbox(
                "Filtrar por tipo:",
                ["Todos", "seguranca", "progresso", "materiais", "qualidade"]
            )

        with filter_col2:
            search_form = st.text_input("🔍 Buscar formulário:")

        # Exibir formulários
        for form in st.session_state.custom_forms:
            show_form = True
            if tipo_form_filter != "Todos" and form['tipo'] != tipo_form_filter:
                show_form = False
            if search_form and search_form.lower() not in form['nome'].lower():
                show_form = False

            if show_form:
                with st.expander(f"📋 {form['nome']} ({'Obrigatório' if form.get('obrigatorio') else 'Opcional'})"):
                    form_col1, form_col2 = st.columns([2, 1])

                    with form_col1:
                        st.write(f"**Tipo:** {form['tipo'].title()}")
                        st.write(f"**Frequência:** {form.get('frequencia', 'Não definida')}")
                        st.write(f"**Campos:** {len(form['campos'])} campos")

                        # Mostrar campos
                        st.markdown("**Campos do formulário:**")
                        for i, campo in enumerate(form['campos'], 1):
                            st.write(f"{i}. {campo}")

                    with form_col2:
                        st.write("**Ações:**")

                        if st.button(f"📝 Preencher", key=f"fill_{form['id']}", type="primary"):
                            st.session_state[f'filling_form_{form["id"]}'] = True
                            st.rerun()

                        if st.button(f"📊 Ver Respostas", key=f"view_{form['id']}", type="secondary"):
                            st.info(f"Funcionalidade de visualizar respostas do formulário '{form['nome']}'")

                        if st.button(f"✏️ Editar", key=f"edit_form_{form['id']}", type="secondary"):
                            st.info("Funcionalidade de edição será implementada!")

                    # Formulário de preenchimento inline
                    if st.session_state.get(f'filling_form_{form["id"]}'):
                        st.divider()
                        st.markdown("**📝 Preenchendo Formulário:**")

                        with st.form(f"form_response_{form['id']}"):
                            responses = {}

                            for field in form['campos']:
                                if 'percentual' in field.lower() or 'quantidade' in field.lower():
                                    responses[field] = st.number_input(f"{field}:", min_value=0)
                                elif 'data' in field.lower():
                                    responses[field] = st.date_input(f"{field}:")
                                elif len(field) > 50:  # Campo longo = text_area
                                    responses[field] = st.text_area(f"{field}:")
                                else:
                                    responses[field] = st.text_input(f"{field}:")

                            form_col1, form_col2 = st.columns(2)

                            with form_col1:
                                submitted_form = st.form_submit_button("💾 Salvar Respostas", type="primary")

                            with form_col2:
                                cancel_form = st.form_submit_button("❌ Cancelar", type="secondary")

                            if submitted_form:
                                new_response = {
                                    'id': len(st.session_state.form_responses) + 1,
                                    'form_id': form['id'],
                                    'form_name': form['nome'],
                                    'responses': responses,
                                    'timestamp': datetime.now(),
                                    'user': 'João Diretor'  # Simulado
                                }
                                st.session_state.form_responses.append(new_response)
                                st.session_state[f'filling_form_{form["id"]}'] = False
                                st.success("✅ Formulário preenchido com sucesso!")
                                st.rerun()

                            if cancel_form:
                                st.session_state[f'filling_form_{form["id"]}'] = False
                                st.rerun()

    with tab2:
        st.subheader("➕ Criar Novo Formulário")

        with st.form("novo_formulario"):
            new_form_col1, new_form_col2 = st.columns(2)

            with new_form_col1:
                form_name = st.text_input("Nome do Formulário:")
                form_type = st.selectbox("Tipo:", ["seguranca", "progresso", "materiais", "qualidade", "outro"])
                form_required = st.checkbox("Obrigatório")

            with new_form_col2:
                form_frequency = st.selectbox("Frequência:", ["Diária", "Semanal", "Mensal", "Por demanda"])
                form_description = st.text_area("Descrição:", height=100)

            st.markdown("**Campos do Formulário:**")
            num_fields = st.number_input("Número de campos:", min_value=1, max_value=10, value=3)

            form_fields = []
            field_cols = st.columns(2)

            for i in range(num_fields):
                col_idx = i % 2
                with field_cols[col_idx]:
                    field_name = st.text_input(f"Campo {i + 1}:", key=f"field_{i}")
                    if field_name:
                        form_fields.append(field_name)

            create_form_btn = st.form_submit_button("🎯 Criar Formulário", type="primary")

            if create_form_btn and form_name and form_fields:
                new_form = {
                    'id': len(st.session_state.custom_forms) + 1,
                    'nome': form_name,
                    'tipo': form_type,
                    'campos': form_fields,
                    'obrigatorio': form_required,
                    'frequencia': form_frequency,
                    'descricao': form_description,
                    'created_at': datetime.now()
                }
                st.session_state.custom_forms.append(new_form)
                st.success(f"✅ Formulário '{form_name}' criado com sucesso!")
                st.rerun()

    with tab3:
        st.subheader("📊 Respostas dos Formulários")

        if st.session_state.form_responses:
            # Estatísticas
            total_responses = len(st.session_state.form_responses)
            forms_with_responses = len(set([r['form_id'] for r in st.session_state.form_responses]))

            response_metrics = [
                ("Total Respostas", total_responses, "+5"),
                ("Formulários Respondidos", forms_with_responses, "+2")
            ]
            create_responsive_metrics(response_metrics)

            st.divider()

            # Listar respostas
            for response in st.session_state.form_responses:
                with st.expander(f"📝 {response['form_name']} - {response['timestamp'].strftime('%d/%m/%Y %H:%M')}"):
                    st.write(f"**Usuário:** {response['user']}")
                    st.write(f"**Data:** {response['timestamp'].strftime('%d/%m/%Y às %H:%M')}")

                    st.markdown("**Respostas:**")
                    for field, answer in response['responses'].items():
                        st.write(f"• **{field}:** {answer}")
        else:
            st.info("📝 Nenhuma resposta de formulário encontrada.")

# ================================
# PÁGINA USUÁRIOS - RESPONSIVA
# ================================
elif page == "👥 Usuários":
    st.header("👥 Gestão de Usuários")

    # Estatísticas de usuários
    total_users = len(df_users)
    active_users = len(df_users[df_users['ativo'] == True])
    supervisors = len(df_users[df_users['tipo'] == 'supervisor'])
    technicians = len(df_users[df_users['tipo'] == 'tecnico'])

    user_metrics = [
        ("Total Usuários", total_users, None),
        ("Usuários Ativos", active_users, f"+{active_users}"),
        ("Supervisores", supervisors, None),
        ("Técnicos", technicians, None)
    ]

    create_responsive_metrics(user_metrics)

    st.divider()

    # Filtros
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        user_type_filter = st.selectbox(
            "Filtrar por tipo:",
            ["Todos", "supervisor", "tecnico"]
        )

    with filter_col2:
        user_status_filter = st.selectbox(
            "Filtrar por status:",
            ["Todos", "Ativo", "Inativo"]
        )

    # Botão para adicionar usuário
    if st.button("➕ Adicionar Usuário", type="primary"):
        st.info("Funcionalidade de adicionar usuário será implementada!")

    st.divider()

    # Lista de usuários com cards responsivos
    filtered_users = df_users.copy()

    if user_type_filter != "Todos":
        filtered_users = filtered_users[filtered_users['tipo'] == user_type_filter]

    if user_status_filter != "Todos":
        active_filter = user_status_filter == "Ativo"
        filtered_users = filtered_users[filtered_users['ativo'] == active_filter]

    st.subheader(f"👥 Usuários ({len(filtered_users)} encontrados)")

    for idx, user in filtered_users.iterrows():
        with st.container():
            # Card de usuário
            user_col1, user_col2, user_col3 = st.columns([1, 2, 1])

            with user_col1:
                # Avatar simulado
                initials = ''.join([n[0] for n in user['nome'].split()[:2]]).upper()
                avatar_color = "#3B82F6" if user['tipo'] == 'supervisor' else "#10B981"

                st.markdown(f"""
                    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                        <div style="width: 60px; height: 60px; background: {avatar_color}; 
                                   border-radius: 50%; display: flex; align-items: center; 
                                   justify-content: center; color: white; font-weight: bold; font-size: 1.2rem;">
                            {initials}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with user_col2:
                st.markdown(f"**{user['nome']}**")
                st.write(f"📧 {user['email']}")
                st.write(f"🔧 {user['tipo'].title()}")
                st.write(f"🔑 {user['nivel_acesso'].title()}")

            with user_col3:
                # Status badge
                status_color = "#10B981" if user['ativo'] else "#EF4444"
                status_text = "✅ Ativo" if user['ativo'] else "❌ Inativo"

                st.markdown(f"""
                    <div style="background: {status_color}20; color: {status_color}; 
                               padding: 0.5rem; border-radius: 8px; text-align: center; 
                               font-size: 0.9rem; font-weight: 500; margin-bottom: 1rem;">
                        {status_text}
                    </div>
                """, unsafe_allow_html=True)

                # Ações
                if st.button(f"✏️ Editar", key=f"edit_user_{user['id']}", type="secondary"):
                    st.info(f"Editar usuário: {user['nome']}")

                if st.button(f"📊 Relatório", key=f"report_user_{user['id']}", type="secondary"):
                    st.info(f"Relatório de: {user['nome']}")

            st.divider()

# ================================
# PÁGINA RELATÓRIOS - RESPONSIVA
# ================================
elif page == "📈 Relatórios":
    st.header("📈 Relatórios Gerenciais")

    # Seletor de relatório com melhor organização
    report_tabs = st.tabs([
        "📊 Executivo",
        "💰 Financeiro",
        "🔧 Materiais",
        "👥 Produtividade",
        "📋 Personalizado"
    ])

    with report_tabs[0]:  # Relatório Executivo
        st.subheader("📊 Resumo Executivo")

        # KPIs principais
        obras_ativas = len(df_projects[df_projects['status'] != 'finalizada'])
        obras_finalizadas = len(df_projects[df_projects['status'] == 'finalizada'])
        taxa_sucesso = (obras_finalizadas / len(df_projects)) * 100

        total_orcamento = df_projects['orcamento'].sum()
        total_gasto = df_projects['gasto'].sum()
        eficiencia_orcamentaria = ((total_orcamento - total_gasto) / total_orcamento) * 100

        executive_metrics = [
            ("Taxa de Sucesso", f"{taxa_sucesso:.1f}%", "+2%"),
            ("Eficiência Orçamentária", f"{eficiencia_orcamentaria:.1f}%", "+1%"),
            ("Obras Ativas", obras_ativas, "+2"),
            ("Produtividade", "8.4", "+0.3")
        ]

        create_responsive_metrics(executive_metrics)

        st.divider()

        # Highlights e alertas em layout responsivo
        highlight_col1, highlight_col2 = st.columns(2)

        with highlight_col1:
            st.success("**✅ Destaques Positivos**")
            highlights = [
                "Obra Centro concluída 5% acima do cronograma",
                "Economia de 8% no orçamento da manutenção",
                "Zero acidentes de trabalho registrados",
                "Equipe com alta satisfação (95%)"
            ]
            for highlight in highlights:
                st.write(f"• {highlight}")

        with highlight_col2:
            st.warning("**⚠️ Pontos de Atenção**")
            warnings = [
                "Atraso na entrega de transformadores",
                "Equipe reduzida por licenças médicas",
                "Pendência de licença ambiental",
                "Chuvas afetando cronograma externo"
            ]
            for warning in warnings:
                st.write(f"• {warning}")

        # Gráfico de evolução temporal
        st.subheader("📈 Evolução dos Projetos")

        # Dados simulados de evolução
        evolution_data = {
            'mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago'],
            'obras_iniciadas': [2, 1, 3, 2, 1, 2, 1, 2],
            'obras_concluidas': [1, 2, 1, 3, 2, 1, 2, 1],
            'orcamento_gasto': [450000, 680000, 520000, 750000, 620000, 480000, 590000, 670000]
        }

        evolution_df = pd.DataFrame(evolution_data)

        fig_evolution = px.line(
            evolution_df,
            x='mes',
            y=['obras_iniciadas', 'obras_concluidas'],
            title="Obras Iniciadas vs Concluídas por Mês",
            labels={'value': 'Quantidade', 'variable': 'Tipo'}
        )
        fig_evolution.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_evolution, use_container_width=True)

    with report_tabs[1]:  # Análise Financeira
        st.subheader("💰 Análise Financeira Detalhada")

        # Criar DataFrame financeiro
        df_financial = df_projects.copy()
        df_financial['percentual_gasto'] = (df_financial['gasto'] / df_financial['orcamento']) * 100
        df_financial['saldo'] = df_financial['orcamento'] - df_financial['gasto']
        df_financial['status_orcamento'] = df_financial['percentual_gasto'].apply(
            lambda x: '🟢 Dentro do orçamento' if x < 70 else
            '🟡 Atenção' if x < 90 else '🔴 Crítico'
        )

        # Métricas financeiras
        total_orcamento = df_financial['orcamento'].sum()
        total_gasto = df_financial['gasto'].sum()
        total_saldo = df_financial['saldo'].sum()
        economia_media = df_financial['saldo'].mean()

        financial_metrics = [
            ("Orçamento Total", f"R$ {total_orcamento / 1000:.0f}K", None),
            ("Total Gasto", f"R$ {total_gasto / 1000:.0f}K", None),
            ("Saldo Total", f"R$ {total_saldo / 1000:.0f}K", "+8%"),
            ("Economia Média", f"R$ {economia_media / 1000:.0f}K", "+5%")
        ]

        create_responsive_metrics(financial_metrics)

        # Tabela financeira responsiva
        st.subheader("💼 Detalhamento por Projeto")

        # Preparar dados para visualização mobile-friendly
        financial_display = df_financial[
            ['nome', 'orcamento', 'gasto', 'percentual_gasto', 'saldo', 'status_orcamento']].copy()
        financial_display['orcamento'] = financial_display['orcamento'].apply(lambda x: f"R$ {x:,.0f}")
        financial_display['gasto'] = financial_display['gasto'].apply(lambda x: f"R$ {x:,.0f}")
        financial_display['saldo'] = financial_display['saldo'].apply(lambda x: f"R$ {x:,.0f}")
        financial_display['percentual_gasto'] = financial_display['percentual_gasto'].apply(lambda x: f"{x:.1f}%")

        financial_display.columns = ['Projeto', 'Orçamento', 'Gasto', '% Gasto', 'Saldo', 'Status']

        st.dataframe(financial_display, use_container_width=True, hide_index=True)

        # Gráfico de distribuição orçamentária
        st.subheader("📊 Distribuição Orçamentária")

        fig_budget_dist = px.pie(
            df_financial,
            values='orcamento',
            names='nome',
            title="Distribuição do Orçamento por Projeto"
        )
        fig_budget_dist.update_layout(height=400)
        st.plotly_chart(fig_budget_dist, use_container_width=True)

    with report_tabs[2]:  # Consumo de Materiais
        st.subheader("🔧 Análise de Consumo de Materiais")

        # Análise de materiais
        df_materials_analysis = df_materials.copy()
        df_materials_analysis['percentual_uso'] = (df_materials_analysis['usado'] / df_materials_analysis[
            'quantidade']) * 100
        df_materials_analysis['valor_usado'] = df_materials_analysis['usado'] * df_materials_analysis['custo_unitario']
        df_materials_analysis['valor_total'] = df_materials_analysis['quantidade'] * df_materials_analysis[
            'custo_unitario']

        # Métricas de materiais
        total_materiais = len(df_materials_analysis)
        valor_total_materiais = df_materials_analysis['valor_total'].sum()
        valor_usado_materiais = df_materials_analysis['valor_usado'].sum()
        eficiencia_materiais = (valor_usado_materiais / valor_total_materiais) * 100

        materials_metrics = [
            ("Total Materiais", total_materiais, None),
            ("Valor Total", f"R$ {valor_total_materiais / 1000:.0f}K", None),
            ("Valor Usado", f"R$ {valor_usado_materiais / 1000:.0f}K", None),
            ("Eficiência", f"{eficiencia_materiais:.1f}%", "+3%")
        ]

        create_responsive_metrics(materials_metrics)

        # Top materiais por valor
        st.subheader("💎 Materiais de Maior Valor")

        top_materials = df_materials_analysis.nlargest(5, 'valor_total')[['material', 'valor_total', 'percentual_uso']]

        fig_top_materials = px.bar(
            top_materials,
            x='valor_total',
            y='material',
            orientation='h',
            title="Top 5 Materiais por Valor Total",
            labels={'valor_total': 'Valor (R$)', 'material': 'Material'}
        )
        fig_top_materials.update_layout(height=400)
        st.plotly_chart(fig_top_materials, use_container_width=True)

        # Status de estoque
        st.subheader("📦 Status de Estoque")

        for _, material in df_materials_analysis.iterrows():
            usage_pct = material['percentual_uso']

            # Card de material responsivo
            with st.container():
                mat_col1, mat_col2, mat_col3 = st.columns([2, 1, 1])

                with mat_col1:
                    st.write(f"**{material['material']}**")
                    st.write(f"Projeto ID: {material['projeto_id']}")

                with mat_col2:
                    st.write(f"**{material['usado']}/{material['quantidade']} {material['unidade']}**")
                    st.progress(usage_pct / 100)

                with mat_col3:
                    if usage_pct >= 90:
                        st.error(f"{usage_pct:.0f}% - Crítico")
                    elif usage_pct >= 70:
                        st.warning(f"{usage_pct:.0f}% - Atenção")
                    else:
                        st.success(f"{usage_pct:.0f}% - Normal")

                st.divider()

    with report_tabs[3]:  # Produtividade
        st.subheader("👥 Análise de Produtividade")

        # Dados de produtividade simulados
        productivity_data = {
            'supervisor': df_projects['supervisor'].tolist(),
            'projetos': [1, 1, 1, 1, 1],  # Cada supervisor tem 1 projeto na amostra
            'progresso_medio': df_projects.groupby('supervisor')['progresso'].mean().values,
            'eficiencia_orcamento': (
                        (df_projects['orcamento'] - df_projects['gasto']) / df_projects['orcamento'] * 100).values,
            'equipe_size': df_projects['equipe_size'].tolist()
        }

        productivity_df = pd.DataFrame(productivity_data)

        # Métricas de produtividade
        prod_metrics = [
            ("Supervisores Ativos", len(productivity_df), None),
            ("Progresso Médio", f"{productivity_df['progresso_medio'].mean():.1f}%", "+5%"),
            ("Eficiência Média", f"{productivity_df['eficiencia_orcamento'].mean():.1f}%", "+2%"),
            ("Equipe Total", productivity_df['equipe_size'].sum(), "+3")
        ]

        create_responsive_metrics(prod_metrics)

        # Ranking de supervisores
        st.subheader("🏆 Ranking de Supervisores")

        productivity_df['score'] = (productivity_df['progresso_medio'] + productivity_df['eficiencia_orcamento']) / 2
        productivity_df = productivity_df.sort_values('score', ascending=False)

        for i, (_, supervisor) in enumerate(productivity_df.iterrows(), 1):
            with st.container():
                rank_col1, rank_col2, rank_col3 = st.columns([1, 2, 1])

                with rank_col1:
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                    st.markdown(f"### {medal}")

                with rank_col2:
                    st.write(f"**{supervisor['supervisor']}**")
                    st.write(f"Progresso: {supervisor['progresso_medio']:.1f}%")
                    st.write(f"Eficiência: {supervisor['eficiencia_orcamento']:.1f}%")

                with rank_col3:
                    score_color = "#10B981" if supervisor['score'] >= 80 else "#F59E0B" if supervisor[
                                                                                               'score'] >= 60 else "#EF4444"
                    st.markdown(f"""
                        <div style="background: {score_color}20; color: {score_color}; 
                                   padding: 1rem; border-radius: 8px; text-align: center; font-weight: bold;">
                            {supervisor['score']:.1f}
                        </div>
                    """, unsafe_allow_html=True)

                st.divider()

    with report_tabs[4]:  # Relatório Personalizado
        st.subheader("📋 Relatório Personalizado")

        st.info("🚧 Funcionalidade em desenvolvimento - Em breve você poderá criar relatórios personalizados!")

        # Preview da funcionalidade
        with st.expander("🔮 Preview - Construtor de Relatórios"):
            custom_col1, custom_col2 = st.columns(2)

            with custom_col1:
                st.multiselect("Selecionar Projetos:", df_projects['nome'].tolist())
                st.multiselect("Métricas:", ["Progresso", "Orçamento", "Materiais", "Equipe"])
                st.selectbox("Período:", ["Última Semana", "Último Mês", "Trimestre", "Personalizado"])

            with custom_col2:
                st.selectbox("Formato:", ["PDF", "Excel", "PowerPoint"])
                st.selectbox("Frequência:", ["Uma vez", "Diário", "Semanal", "Mensal"])
                st.text_input("Email para envio:")

            if st.button("🎯 Gerar Relatório Personalizado", type="primary"):
                st.success("Relatório personalizado será gerado em breve!")

    # Botões de ação para todos os relatórios
    st.divider()

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("📥 Exportar PDF", type="primary", use_container_width=True):
            st.success("📄 Relatório PDF gerado com sucesso!")

    with action_col2:
        if st.button("📊 Exportar Excel", type="secondary", use_container_width=True):
            st.success("📈 Planilha Excel gerada com sucesso!")

    with action_col3:
        if st.button("📧 Enviar por Email", type="secondary", use_container_width=True):
            st.success("📬 Relatório enviado por email!")

# ================================
# FOOTER RESPONSIVO
# ================================
st.divider()

# Footer adaptado para mobile
st.markdown(f"""
<div class="footer-content">
    <div class="footer-grid">
        <div>
            <strong>⚡ Sistema de Gestão de Obras Elétricas - Equatorial Energia</strong><br>
            <small>Versão 2.0 Mobile - Sistema Completo de Gestão</small>
        </div>
        <div style="text-align: right;">
            <small>Última atualização: {datetime.now().strftime("%d/%m/%Y às %H:%M")}<br>
            👥 Usuários: <strong>15</strong> | 🏗️ Obras ativas: <strong>{len(df_projects[df_projects['status'] != 'finalizada'])}</strong></small>
        </div>
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ddd;">
        <small>
            🚀 <strong>Mobile First:</strong> Dashboard | Projetos | Mapa | Tarefas | Comentários | Formulários | Usuários | Relatórios<br>
            📱 <strong>Otimizado para:</strong> Smartphones | Tablets | Desktop | PWA Ready
        </small>
    </div>
</div>
""", unsafe_allow_html=True)

# Adicionar indicador de conectividade (simulado)
if st.sidebar.button("📶 Status da Conexão"):
    st.sidebar.success("🟢 Online - Sincronizado")
    st.sidebar.info("📊 Última sincronização: Agora")
    st.sidebar.info("💾 Dados salvos localmente: Sim")