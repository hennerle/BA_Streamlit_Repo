import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

def get_vehicle_schedule_json():
    return json.load(open("vehicle_schedule.json"))

def get_flex_message_json():
    return json.load(open("flex_message.json"))

def create_matrix_from_json():
    entries = get_flex_message_json()["payload"]["flexmatrix"]
    hours = []

    for entry in entries:
        increaseTimeEntry = datetime.fromisoformat(entry["increaseTime"]["deliveryStart"])
        decreaseTimeEntry = datetime.fromisoformat(entry["decreaseTime"]["deliveryStart"])

        hours.append(increaseTimeEntry.hour)
        hours.append(decreaseTimeEntry.hour)

    max_hour = max(hours) + 1

    matrix = np.zeros((max_hour, max_hour))

    for entry in entries:
        increaseTimeEntry = datetime.fromisoformat(entry["increaseTime"]["deliveryStart"])
        decreaseTimeEntry = datetime.fromisoformat(entry["decreaseTime"]["deliveryStart"])
        kW = entry["quantity"]["value"]

        matrix[increaseTimeEntry.hour, decreaseTimeEntry.hour] = kW
    
    return matrix
    
