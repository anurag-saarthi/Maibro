#FROM saarthicore114.azurecr.io/rasa114:latest
FROM 907972392184.dkr.ecr.ap-south-1.amazonaws.com/rasa114:latest

RUN pip3 install num2words
RUN pip3 install pydub
RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN pip3 install fastapi
RUN pip3 install azure
RUN pip3 install azure-cognitiveservices-speech==1.19.0
RUN pip3 install python-dotenv==0.20.0
RUN pip3 install uvicorn
RUN pip3 install gunicorn
RUN pip3 install dnspython
RUN pip3 install aiohttp
RUN pip3 install --upgrade google-cloud-texttospeech

COPY . /app


RUN cd /app/core && pip install -r requirements.txt && pip install -r requirements-setup.txt

EXPOSE 9256
EXPOSE 9434
EXPOSE 6321
EXPOSE 13522
EXPOSE 15618

EXPOSE 6434
EXPOSE 7434
EXPOSE 14520
EXPOSE 15517


EXPOSE 9924
EXPOSE 7020

ENTRYPOINT ["/app/start_image.sh"]