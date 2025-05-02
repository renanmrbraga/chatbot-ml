# chatbot-llm/backend/components/charts/gauge_chart.py
from typing import Any, Dict, List, Union

from streamlit_echarts import st_echarts
from components.theme import get_theme_styles
from config.dicionarios import METRICAS_VALIDAS


def render_gauge_chart(
    data: Dict[str, Any],
) -> None:
    cidades = data["cidades"] if isinstance(data.get("cidades"), list) else []
    metricas = data["metricas"] if isinstance(data.get("metricas"), list) else []
    valores = data["valores"] if isinstance(data.get("valores"), dict) else {}

    if not cidades or not metricas:
        return

    theme = get_theme_styles()
    city = cidades[0]
    key = metricas[0]
    label = METRICAS_VALIDAS.get(key, key.replace("_", " ").title())

    if not isinstance(valores, dict) or city not in valores:
        val = 0
    else:
        val = valores.get(city, [0])[0]

    scale_max = data["max"] if isinstance(data.get("max"), (int, float)) else val * 1.2

    options = {
        "title": {"text": f"{label} — {city}", "textStyle": theme["CHART_TEXT_STYLE"]},
        "tooltip": {"trigger": "item", **theme["CHART_TOOLTIP_STYLE"]},
        "series": [
            {
                "type": "gauge",
                "min": 0,
                "max": scale_max,
                "detail": {
                    "formatter": "{value}",
                    "textStyle": theme["CHART_TEXT_STYLE"],
                },
                "data": [{"value": val, "name": label}],
            }
        ],
    }
    st_echarts(options=options, height="300px")
