from fastapi import FastAPI,Response
import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from uvicorn import run
import logging
logging.basicConfig(level=logging.INFO,filename="logs/customer_details.log",filemode="w",format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read() 
    file_name = "uploadfile.csv"
    contents = json.loads(contents)
    df = pd.read_json(contents)
    df.to_csv(file_name)
    some_file_path = "/home/azureuser/Fullerton_bot/names.csv"
    return FileResponse(some_file_path)


if __name__ == "__main__":
    run("fastapi_python:app", host="0.0.0.0", port=8999,workers=1)