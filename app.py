import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="centered")

st.header("On the left side are the options for visualizing the data", divider="gray")
st.markdown("The flexmatrix shows all flexibility options given the schedule provided by the depots.")
