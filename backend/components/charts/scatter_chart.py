# chatbot-llm/backend/components/charts/scatter_chart.py
from typing import Dict, List, Union

from streamlit_echarts import st_echarts
from components.theme import get_theme_styles
from config.dicionarios import METRICAS_VALIDAS


def render_scatter_chart(
    data: Dict[str, Union[List[str], Dict[str, List[float]]]],
) -> None:
    theme = get_theme_styles()
    key_x, key_y = data["metricas"]
    label_x = METRICAS_VALIDAS.get(key_x, key_x.replace("_", " ").title())
    label_y = METRICAS_VALIDAS.get(key_y, key_y.replace("_", " ").title())

    points = []
    for idx, city in enumerate(data["cidades"]):
        valores = data.get("valores", {})
        if isinstance(valores, dict):
            vals = valores.get(city, [0, 0])
        else:
            vals = [0, 0]
        points.append(
            {
                "name": city,
                "value": vals,
                "symbolSize": 20,
                "itemStyle": {
                    "color": (
                        theme["CHART_PRIMARY_COLOR"]
                        if idx == 0
                        else theme["CHART_SECONDARY_COLOR"]
                    )
                },
            }
        )

    options = {
        "title": {
            "text": f"{label_x} × {label_y}",
            "textStyle": theme["CHART_TEXT_STYLE"],
        },
        "tooltip": {"trigger": "item", **theme["CHART_TOOLTIP_STYLE"]},
        "xAxis": {
            "type": "value",
            "name": label_x,
            "nameTextStyle": theme["CHART_AXIS_LABEL_STYLE"],
        },
        "yAxis": {
            "type": "value",
            "name": label_y,
            "nameTextStyle": theme["CHART_AXIS_LABEL_STYLE"],
        },
        "series": [{"type": "scatter", "data": points}],
    }
    st_echarts(options=options, height="400px")
