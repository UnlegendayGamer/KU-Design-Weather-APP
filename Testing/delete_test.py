# from fastapi import FastAPI, HTTPException 
# import pandas as pd

# @app.delete("/delete_weather/")
# async def delete_weather(date):                

# #check if the date is present in the dataframe        
#     df = pd.read_csv("weatherdata.csv")
#     date_is_present = df.isin([date])

#     if not date_is_present:
#         raise HTTPException(status_code=500, detail=f"Failed to retrieve date: {date}") 
        
# #delete the specific column if the date is found
#     df.drop(date, axis=1)       
#     return {"message": f"Weather data for {date} deleted successfully"}


# @app.post()