import pandas as pd
import plotly.express as px
import streamlit as st

file = ".venv/The Beatles songs dataset 285x45 v0.csv"
dt = pd.read_csv(file)

#Usless columns
columns_remove = [
    'URI', 'Time_signature', 'Energy', 'Loudness', 'Instrumentalness',
    'Speechiness', 'Tempo', 'Other releases', 'Single A side',
    'Single B side', 'Single certification', 'Styles', 'Themes',
    'Moods', 'Songwriter(s)', 'Lead vocal(s)', 'Cover', 'Covered by',
    'Chart position UK (Wikipedia)', 'Chart position US (Wikipedia)',
    'Highest position (The Guardian)', 'Weeks on chart in UK (The Guardian)',
    'Weeks at No1 in UK (The Guardian)', 'Highest position (Billboard)',
    'Weeks at No1 (Billboard)', 'Top 50 (Billboard)',
    'Top 50 (Ultimate classic rock)', 'Top 50 (NME)',
    'Top 50 (Top50songs.org)', 'Album', 'Genre',
    'Top 50 (USA today, 2017)', 'Album debut',
    'Top 50 (Vulture, by Bill Wyman)'
]
dt = dt.drop(columns=columns_remove, errors="ignore")


dt['Year'] = pd.to_numeric(dt['Year'], errors='coerce')
dt = dt.dropna(subset=['Year'])
dt['Top 50 (Rolling Stone)'] = pd.to_numeric(dt['Top 50 (Rolling Stone)'], errors='coerce').fillna(0)


# Here I sort whole dataset by year
dt = dt.sort_values(by="Year", ascending=False)


# Code with output
st.title("The Beatles' songs (Analysis by Davlet Bairamkulov)")

# Basic analyse
st.subheader("Basic information")
st.dataframe(dt)
st.write('''I have sorted dataset by year, deleted some columns that do not suit for my purposes,
 replaced NaNs in column Top 50 (Rolling Stones) with 0 
 and deleted songs without realise date (there was only 8, so it did not influence the data).''')
st.write(f"Strings: {len(dt)}")
st.write("Here is some basic data about the dataset:")
st.dataframe(dt.describe())


# 1 Chart
# This barchart shows popularity of the songs through the years
dt_sort1 = dt.sort_values(by="Popularity", ascending=True)

st.subheader("Popularity of the songs through the years")
fig1 = px.bar(
    dt_sort1,
    x="Title",
    y="Popularity",
    labels={"Title": "Name", "Popularity": "Popularity"}
)
st.plotly_chart(fig1)
st.write("Using this graph we can easily find out the most and the least popular song.")

# 2 Chart
# This pie chart shows us the ratio of major and minor songs
st.subheader("The ratio of major and minor songs")
mode_all = dt["Mode"].value_counts()
fig2 = px.pie(
    values=mode_all.values,
    names=["Major", "Minor"],
)
st.plotly_chart(fig2)
st.write("From this diogram we can easily mention that The Beatles prefer major to minor mode.")

# 3 Chart
# Bar chart that shows songs' duration
dt_sort2 = dt.sort_values(by='Duration', ascending=True)
st.subheader("Songs' duration")
fig3 = px.bar(
    dt_sort2,
    x="Title",
    y="Duration",
    labels={"Title": "Name", "Duration": "Duration"}
)
st.plotly_chart(fig3)
st.write("This graph can help us to define the shortest and the longest song")

# 4 Chart
# Rolling Stone Top 50
st.subheader("Songs Rolling Stone Top 50")
top_all = dt["Top 50 (Rolling Stone)"].value_counts()
fig4 = px.pie(
    values=top_all.values,
    names=[pos if pos != 0 else "Out of the top" for pos in top_all.index]
)
st.plotly_chart(fig4)
st.write("On this piechart we can see how many songs got into the chart and what places they get.")

# 5 Chart
# Key of the songs
st.subheader("The Beatles' most favorite keys")
key_all = dt["Key"].value_counts()
fig6 = px.pie(
    values=key_all.values,
    names=key_all.index
)
st.plotly_chart(fig6)
st.write("On this diogram one can see what was the most popular key in Beatles' songs")

# 6 Chart
# Bubble chart, not very comfortable for using, but interesting and beautiful
st.subheader("Popularity, Duration, Mode and Valence of the songs")
fig6 = px.scatter(
    dt,
    x="Duration",
    y="Popularity",
    size="Valence",
    color="Mode",
    hover_name="Title",
    labels={"Duration": "Duration", "Popularity": "Popularity", "Valence": "Valence"}
)
st.plotly_chart(fig6)
st.write('''The graph shows how the popularity of songs depends on their duration mod and valece. 
Size of the bubbles shows valence, colour shows mod (blue - minor,white - major).''')

