#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[2]:


df = pd.read_csv(
    r"C:\Users\acbre\OneDrive\Desktop\Freemont_Cleaned.csv"
)


# In[3]:


df["Date"] = pd.to_datetime(df["Date"])
df["hour"] = df["Date"].dt.hour
df["day_of_week"] = df["Date"].dt.day_name()
df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])


# In[4]:


st.title("Fremont Bridge Traffic: Weekday vs Weekend")

st.write(
    "This chart shows how bike traffic varies by hour, comparing weekdays "
    "and weekends for riders aged 18–35."
)


# In[5]:


hourly_pattern = (
    df.groupby(["hour", "is_weekend"])["Total"]
      .mean()
      .reset_index()
)


# In[6]:


fig = px.line(
    hourly_pattern,
    x="hour",
    y="Total",
    color="is_weekend",
    labels={
        "hour": "Hour of day",
        "Total": "Average bikes per hour",
        "is_weekend": "Is weekend?"
    },
    title="Hourly traffic pattern: Weekday vs Weekend"
)

st.plotly_chart(fig, use_container_width=True)


# In[ ]:




