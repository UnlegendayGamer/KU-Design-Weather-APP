import streamlit as st
import pandas as pd

dataframe = None
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    new_file = uploaded_file.getvalue().decode("utf-8")
    # st.write(new_file)
    temp_val = new_file.replace(": ", ",").replace(" ", ",")
    
    f = open("weatherdata.csv", "w")
    f.write(temp_val)
    f.close()
    
    with open("weatherdata.csv", "r") as r, open("weatherdata2.csv", "w") as w:
        for line in r:
            if line.strip():
                w.write(line)
    
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv("weatherdata2.csv")
    print(dataframe)
    st.dataframe(dataframe)
    
    flipped_df = dataframe.T
    flipped_df.columns = flipped_df.iloc[0]
    flipped_df = flipped_df.iloc[1:]
    flipped_df = flipped_df.reset_index()
    st.dataframe(flipped_df)

    option = st.selectbox(
        "What data would you like to compare",
        ("weather_code", "temperature_max", "temperature_min", "precipitation_sum", "wind_speed_max", "precipitation_probability_max"),
    )

    st.bar_chart(data=flipped_df, x="index", y=option, color="#40242c", stack=False)