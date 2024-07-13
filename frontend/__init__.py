from plotly.graph_objects import Figure
import streamlit.components.v1 as components

_component_func = components.declare_component("telegram_web_app", path="./frontend")

def telegram_web_app(user_data=None):
    component_value = _component_func(user_data=user_data, default=None)
    return component_value