# 7 chart
# 3D scatter just like buble but in 3D
st.subheader("Danceability, acousticness, mod, duration and popularity")
fig7 = px.scatter_3d(
    dt,
    x="Danceability",
    y="Acousticness",
    z="Popularity",
    color="Key",
    size="Duration",
    hover_name="Title",
    labels={"Danceability": "Danceability", "Acousticness": "Acousticness", "Popularity": "Popularity"}
)
st.plotly_chart(fig7)
st.write('''The graph shows how the acoustics and dance quality of the songs are related to their popularity. 
The color of the dots indicates the key, and the size indicates the duration of the song.''')

#8 chart
# Sunburst chart, this one show dependence of key on mod

st.subheader("The distribution of songs by mod, key and popularity")
dt["Mode+"] = dt["Mode"].replace({0: "Minor", 1: "Major"})
fig_sunburst = px.sunburst(
    dt,
    path=["Mode+", "Key"],
    values="Popularity",
    color="Popularity",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_sunburst)
st.write("The graph shows the distribution of songs by major and minor, by key, and their popularity(colour).")

# Hypothesis

st.subheader('''Hypothesis: Major songs with high danceability are more popular than major ones with low, and minor songs with high acoustics are more popular than minor ones with low.''')

major_songs = dt[dt["Mode"] == 1]
minor_songs = dt[dt["Mode"] == 0]

# Here I find median to understand what is high and what is low acousticness and danceability
danceability_median = dt["Danceability"].median()
acousticness_median = dt["Acousticness"].median()

# Major
major_songs_high_dance = major_songs[major_songs["Danceability"] > danceability_median]
major_songs_low_dance = major_songs[major_songs["Danceability"] <= acousticness_median]

major_songs_high_dance_popularity = major_songs_high_dance["Popularity"].mean()
major_songs_low_dance_popularity = major_songs_low_dance["Popularity"].mean()

st.write("**Information from the graph:**")
st.write(f"Popularity of major songs with high danceability: {major_songs_high_dance_popularity:.2f}")
st.write(f"Popularity of major songs with low danceability: {major_songs_low_dance_popularity:.2f}")

# Minor
minor_songs_high_acoustic = minor_songs[minor_songs["Acousticness"] > acousticness_median]
minor_songs_low_acoustic = minor_songs[minor_songs["Acousticness"] <= acousticness_median]

minor_songs_high_acoustic_popularity = minor_songs_high_acoustic["Popularity"].mean()
minor_songs_low_acoustic_popularity = minor_songs_low_acoustic["Popularity"].mean()

st.write(f"Popularity of minor songs with high acousticness: {minor_songs_high_acoustic_popularity:.2f}")
st.write(f"Popularity of minor songs with low acousticness: {minor_songs_low_acoustic_popularity:.2f}")

# 9 chart hypothesis
fig9 = px.bar(
    x=["Major (high dance.)", "Major (low dance.)",
       "Minor (high acoustic.)", "Minor (low acoustic.)"],
    y=[major_songs_high_dance_popularity, major_songs_low_dance_popularity,
       minor_songs_high_acoustic_popularity, minor_songs_low_acoustic_popularity],
    labels={"y": "Popularity", "x": ""}
)
st.plotly_chart(fig9)

st.write("From the graph we can see that our hypothesis is wrong. In fact, it turned out to be the opposite, major songs with low danceability are more popular than with high, the same is for minor songs and acousticness.")


# New columns
st.subheader("New columns")

# Valence + Danceability
dt["Energy Index"] = dt["Valence"] + dt["Danceability"]

# Complexity
# This one will show complexity of the songs from musical point of view
# Songs with keys farther from the 6 are more complex.
# Minor songs more complex.
# Longer songs are more complex.
# High acousticness is more complex.

dt["Complexity"] = (
    0.3 * abs(dt["Key"] - 6) +
    0.4 * (1 - dt["Mode"]) +
    0.2 * dt["Duration"] +
    0.1 * dt["Acousticness"]
)
# Parameters as 0.3 0.4 ... I put by random

st.dataframe(dt[["Title", "Energy Index", "Complexity"]])

st.write(""" I have added 2 new columns Energy index and Complexity. The first one shows us how energetic sing is, it 
uses 2 other columns: Valence and Danceability.
The second column is harder, it shows complexity of the songs from musical point of view, using columns: Key, Mode, 
Duration, Acousticness (each of them has its own effect coefficient(0.3; 0.4; 0.2; 0.1 accordingly)).
""")

st.subheader("That is the end of my analysis. Davlet and the Beatles were with you, best wishes X")
