#!/bin/bash
cp /dev/null nohup.out
export REDIS_HOST="localhost"
export REDIS_PASSWORD="sam@1234"

sudo kill -9 $(sudo lsof -t -i:9256)
sudo kill -9 $(sudo lsof -t -i:9924)
sudo kill -9 $(sudo lsof -t -i:6321)
sudo kill -9 $(sudo lsof -t -i:15618)
sudo kill -9 $(sudo lsof -t -i:13522)
sudo kill -9 $(sudo lsof -t -i:6434)
sudo kill -9 $(sudo lsof -t -i:7434)
sudo kill -9 $(sudo lsof -t -i:14520)
sudo kill -9 $(sudo lsof -t -i:15517)
sudo kill -9 $(sudo lsof -t -i:9434)



# sudo kill -9 $(sudo lsof -t -i:8333)
# sudo kill -9 $(sudo lsof -t -i:6334)
# sudo kill -9 $(sudo lsof -t -i:6335)
# sudo kill -9 $(sudo lsof -t -i:7334)
# sudo kill -9 $(sudo lsof -t -i:7335)
# sudo kill -9 $(sudo lsof -t -i:12525)
# sudo kill -9 $(sudo lsof -t -i:14515)
# sudo kill -9 $(sudo lsof -t -i:12524)
# sudo kill -9 $(sudo lsof -t -i:14514)
# sudo kill -9 $(sudo lsof -t -i:7336)
# sudo kill -9 $(sudo lsof -t -i:12526)
# sudo kill -9 $(sudo lsof -t -i:14516)
# sudo kill -9 $(sudo lsof -t -i:6336)
# sudo kill -9 $(sudo lsof -t -i:6337)
# sudo kill -9 $(sudo lsof -t -i:7337)
# sudo kill -9 $(sudo lsof -t -i:12527)
# sudo kill -9 $(sudo lsof -t -i:14518)




exec python Orchestrator/CZ/orchestrator.py --port 9255 &


exec rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core.yml --port 9434 -vv &
exec rasa run actions --actions actions.actions --port 6321 -vv &
exec python nlu/emi_english/app.py &
exec python nlg/emi_english/nlg_server.py &

exec rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_hindi.yml --port 6434 -vv &
exec rasa run actions --actions actions.actions --port 7434 -vv &
exec python nlu/emi_english/app_hindi.py &
exec python nlg/emi_english/nlg_server_hindi.py &

exec python get_customer_details_fastapi.py &

exec python Audio_server/streaming_api.py &


# exec   nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_tamil.yml --port 6334 -vv &
# exec   nohup rasa run actions --actions actions.actions --port 7334 -vv &
# exec   nohup python nlu/emi_english/app_tamil.py &
# exec   nohup python nlg/emi_english/nlg_server_tamil.py &


# exec   nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_malayalam.yml --port 6335 -vv &
# exec   nohup rasa run actions --actions actions.actions --port 7335 -vv &
# exec   nohup python nlu/emi_english/app_malayalam.py &
# exec   nohup python nlg/emi_english/nlg_server_malayalam.py &

# exec   nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_kannada.yml --port 6336 -vv &
# exec   nohup rasa run actions --actions actions.actions --port 7336 -vv &
# exec   nohup python nlu/emi_english/app_kannada.py &
# exec   nohup python nlg/emi_english/nlg_server_kannada.py &


# exec   nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_telugu.yml --port 6337 -vv &
# exec   nohup rasa run actions --actions actions.actions --port 7337 -vv &
# exec   nohup python nlu/emi_english/app_telugu.py &
# exec   nohup python nlg/emi_english/nlg_server_telugu.py &

