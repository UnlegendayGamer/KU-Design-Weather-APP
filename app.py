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

<<<<<<< HEAD
    st.bar_chart(data=flipped_df, x="index", y=option, color="#40242c", stack=False)
    
    df = None
    
    latitude = st.number_input("Latitude")
    longitude = st.number_input("Longitude")
    
    df = request.get_info(latitude, longitude)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    st.dataframe(df)

    user_choice = st.selectbox(
        "What data would you like to compare?",
         ("weather code", "temperature 2m max", "temperature 2m min", "precipitation sum", "wind speed max", "precipitation probability max"), key="1"
    )

    choice = None
    
    if (user_choice == "weather code"):
        choice = "weather_code"
    elif (user_choice == "temperature 2m max"):
        choice = "temperature_2m_max"
    elif (user_choice == "temperature 2m min"):
        choice = "temperature_2m_min"
    elif (user_choice == "precipitation sum"):
        choice = "precipitation_sum"
    elif (user_choice == "wind speed max"):
        choice = "wind_speed_max"
    elif (user_choice == "precipitation probability max"):
        choice = "precipitation_probability_max"
    else:
        choice = "What the heck?"
    
    
    date_slider = st.select_slider(
        "Select a date range",
        options=df['date'],
        value=(df['date'].min(), df['date'].max())
    )
    
    # filter the data to the selected date range
    filtered_df = df[(df['date'] >= date_slider[0]) & (df['date'] <= date_slider[1])]

    st.bar_chart(filtered_df[['date', choice]].set_index('date'), color="#40242c")

    if (filtered_df[choice].max() > flipped_df[choice].max()):
        max_value = filtered_df[choice].max()
    else:
        max_value = flipped_df[choice].max()
    st.write("In the given data, the " + user_choice + " was " + str(flipped_df[user_choice].max()) + ", while the " + user_choice + " at latitude " + str(latitude) + " longitude " + str(longitude) + ", was " + str(max_value))
=======
    st.bar_chart(data=flipped_df, x="index", y=option, color="#40242c", stack=False)
>>>>>>> parent of dbf16e3 (completed chellenges 1 and 2)
