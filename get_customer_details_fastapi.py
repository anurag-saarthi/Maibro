from fastapi import FastAPI,Request
from uvicorn import run
from handle_bulk_data import store_into_redis,fetch_data
import logging
logging.basicConfig(level=logging.INFO,filename="logs/customer_details.log",filemode="w",format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
app = FastAPI()


@app.get('/')
def index():
    return {"details":"found"}

@app.post("/fetch_customer_data_maibro")
async def fetch_customer_data(request:Request):
    customer_details=await request.json()
    logging.info("Pushing customer details")
    logging.info(customer_details)
    print("the requesr dagte",customer_details["data"])
    print(type(customer_details["data"][0]))
    store_into_redis(customer_details["data"])
    return {"message":"Success"}

@app.post("/get_data_maibro")
async def get_data(request:Request):
    customer_details=await request.json()
    print("customer_details",customer_details)
    result = fetch_data(customer_details["data"])
    return {"message":result}


if __name__ == "__main__":
    run("get_customer_details_fastapi:app", host="0.0.0.0", port=9924,workers=1)


#sudo kill -9 $(sudo lsof -t -i:8823)