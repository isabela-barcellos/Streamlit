import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

csv_path = "GUIDE_Excel.csv"

df = pd.read_csv(csv_path, sep=";", encoding="utf-8", nrows=5000, engine="c", on_bad_lines="skip", dtype=str)

if "data" not in st.session_state:
    st.session_state.data = pd.read_csv(csv_path, sep=";", encoding="utf-8", 
                                                nrows=5000, engine="c", 
                                                on_bad_lines="skip", dtype=str)

# Configuração da página
st.set_page_config(page_title="Dashboard para Microsoft", layout="wide")
st.sidebar.markdown("Desenvolvido por Isabela Barcellos [linkedin](https://www.linkedin.com/in/isabela-barcellos-freire-91263328a/)") #colocar link do linkedin

# Adicionando logo com streamlit-extras
# add_logo("logo.jpeg")

# Adicionando o logo
st.logo("logo_microsoft.png")

# Adicionando o logo no body
st.image("logo_microsoft_body.png", width=200)

st.title("Analise de previsões de incidentes de segurança da Microsoft")

st.write("A análise que precisa ser realizada visa prever incidentes significativos de segurança cibernética com base em um conjunto de dados robusto da Microsoft, contendo mais de 13 milhões de evidências e 1,6 milhão de alertas sobre incidentes. O objetivo é desenvolver técnicas e modelos de aprendizado de máquina para automatizar a triagem e remediação de incidentes de segurança, um processo que, devido ao volume crescente de ameaças, sobrecarrega os centros de operações de segurança (SOCs). A análise deverá explorar e comparar esses modelos para fornecer recomendações de resposta guiada, que apoiem analistas de SOC a tomar decisões informadas, com base em uma rica telemetria de segurança, incluindo técnicas MITRE ATT&CK e dados de mais de 6.100 organizações.")


