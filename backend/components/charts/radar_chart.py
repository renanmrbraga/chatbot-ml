# app/components/charts/radar_chart.py
from typing import Dict, List, Union

from streamlit_echarts import st_echarts
from components.theme import get_theme_styles
from config.dicionarios import METRICAS_VALIDAS


def render_radar_chart(
    data: Dict[str, Union[List[str], Dict[str, List[float]]]],
) -> None:
    """
    Espera ChartData:
    {
      "cidades": ["SP", "RJ"],
      "metricas": ["populacao_total", "pib_per_capita", ...],
      "valores": {
        "SP": [val1, val2, ...],
        "RJ": [val1, val2, ...]
      }
    }
    """
    theme = get_theme_styles()
    cidades: List[str] = data["cidades"]  # type: ignore
    metricas: List[str] = data["metricas"]  # type: ignore
    valores: Dict[str, List[float]] = data["valores"]  # type: ignore

    # Garantir que cada cidade tenha o mesmo número de métricas
    for cidade in cidades:
        if cidade not in valores or len(valores[cidade]) != len(metricas):
            valores[cidade] = [0] * len(metricas)

    # Construir indicadores com máximos relativos por métrica
    indicators = []
    for idx, met in enumerate(metricas):
        met_label = METRICAS_VALIDAS.get(met, met.replace("_", " ").title())
        max_val = max(valores[c][idx] for c in cidades if c in valores) * 1.2 or 1
        indicators.append({"name": met_label, "max": round(max_val, 2)})

    # Construir as séries de dados
    colors = [theme["CHART_PRIMARY_COLOR"], theme["CHART_SECONDARY_COLOR"]]
    series_data = []
    for i, cidade in enumerate(cidades):
        series_data.append(
            {
                "value": valores[cidade],
                "name": cidade,
                "itemStyle": {"color": colors[i % len(colors)]},
                "areaStyle": {"opacity": 0.3},
            }
        )

    options = {
        "title": {
            "text": "Comparativo entre Cidades",
            "textStyle": theme["CHART_TEXT_STYLE"],
        },
        "legend": {
            "data": cidades,
            "textStyle": theme["CHART_TEXT_STYLE"],
            "bottom": 10,
        },
        "tooltip": {"trigger": "item", **theme["CHART_TOOLTIP_STYLE"]},
        "radar": {
            "indicator": indicators,
            "name": {"textStyle": theme["CHART_AXIS_LABEL_STYLE"]},
            "splitLine": {"lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}},
        },
        "series": [{"type": "radar", "data": series_data}],
    }

    st_echarts(options=options, height="500px")
