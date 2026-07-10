#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[2]:


df = pd.read_csv(
    "fremont_bridge_cleaned.csv"
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


st.subheader("Hourly traffic pattern: Weekday vs Weekend")

metric = st.selectbox(
    "Choose metric to plot:",
    ["Total", "West", "East"],
    index=0
)

hourly_pattern = (
    df.groupby(["hour", "is_weekend"])[metric]
      .mean()
      .reset_index()
)

fig_hourly = px.line(
    hourly_pattern,
    x="hour",
    y=metric,
    color="is_weekend",
    labels={
        "hour": "Hour of day",
        metric: f"Average {metric} bikes per hour",
        "is_weekend": "Is weekend?"
    },
    title=f"Hourly traffic pattern ({metric}): weekday vs weekend"
)

st.plotly_chart(fig_hourly, use_container_width=True)

# ---------- 4. Daily totals over time ----------

st.subheader("Daily total bike counts over time")

daily = (
    df.groupby("date_only")["Total"]
      .sum()
      .reset_index()
)

fig_daily = px.line(
    daily,
    x="date_only",
    y="Total",
    labels={
        "date_only": "Date",
        "Total": "Total bikes per day"
    },
    title="Daily total bike counts on Fremont Bridge"
)

st.plotly_chart(fig_daily, use_container_width=True)

# ---------- 5. Average traffic by day of week ----------

st.subheader("Average daily traffic by day of week")

dow_avg = (
    df.groupby("day_of_week")["Total"]
      .mean()
      .reset_index()
)

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_avg["day_of_week"] = pd.Categorical(dow_avg["day_of_week"], categories=order, ordered=True)
dow_avg = dow_avg.sort_values("day_of_week")

fig_dow = px.bar(
    dow_avg,
    x="day_of_week",
    y="Total",
    labels={
        "day_of_week": "Day of week",
        "Total": "Average bikes per day"
    },
    title="Average daily bike counts by day of week"
)

st.plotly_chart(fig_dow, use_container_width=True)


st.subheader("Busiest hourly times on the bridge")

# Average bikes per hour, split by weekday vs weekend
busy_hours = (
    df.groupby(["hour", "is_weekend"])["Total"]
      .mean()
      .reset_index()
)

# Sort descending by average Total and take top 5 rows
busy_top5 = busy_hours.sort_values("Total", ascending=False).head(5)

st.write("Top 5 busiest hour/weekend combinations (by average bikes per hour):")
st.dataframe(busy_top5)
