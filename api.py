from fastapi import FastAPI, Request, Depends
import requests
import pandas as pd
from datetime import datetime, time, timedelta
import time
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from main import stop, main


templates = Jinja2Templates(directory=".")

app = FastAPI()


list_of_titles = ["Linje", "Mot", "Läge", "Planerad Avgång", "Avgång", "Avgår Om"]


@app.get("/")
def get(request: Request):
    my_list, curr_time = main()
    year = curr_time[0]
    month = curr_time[1]
    month_name = curr_time[2]
    week = curr_time[3]
    day_no = curr_time[4]
    day_name = curr_time[5]
    hour = curr_time[6]
    minute = curr_time[7]
    return templates.TemplateResponse("index.html", {"request": request, "my_list": my_list, "titles_list": list_of_titles, "departure_stop": stop, "now": curr_time, "year": year, "month": month, "month_name": month_name, 
                                                    "day_no": day_no, "day_name": day_name, "hour": hour, "minute": minute})
