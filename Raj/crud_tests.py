# from fastapi import FastAPI, HTTPException 
# import pandas as pd

# def check_presence(value, value_checked):
#     value_is_present = df.isin([value])

#     if not data_type_is_present:
#         raise HTTPException(status_code=500, detail=f"Failed to retrieve {value_checked}: {value}")
    
#     return True
    
# @app.delete("/delete_weather/")
# async def delete_weather(date):                

# #check if the date is present in the dataframe        
#     df = pd.read_csv("weatherdata.csv")
#     date_is_present = df.isin([date])


#     check_presence(date, "date")
        
# #delete the specific column if the date is found
#     df.drop(date, axis=1)       
#     return {"message": f"Weather data for {date} deleted successfully"}


# @app.put("/put_weather/")
# async def put_weather(date, data_type, data_value):
#     with open("weatherdata.txt", 'r') as file:
#         lines = file.readlines()