import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import data_service

with st.expander("Beschreibung Ermittlung der Flexibilitäten und Darstellung als Flexmatrix", expanded=False):
    st.write("Abbildung 1 zeigt die in einem Realfall durch den Depot-Optimizer ermittelten Ladebedarfe der E-trucks jedes Depots. Daran lässt sich ablesen, dass Fahrzeug A von 01:00 Uhr - 10:00 Uhr am gegebenen Tag an der Ladestation steht und von 02:00 Uhr bis 09:00 Uhr das Laden mit einer Leistung von 10kW geplant hat. Fahrzeug B steht von 10:00 Uhr bis 11:00 Uhr und plant auch über diesen Zeitraum zu laden.") 
    st.write("Auf Basis dieser Ladekurven werden anschließend die Flexibilitäten (Abblidung 2) ermittelt. Dabei handelt es sich um alle möglichen Verschiebungen der Ladeleistung während die Fahrzeuge an der Ladesäule stehen. Jedes Fahrzeug soll trotz Anpassung der Ladekurve denselben End-Ladezustand wie ursprünglich geplant erreichen..")
flex_data = data_service.get_flex_message_json()

vehicle_data = data_service.get_vehicle_schedule_json()

entries = flex_data["payload"]["flexmatrix"]

hours = []

flex_data = data_service.get_flex_message_json()


vehicle_data = data_service.get_vehicle_schedule_json()

def build_row_vehicles(vehicle_entries):
    row = {}
    for entry in vehicle_entries:
        time = datetime.fromisoformat(entry["time"]).strftime("%H:%M")
        row[time] = entry["value"]
    return row


row1= build_row_vehicles(vehicle_data["vehicle-1"])
row2= build_row_vehicles(vehicle_data["vehicle-2"])

data_frame_vehicles = pd.DataFrame([row1, row2], index=["Fahrzeug A", "Fahrzeug B"])

data_frame_vehicles = data_frame_vehicles.reindex(sorted(data_frame_vehicles.columns), axis=1)

styled_data_frame_vehicles = data_frame_vehicles.style.format("{:.0f} kW", na_rep="x")

st.text("Abbildung 1: Ladeplan durch den Depot-Optimizer:")
st.text("Ladelimit an der Station: 20kW")
st.table(styled_data_frame_vehicles)


for entry in entries:
    increaseTimeEntry = datetime.fromisoformat(entry["increaseTime"]["deliveryStart"])
    decreaseTimeEntry = datetime.fromisoformat(entry["decreaseTime"]["deliveryStart"])
    if entry["quantity"]["value"] > 0:
        hours.append(increaseTimeEntry.hour)
        hours.append(decreaseTimeEntry.hour)

min_hour = min(hours)
max_hour = max(hours) + 1

matrix = np.zeros((max_hour, max_hour))



vehicle_naming_matrix = np.full((max_hour, max_hour),"", dtype=object)

for entry in entries:
    increaseTimeEntry = datetime.fromisoformat(entry["increaseTime"]["deliveryStart"])
    decreaseTimeEntry = datetime.fromisoformat(entry["decreaseTime"]["deliveryStart"])
    kW = entry["quantity"]["value"]

    matrix[increaseTimeEntry.hour, decreaseTimeEntry.hour] = kW

    if datetime.fromisoformat(entry["increaseTime"]["deliveryStart"]).hour < 10:
        vehicle_naming_matrix[increaseTimeEntry.hour, decreaseTimeEntry.hour] = "A"
    else:
        vehicle_naming_matrix[increaseTimeEntry.hour, decreaseTimeEntry.hour] = "B"
    
matrix = matrix[min_hour:, min_hour:]   
vehicle_naming_matrix = vehicle_naming_matrix[min_hour:, min_hour:]   
size = matrix.shape[0]

times = [f"{h:02d}:00" for h in range(size)]

dataFrame = pd.DataFrame(
    matrix,
    index=times,
    columns=times
)

dataFrame.index.name = "Leistung [kW]"


styled_dataFrame = dataFrame.style.format("{:.0f}")

cell_text = np.where(
    matrix > 0,
    matrix.astype(int).astype(str) + "<br>" + vehicle_naming_matrix,
    ""
)

flex_matrix_heatmap = px.imshow(
    dataFrame,
    labels=dict(x="Entladen", y="Laden", color="Leistung [kW]"),
    aspect="auto",
    color_continuous_scale="Blues"
)

flex_matrix_heatmap.update_traces(text=cell_text, texttemplate="%{text}")

flex_matrix_heatmap.update_layout(
    xaxis_title="Entladen (Zeit)",
    yaxis_title="Laden (Zeit)",
    height=600,
)
st.text("Abbildung 1: Darstellung der Flex-Optionen als Heatmap-Flexmatrix:")
st.plotly_chart(flex_matrix_heatmap)
with st.expander("Erklärung Flexmatrix", expanded=False):
    st.write("test")