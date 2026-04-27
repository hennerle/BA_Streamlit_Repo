import streamlit as st
import numpy as np
import plotly.graph_objects as go
import data_service

matrix_data = data_service.create_matrix_from_json()


hours = list(range(12))
power = [0] * 12

power[1] = 20

for h in range(2, 10):
    power[h] = -20

fig = go.Figure(go.Bar(
    x=hours,
    y=power,
    marker_color=['green' if p > 0 else ('red' if p < 0 else 'gray') for p in power],
    text=[f'{p:+d}' if p != 0 else '' for p in power],
    textposition='auto'
))

fig.update_layout(
    title="Flexibilitätsprofil: Laden vs. Entladen",
    xaxis_title="Stunde",
    yaxis_title="Leistung (kW)",
    yaxis=dict(range=[-20, 20], tick0=-20, dtick=5),
    xaxis=dict(tick0=0, dtick=1),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)