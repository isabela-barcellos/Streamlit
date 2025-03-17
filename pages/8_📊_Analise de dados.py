import numpy as np
import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go
import streamlit as st



st.set_page_config(page_title="Dados", page_icon="📊", layout="wide")

def categorizar_periodo(horario):
    hora = int(horario.split(':')[0])  
    if 6 <= hora < 12:
        return "Manhã"
    elif 12 <= hora < 18:
        return "Tarde"
    else:
        return "Noite"

pages = st.sidebar.selectbox("Abas de análise:", [
    "📊 Dados",
    "🎲Análise inicial dos dados",
    "📈 Distribuição Probabilística",
])

if pages == "📊 Dados":
    st.title("Apresentação dos dados e tipos de variáveis")
    
    if "data" in st.session_state:
        df = st.session_state.data
       
        
        colunas_desejadas = ["Id", "Timestamp", "Categoria", "Grau de Incidente", "Função de evidência", "Uso"]  
        df = df[colunas_desejadas]
        df = df.dropna()
        df["Id"] = df["Id"].astype(str).str.replace(",", ".", regex=True) 
        df["Id"] = pd.to_numeric(df["Id"], errors="coerce")  
        
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["data"] = df["Timestamp"].dt.date
        df["hora_minuto"] = df["Timestamp"].dt.strftime("%H:%M")  
        
        st.session_state.data = df  # Atualiza os dados na sessão
        
        st.subheader("🎲**Conjunto de dados utilizado:**")
        st.write("Iremos utilizar os seguintes dados: Categoria, Data, Hora, Grau de Incidente, Função de evidência e Uso. Cada um desses dados irá ajudar a entender os ataques.")
        st.write("Teremos então a categoria, grau de incidente e função de evidência desses ataques para entender o impacto causado. A data e hora para saber se o horário influencia na quantidade de ataques. O uso irá determinar se era público ou privado.")
        st.dataframe(df.head(500))
        
        st.subheader("🔍**Identificação do tipo das variáveis:**")
        st.write("**Id**: ID único para cada par OrgId-IncidentId (Quantitativa Discreta)")
        st.write("**Timestamp**: Data e hora em que o alerta foi criado (Quantitativa Discreta)")
        st.write("**Categoria**: Categoria do alerta (Qualitativa Nominal)")
        st.write("**Grau de Incidente**: Grau atribuído ao incidente pelo SOC (Qualitativa Nominal)")
        st.write("**Função de evidência**: Função da evidência na investigação (Qualitativa Nominal)")
        st.write("**Uso**: O uso é definido em público ou privado (Qualitativa Nominal)")
        st.write("**Data**: Data em que o alerta foi criado - (Quantitativa Discreta)")
        st.write("**hora_minuto**: Hora em que o alerta foi criado - (Quantitativa Discreta)")
        
        st.subheader("❓*Perguntas de análise**")
        st.write("Em que horário ou perídos mais acontecem os ataques?")
        st.write("Quais tipos de ataques acontecem com mais frequência?")
        

elif pages == "🎲Análise inicial dos dados":
    st.title("Análise inicial dos dados") 
    st.write("Interpretar os dados")
    
    if "data" in st.session_state:
        df = st.session_state.data.copy()
        
        if 'hora_minuto' in df.columns and 'Grau de Incidente' in df.columns:
            df['Periodo'] = df['hora_minuto'].apply(categorizar_periodo)

            # Contagem de ataques por período
            ataques_por_periodo = df['Periodo'].value_counts()

            # Contagem do impacto dos incidentes por período
            impacto_por_periodo = df.groupby('Periodo')['Grau de Incidente'].value_counts().unstack().fillna(0)

            
            grau_mais_frequente_por_periodo = impacto_por_periodo.idxmax(axis=1)  # Grau mais frequente por período
            impacto_total_por_periodo = impacto_por_periodo.sum(axis=1)  # Total de incidentes por período
            
            periodo_maior_impacto = impacto_total_por_periodo.idxmax()
            maior_quantidade_impacto = impacto_total_por_periodo.max()

            st.write("### Distribuição de ataques por período do dia")
            st.bar_chart(ataques_por_periodo)

            st.write("### Grau de Incidente por Período")
            st.dataframe(impacto_por_periodo)

            st.write(f"📌 **Período com maior impacto:** {periodo_maior_impacto} ({maior_quantidade_impacto} incidentes totais)")

            st.write("### Grau de incidente mais comum por período:")
            st.dataframe(grau_mais_frequente_por_periodo)
            
            # Frequência de ataques por dia
            st.write("### Frequência de ataques ao longo do tempo")
            ataques_por_dia = df['data'].value_counts().sort_index()
            st.line_chart(ataques_por_dia)
        


