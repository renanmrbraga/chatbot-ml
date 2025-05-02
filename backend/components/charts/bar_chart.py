# chatbot-llm/backend/components/charts/bar_chart.py
from typing import Any, Dict

from streamlit_echarts import st_echarts
from components.theme import get_theme_styles
from config.dicionarios import METRICAS_VALIDAS


def render_bar_chart(data: Dict[str, Any]) -> None:
    theme = get_theme_styles()
    key = data["metricas"][0]
    label = METRICAS_VALIDAS.get(key, key.replace("_", " ").title())
    cities = data["cidades"]
    values = [data["valores"].get(c, [0])[0] for c in cities]

    options = {
        "title": {
            "text": f"{label} por cidade",
            "textStyle": theme["CHART_TEXT_STYLE"],
        },
        "tooltip": {"trigger": "axis", **theme["CHART_TOOLTIP_STYLE"]},
        "legend": {
            "data": [label],
            "textStyle": theme["CHART_TEXT_STYLE"],
            "bottom": 10,
        },
        "xAxis": {
            "type": "category",
            "data": cities,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
        },
        "yAxis": {
            "type": "value",
            "name": label,
            "axisLabel": theme["CHART_AXIS_LABEL_STYLE"],
        },
        "series": [
            {
                "name": label,
                "type": "bar",
                "data": values,
                "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
                "emphasis": {"itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]}},
            }
        ],
    }
    st_echarts(options=options, height="400px")
