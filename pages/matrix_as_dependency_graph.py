import streamlit as st
import numpy as np
import data_service
from datetime import datetime
import pandas as pd

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

data_frame_vehicles = pd.DataFrame([row1, row2], index=["Vehicle 1", "Vehicle 2"])

data_frame_vehicles = data_frame_vehicles.reindex(sorted(data_frame_vehicles.columns), axis=1)

styled_data_frame_vehicles = data_frame_vehicles.style.format("{:.0f} kW", na_rep="x")

st.text("Planned vehicle schedule:")
st.table(styled_data_frame_vehicles)

matrix = data_service.create_matrix_from_json()

for zeile_idx, zeile in enumerate(matrix):
    if np.sum(zeile) > 0:
        st.subheader(f"Flexibilitäten Stunde {zeile_idx}")
        
        graph = "digraph {\n"
        graph += "    rankdir=TB;\n"  
        graph += "    node [shape=box, style=filled, fillcolor=lightblue];\n"
        
        for spalte_idx, wert in enumerate(zeile):
            if wert > 0:
                graph += f'    {zeile_idx} [label="Stunde {zeile_idx}\\n+{int(wert)} kW"];\n'
                graph += f'    {spalte_idx} [label="Stunde {spalte_idx}\\n-{int(wert)} kW"];\n'
                graph += f'    {zeile_idx} -> {spalte_idx} [dir=both];\n'
        
        graph += "}"
        
        st.graphviz_chart(graph)
