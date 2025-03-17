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
        
        st.subheader("❓**Perguntas de análise**")
        st.write("Em que horário ou perídos mais acontecem os ataques?")
        st.write("Quais tipos de ataques acontecem com mais frequência?")
        st.write("Quais tipos de incidentes acontecem com mais frequência?")
        st.write("Quais tipos de incidentes aparecem nos períodos do dia?")
        st.write("Como saber a relação existente entre os horários e os ataques?")
        st.write("Qual a probabilidade de acontecer um ataque concreto?")
        
        

elif pages == "🎲Análise inicial dos dados":
    st.title("Análise inicial dos dados") 
    st.subheader("Interpretação os dados")
    
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
            
            st.write('Podemos observar que o período do dia com mais ataques, é o período da noite e o que recebe menos ataques é o período da manhã')

            st.write("### Grau de Incidente por Período")
            st.dataframe(impacto_por_periodo)

            st.write(f"**Período com maior impacto:** {periodo_maior_impacto} ({maior_quantidade_impacto} incidentes totais)")
            st.write('Podemos concluir então que temos uma **associação** entre o perído de ataques com o impacto dele.')

            st.write("### Grau de incidente mais comum por período:")
            st.dataframe(grau_mais_frequente_por_periodo)
            
            # Frequência de ataques por dia
            st.write("### Frequência de ataques ao longo do tempo")
            ataques_por_dia = df['data'].value_counts().sort_index()
            st.line_chart(ataques_por_dia)
        


if pages == "📈 Distribuição Probabilística":
    st.title("Distribuição Probabilística")
    st.subheader("Distribuição de Poisson")
    
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
                st.write( "Para calcular essa média foi necessário diminuir a média, para que a probabilidade pudesse ser calculada")
                media_acertos = 0.1  
      
            x = np.arange(0, df['Acerto_Modelo'].max() + 5)  # Valores possíveis
            poisson_dist = stats.poisson.pmf(x, media_acertos)  # Cálculo da Poisson
            
            st.bar_chart(pd.DataFrame({'Probabilidade': poisson_dist}, index=x))
            
            st.write("A distribuição de Poisson modela a probabilidade de um certo número de acertos do modelo em um intervalo de tempo fixo.")
            st.write("Ao observarmos o gráfico obtido teremos então mais chances do número de acerto ser 0 e menos chance de ser 2. Ou seja a probabilidade de termo uma verdadeiro true e um verdadeiro false é 0, com poucas chances dessa probabilidade ser 2")
            
        

       
            st.header("Distribuição Normal")
            st.markdown('''A distribuição normal está interativa, onde podemos observar como a distribuição normal e acumulada vão se comportar com o valor que ddeseja. Ela irá trazer os valores que estão concentrados ao redor da média , por isso o gráfico tem um formato de sino.''')
            
         
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
            
            st.markdown('''Se observa que a distribuição normal sempre será maior em 0, já que o número de acertos está mais próximo de zero, assim como na acamulada, momento em que ele começa a crescer em 0.''')

      
