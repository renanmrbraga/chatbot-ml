# app/components/charts/other_chart.py
import streamlit as st


def render_other_chart(data: dict[str, object]) -> None:
    st.warning("Tipo de gráfico não suportado pelo builder atual.")
    st.json(data)
