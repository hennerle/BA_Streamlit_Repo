import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime

st.header("This is the flexmatrix displayed as a plain table", divider="gray")
st.markdown("The flexmatrix shows all flexibility options given the schedule provided by the depots.")

data = json.load(open("flex_message.json"))

df = pd.DataFrame(data)
st.dataframe(df)

st.text(data["messageId"])

entries = data["payload"]["flexmatrix"]

hours = []

for entry in entries:
    increaseTimeEntry = datetime.fromisoformat(entry["increaseTime"]["deliveryStart"])
    decreaseTimeEntry = datetime.fromisoformat(entry["decreaseTime"]["deliveryStart"])
    kW = entry["quantitity"]["value"]



    hours.append(increaseTimeEntry.hour)
    hours.append(decreaseTimeEntry.hour)

max_hour = max(hours)

matrix = np.zeros((max_hour, max_hour))

for entry in entries:
    increaseTimeEntry = datetime.fromisoformat(entry["increaseTime"]["deliveryStart"])
    decreaseTimeEntry = datetime.fromisoformat(entry["decreaseTime"]["deliveryStart"])
    kW = entry["quantity"]["value"]

    matrix[increaseTimeEntry, decreaseTimeEntry] = kW
    
st.write("Flexmatrixgröße: ", matrix.shape)
st.write(matrix)



