# chatbot-llm/backend/components/charts/chart_builder.py
from typing import Any, Dict
from .bar_chart import render_bar_chart
from .radar_chart import render_radar_chart
from .scatter_chart import render_scatter_chart
from .gauge_chart import render_gauge_chart
from .other_chart import render_other_chart

ChartData = Dict[str, Any]


def infer_chart_type(data: ChartData) -> str:
    metricas = data.get("metricas", [])
    cidades = data.get("cidades", [])
    n_met = len(metricas)
    n_cid = len(cidades)

    if n_met == 1 and n_cid > 1:
        return "bar"
    if n_met > 1 and n_cid > 1:
        return "radar"
    if n_met == 2:
        return "scatter"
    if n_met == 1 and n_cid == 1:
        return "gauge"
    return "other"


def render_chart(data: ChartData) -> None:
    chart_type = infer_chart_type(data)

    if chart_type == "bar":
        render_bar_chart(data)
    elif chart_type == "radar":
        render_radar_chart(data)
    elif chart_type == "scatter":
        render_scatter_chart(data)
    elif chart_type == "gauge":
        render_gauge_chart(data)
    else:
        render_other_chart(data)