if pages == "📈 Distribuição Probabilística":
    st.title("Distribuição Probabilística")
    if "data" in st.session_state:
        df = st.session_state.data.copy()
        
        if 'Grau de Incidente' in df.columns:
         
            st.write("Valores únicos de 'Grau de Incidente':", df['Grau de Incidente'].unique())
      
            df['Acerto_Modelo'] = df['Grau de Incidente'].apply(lambda x: 1 if x in ["true positive", "true negative", "false positive", "false negative"] else 0)
   
            st.write("Distribuição de 'Acerto_Modelo':", df['Acerto_Modelo'].value_counts())

       
            media_acertos = df['Acerto_Modelo'].mean()
      
            st.write(f"Média de acertos do modelo: {media_acertos:.2f}")
            
            #  ajustando a média 
            if media_acertos == 0:
                st.write("A média de acertos é zero. Para calcular a distribuição de Poisson, ajustaremos a média para um valor mínimo.")
                media_acertos = 0.1  
      
            x = np.arange(0, df['Acerto_Modelo'].max() + 5)  # Valores possíveis
            poisson_dist = stats.poisson.pmf(x, media_acertos)  # Cálculo da Poisson
            
            st.bar_chart(pd.DataFrame({'Probabilidade': poisson_dist}, index=x))
            
            st.write("A distribuição de Poisson modela a probabilidade de um certo número de acertos do modelo em um intervalo de tempo fixo.")
            
        

       
            st.header("Distribuição Normal")
            st.markdown('''A distribuição normal, também conhecida como distribuição de Gauss, é uma das mais importantes na estatística e na ciência de dados. Ela descreve fenômenos naturais e sociais em que os valores se concentram ao redor de uma média, formando um gráfico em forma de sino. Esse comportamento é comum em diversas situações do dia a dia, como alturas de pessoas, notas em provas e erros de medição em experimentos.''')
            
         
            mu = st.number_input("Média (μ):", value=media_acertos) 
            sigma = st.number_input("Desvio Padrão (σ):", value=1.0, min_value=0.1)
            
           
            x_normal = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
            y_normal = stats.norm.pdf(x_normal, mu, sigma)
            y_normal_cdf = stats.norm.cdf(x_normal, mu, sigma)
            
            # gráfico para a distribuição normal
            col1, col2 = st.columns(2)
            fig_normal = go.Figure()
            fig_normal.add_trace(go.Scatter(x=x_normal, y=y_normal, mode='lines', name='PDF'))
            fig_normal.update_layout(title="Distribuição Normal", xaxis_title="Valores", yaxis_title="Densidade de Probabilidade")
            col1.plotly_chart(fig_normal)
            
            # Gráfico Função de Distribuição Acumulada
            fig_normal_cdf = go.Figure()
            fig_normal_cdf.add_trace(go.Scatter(x=x_normal, y=y_normal_cdf, mode='lines', name='CDF'))
            fig_normal_cdf.update_layout(title="Distribuição Normal Acumulada", xaxis_title="Valores", yaxis_title="Probabilidade Acumulada")
            col2.plotly_chart(fig_normal_cdf)

      
