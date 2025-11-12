import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

st.set_page_config(page_title="Genesights", layout="wide")


def calculate_delta(df, column):
    series = df[column].dropna()
    if len(series) < 2:
        return 0, 0
    current_value = series.iloc[-1]
    previous_value = series.iloc[-2]
    delta = current_value - previous_value
    delta_percent = (delta / previous_value) * 100 if previous_value != 0 else 0
    return delta, delta_percent


def is_valid_column(df, col_name):
    return col_name in df.columns and df[col_name].dropna().shape[0] > 0

DB_USER = "postgres"
DB_PASSWORD = "admin"
DB_HOST = "localhost" 
DB_PORT = "5432"
DB_NAME = "GENESIGHTS_DATABASE"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


with st.sidebar:
    st.image("src/img/logo.png", caption="Genesights")
    st.title("Genesights", anchor="Genesights")
    uploaded_file = st.file_uploader("Carregar arquivo CSV ou XLSX", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    numeric_cols = ["Max", "Min", "Média", "Desvio Padrão", "Variação de Porcentagem"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Estado" in df.columns and "Produto" in df.columns:
        with st.sidebar:
            state = st.selectbox("Selecione o estado", df["Estado"].unique().tolist())
            product = st.selectbox("Selecione o produto", df["Produto"].unique().tolist())
        df_filtered = df[(df["Estado"] == state) & (df["Produto"] == product)]
    else:
        df_filtered = df.copy()
        state = None
        product = None

    st.header("📊 Métricas de Preços por Período e Local")

    estados_coords = {
        "MA": (-2.5297, -44.3028),
        "PI": (-5.0892, -42.8019),
        "CE": (-3.7172, -38.5433),
        "RN": (-5.7945, -35.2110),
        "PB": (-7.11532, -34.8610),
        "PE": (-8.0476, -34.8770),
        "AL": (-9.6659, -35.7350),
        "SE": (-10.9472, -37.0731),
        "BA": (-12.9714, -38.5014)
    }

    COLS_TO_PLOT = ["Max", "Min", "Média", "Desvio Padrão", "Variação de Porcentagem"]

    for col_name in COLS_TO_PLOT:
        if is_valid_column(df_filtered, col_name):
            data_series = df_filtered[[col_name]].dropna()
            data_series.reset_index(drop=True, inplace=True)
            x = range(1, len(data_series) + 1)
            y = data_series[col_name]

            delta, delta_percent = calculate_delta(df_filtered, col_name)
            current_value = y.iloc[-1]

            st.markdown(f"### 🧾 {state} - {product} - {col_name}")

            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(
                    label=f"{col_name}",
                    value=f"R$ {current_value:,.2f}" if "Variação" not in col_name else f"{current_value:+.2f}%",
                    delta=f"{delta:+.4f} ({delta_percent:+.2f}%)"
                )

                if state in estados_coords:
                    coords = estados_coords[state]
                    lat, lon = coords
                    map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
                    st.map(map_df, zoom=4, use_container_width=True, height=263, width=300)
                else:
                    st.info("Localização não disponível para este estado.")

            with col2:
                st.markdown("---")
                fig, ax = plt.subplots(figsize=(13, 4))

                fig.patch.set_facecolor("#1e1e1e")
                ax.set_facecolor("#1e1e1e")

                ax.grid(color="#444444", linestyle="--", linewidth=0.7)
                ax.plot(x, y, color="#444444", linewidth=1.5, linestyle='--', zorder=1)
                ax.plot(x, y, marker="o", color="#29b5e8", linewidth=2, linestyle='-', zorder=2)

                for i, val in enumerate(y):
                    ax.text(x[i], val, f"R${val:.2f}", color="white", fontsize=10, ha="center", va="bottom")

                ax.set_title(f"{product} - {col_name}", fontsize=12, fontweight="bold", color="white", pad=10)
                ax.set_xlabel("Mês", color="white")
                ax.set_ylabel("Preço (R$)", color="white")
                ax.tick_params(colors="white")

                for spine in ax.spines.values():
                    spine.set_color("white")

                st.pyplot(fig)
        else:
            st.warning(f"⚠️ {state} - {product}: Dados insuficientes ou ausentes para **{col_name}**.")

    st.subheader("📄 Dados Filtrados")
    st.dataframe(df_filtered, use_container_width=True)

    if st.button("💾 Enviar dados para o banco"):
        try:
            df_filtered.to_sql("data_table", engine, if_exists="append", index=False)
            st.success("✅ Dados enviados com sucesso para o banco de dados.")
        except Exception as error:
            st.error(f"❌ Erro ao enviar dados: {error}")

else:
    st.info("📂 Faça o upload de um arquivo CSV ou XLSX para visualizar os gráficos.")
