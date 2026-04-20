import streamlit as st
import json
import pandas as pd

st.header("This is the flexmatrix displayed as a plain table", divider="gray")
st.markdown("The flexmatrix shows all flexibility options given the schedule provided by the depots.")

data = json.load(open("flex_message.json"))

df = pd.DataFrame(data)
st.dataframe(df)


print(data.messageId)