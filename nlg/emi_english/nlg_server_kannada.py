import argparse
import logging
import requests
import ast
import json
import os
import datetime

from sanic import Sanic, response

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

nlg_logger = setup_logger('nlg_logger', 'logs/nlg_logger.log')

DEFAULT_SERVER_PORT = 14516

DEFAULT_SANIC_WORKERS = 1


def create_argument_parser():
    """Parse all the command line arguments for the nlg server script."""

    parser = argparse.ArgumentParser(description="starts the nlg endpoint")
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_SERVER_PORT,
        type=int,
        help="port to run the server at",
    )
    parser.add_argument(
        "--workers",
        default=DEFAULT_SANIC_WORKERS,
        type=int,
        help="Number of processes to spin up",
    )

    return parser


async def generate_response(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    args = nlg_call.get("arguments", {})
    print("Args", args)
    template = nlg_call.get("template")
    bot_response = dict()
    utterance_transcript = "Kannada"
    utterance = 'Kannada TTS'
    audio_code = 'Kannada_Audio_ID'
    print("Started reading JSON files")
    json_data = "nlg/emi_english/json_files/"
    files = os.listdir(json_data)
    data = []
    
    for f in files:
        with open(json_data + f, "r+", encoding='utf-8') as q:
            try:
                data1 = json.load(q)
                data = data +data1
            except Exception as e:
                print(e)
    print("Completed reading JSON files")
    for item in data:
        if item and "Response_ID" in item and item["Response_ID"] == template and \
                utterance in item:
            if "buttons" in item and item["buttons"] and item["buttons"] == "":
                text = "".join(x.get(utterance, '') for x in item)
                args_list = list(args.keys())
                audio_id = "".join(item.get(audio_code))
                if len(args_list) == 0:
                    bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id
                else:
                    text = text.format(**args)
                    bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id
            else:
                text = "".join(item.get(utterance))
                text_1 = "".join(item.get(utterance_transcript))
                audio_id = "".join(item.get(audio_code))
                print("TEXT: ", text)
                args_list = list(args.keys())
                print("ARG: ", args_list)
                if len(args_list) == 0:
                    bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id+"<transcript_text>"+text_1
                else:
                    text = text.format(**args)
                    text_1 = text_1.format(**args)
                    bot_response["text"] = text+"<template>"+template+"<audio_id>"+audio_id+"<transcript_text>"+text_1

                x = ast.literal_eval(item["buttons"]) if "buttons" in item and \
                                                         item["buttons"] else []
                bot_response["buttons"] = x
    return bot_response

def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/nlg", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        in_time=datetime.datetime.now()
        nlg_call = request.json
        print("NLG Response", nlg_call)
        bot_response = await generate_response(nlg_call)
        end_time=datetime.datetime.now()
        delay=end_time-in_time
        sender_id = nlg_call["tracker"]["sender_id"]
        out_time = "session_id %s"%sender_id+"\t"+"Incoming Time %s"%in_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n"
        nlg_logger.info(out_time)
        return response.json(bot_response)

    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)
