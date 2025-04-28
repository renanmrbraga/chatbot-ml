# backend/components/theme.py
from typing import Any, Dict


def get_theme_styles() -> Dict[str, Any]:
    """
    Retorna um dicionário único de estilos: fundo do chatbot azul-marinho, fundo dos gráficos branco.
    """
    # Cores principais
    primary_color = "#1e90ff"  # Azul forte (destaque)
    secondary_color = "#00c853"  # Verde neon (contraste forte)
    foreground = "#ffffff"  # Texto branco (no chatbot)
    background = "#0b0c1a"  # Azul marinho escuro (fundo do app)
    card_bg = "#15162a"  # Fundo dos cards

    # Gradientes e fundos para gráficos
    bar_gradient = {
        "type": "linear",
        "x": 0,
        "y": 0,
        "x2": 1,
        "y2": 0,
        "colorStops": [
            {"offset": 0, "color": "rgba(30,144,255,0.9)"},
            {"offset": 1, "color": "rgba(0,200,83,0.5)"},
        ],
    }
    area_gradient = {
        "type": "linear",
        "x": 0,
        "y": 0,
        "x2": 0,
        "y2": 1,
        "colorStops": [
            {"offset": 0, "color": "rgba(30,144,255,0.3)"},
            {"offset": 1, "color": "rgba(0,200,83,0.1)"},
        ],
    }

    return {
        # Modo
        "mode": "dark",
        # Cores básicas
        "PRIMARY_BLUE": primary_color,
        "HIGHLIGHT_COLOR": secondary_color,
        "FOREGROUND_COLOR": foreground,
        "BACKGROUND_COLOR": background,
        "CARD_BACKGROUND": card_bg,
        "RADIO_COLOR": secondary_color,
        "TOOLTIP_BG": card_bg,
        "TOOLTIP_TEXT": foreground,
        # Gradientes para gráficos
        "GRADIENT_HORIZONTAL_ECHARTS": bar_gradient,
        "GRADIENT_VERTICAL_ECHARTS": area_gradient,
        # Estilos de cards
        "CARD_STYLE": (
            f"background-color: {card_bg};"
            "padding: 1.2rem;"
            "border-radius: 1rem;"
            f"box-shadow: 0 0 15px {secondary_color}55;"
            "text-align: center;"
            "min-width: 180px;"
            "transition: all 0.3s ease;"
        ),
        "CARD_TITLE_STYLE": (
            f"color: {foreground};"
            "margin-bottom: 0.5rem;"
            "font-size: 1.05rem;"
            "font-weight: 500;"
        ),
        "CARD_VALUE_STYLE": (
            f"color: {secondary_color};"
            "margin: 0;"
            "font-size: 1.6rem;"
            "font-weight: bold;"
        ),
        # Estilos para gráficos
        "CHART_TEXT_STYLE": {
            "color": "#000000",
            "fontWeight": "bold",
            "fontSize": 14,
        },  # Texto preto no gráfico
        "CHART_AXIS_LABEL_STYLE": {"color": "#333333"},
        "CHART_AXIS_LINE_STYLE": {"lineStyle": {"color": "#cccccc"}},
        "CHART_GRIDLINE_COLOR": "#dddddd",
        "CHART_TOOLTIP_STYLE": {
            "backgroundColor": "#ffffff",
            "borderColor": primary_color,
            "textStyle": {"color": "#000000"},
        },
        "CHART_PRIMARY_COLOR": primary_color,
        "CHART_SECONDARY_COLOR": secondary_color,
        "CHART_AREA_GRADIENT": area_gradient,
        "BAR_GRADIENT": bar_gradient,
        "CHART_RADAR_BG": [
            "#ffffff",
            "#f5f5f5",
            "transparent",
        ],  # Fundo do radar branco
    }
