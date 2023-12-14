#!/bin/bash
exec python Orchestrator/CZ/orchestrator.py --port 9255 &
exec python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core.yml --port 9434 -vv &
exec python -m rasa run actions --actions actions.actions --port 6321 -vv &
exec python nlu/emi_english/app.py &
exec python nlg/emi_english/nlg_server.py &
exec python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_hindi.yml --port 6434 -vv &
exec python -m rasa run actions --actions actions.actions --port 7434 -vv &
exec python nlu/emi_english/app_hindi.py &
exec python nlg/emi_english/nlg_server_hindi.py &
exec python get_customer_details_fastapi.py &
exec python Audio_server/streaming_api.py