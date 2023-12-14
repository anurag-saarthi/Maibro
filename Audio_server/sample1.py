import hashlib
import json
import os
import re
import shutil

def find_hash(text,template_id):
    updated_text = text+template_id
    hash_object = hashlib.md5(updated_text.encode('utf-8'))
    file_name = str(hash_object.hexdigest())
    return text, file_name

with open("Main_Response.json","r") as f:
    data=json.load(f)
# f = open("file_tracker_english.txt", "w")
# PATH = "/Users/debadityamandal/Desktop/SHRIRAM/GUJRATI/STATIC/"
# dst_path = "/Users/debadityamandal/Desktop/Sriram_updated_flow_tts/in_folder/"
# for file in os.listdir(PATH):
#     shutil.copy(PATH + file, dst_path)
#     filename = file.split(".")[0]
#     for row in data:
#         utterance_template=row['Response_ID']
#         if utterance_template == filename:
#             text = row['Gujarati response']
#             template, updated_file = find_hash(text)
#             os.rename(dst_path + file, dst_path + updated_file + ".wav")
# print("Completed")

# src_path = "/Users/prasannakumar/Desktop/saarthiprojects/maia_tts/out_folder/"
# dst_path = "/Users/prasannakumar/Desktop/saarthiprojects/maia_tts/maia_audios_converted/HINDI/ENTITY/"
# for row in data:
#     if "{" in row['Hindi']:
#         english=row["Hindi"]
#         template_id = row["Response_ID"]
#         print(template_id)
#         splits=re.split("{\w+}",english)
#         print(splits)
#         print("********************")
#         for i in range(0,len(splits)):
#             present_file_name = template_id +"_"+str(i+1)
#             text_passed,new_file_name=find_hash(splits[i],template_id)
#             print(text_passed)
#             print(new_file_name)
#             print(present_file_name)
#             print("_______________________")
#             shutil.copy(src_path + present_file_name+".wav", dst_path)
#             os.rename(dst_path + present_file_name+".wav", dst_path + new_file_name + ".wav")
#             # f.write('"'+template+'"'+"\t"+file_name+"\n")


# print(find_hash("नमस्ते, क्या मेरी बात ","utter_greet_name_predue_RFYB_WAOR_M"))
# print(find_hash("Could I have","utter_request_for_customer_predue_static_M"))