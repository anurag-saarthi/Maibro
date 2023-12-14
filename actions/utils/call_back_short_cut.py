import datetime
from datetime import timedelta
threshold_days = "7"
threshold_time = "18:00"
min_threshold_time = "7:59"

def given_date_function(value):
    today = datetime.date.today()
    if "due_date" in value:
        value = value.split("due_date")[1]
        if value=="":
            given_date = today
        elif "+" in value:
            value = value.split("+")[1]
            given_date = today + timedelta(days=int(value))
        else: #elif "-" in value:
            value  = value.split("-")[1]
            given_date = today - timedelta(days=int(value))
    else:
        given_date = datetime.datetime.strptime(value, "%d/%m/%Y").date()
        if given_date.year==2024:
            given_date = given_date - timedelta(days=365)
    return given_date

def date_value(given_date):
    today = datetime.date.today()
    no_of_days = given_date - today
    date = ""
    if no_of_days.days < int(threshold_days):
        date = "true"
        if no_of_days.days<0:
            date="previous"
        elif int(no_of_days.days) == 0:
            date = "today"
    else:
        date = "false"
    return date

def get_time(given_time):
    given_time = given_time.split(":")[0]
    if 1<=int(given_time)<=6:
        given_time = 12 + int(given_time)
    threshold_time_1 = threshold_time.split(":")[0]
    if int(given_time)>12:
        dispatcher_time = int(given_time) - 12 
    return given_time,threshold_time_1,dispatcher_time




entities =  [
            {
                "entity": "date",
                "extractor": "saarthi-ner",
                "value": "14/02/2023"
            },
            {
                "entity": "time",
                "extractor": "saarthi-ner",
                "value": "19:00"
            }
        ]


given_date = ""
date_value = ""
given_time = ""
if entities:
    for entity in entities:
        if entity["entity"] == "date":
            given_date=given_date_function(entity["value"])
            date_value = date_value(given_date)
            print(given_date,date_value)
        elif entity["entity"] == "time":
            given_time = get_time(entity["value"])
            print(given_time)

    if given_time:
        if min_threshold_time<=given_time<= threshold_time:  
            if date_value == "today":
                print("it's todays date")
            elif date_value == "true":
                print("the date is valid")
            elif date_value = "previous":
                print("the date is previous")
            else:
                print("unacceptable")
        else:
            print("unaccpetiable time")
    elif date_value:
        if date_value == "today":
                print("it's todays date")
        elif date_value == "true":
            print("the date is valid")
        elif date_value = "previous":
            print("the date is previous")
        else:
            print("unacceptable")
        
else:
    print("no date and no time")



