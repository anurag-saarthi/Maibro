from actions.utils.common_imports import *
from actions.utils.helper import *
import copy
import os

helper = Helper()

from dotenv import dotenv_values
config = dotenv_values(".env")
if len(config) > 0:
    REDIS_HOST = config["REDIS_HOST"]
    REDIS_PASSWORD = config["REDIS_PASSWORD"]
else:
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = "prod-saarthi-redis.1vscjj.ng.0001.aps1.cache.amazonaws.com"
REDIS_PASSWORD = ""
REDIS_PORT = 6379
REDIS_DB = 14

red_lang = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)

class ActionGreet(Action):
    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        print("inactiongreet")
        intent = tracker.latest_message.get("intent").get("name")
        greet_count = tracker.get_slot("greet_count")
        user_message = tracker.latest_message.get("text")
        # emi_flow = tracker.get_slot("emi_flow")
        flow_type = tracker.get_slot("flow_type")
        utter_client_name =tracker.get_slot("utter_client_name_slot")
        utter_flow =tracker.get_slot("utter_flow_slot")
        utter_type =tracker.get_slot("utter_type_slot")
        utter_category =tracker.get_slot("utter_category_slot")
        utter_bot_gender =tracker.get_slot("utter_bot_gender_slot")
        client_name = tracker.get_slot("client_name_slot")
        agent_name = tracker.get_slot("agent_name")
        customer_name=tracker.get_slot("customer_name")
        template_structure = tracker.get_slot("template_structure")
        name_confirmation=tracker.get_slot("name_confirmation")
        requested_slot = tracker.get_slot(REQUESTED_SLOT)

        if greet_count < 2:
            if requested_slot == "name_confirmation":
                print("okie")
                # dispatcher.utter_template(
                #         "utter_G_bot_capability_2_"+template_structure,
                #         tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Greet", flag=DEFAULT_FLAG)
            else:
                dispatcher.utter_template(
                        "utter_G_bot_capability_2_"+template_structure,
                        tracker)
                send_and_store_disposition_details(
                    tracker=tracker,
                    dispatcher=dispatcher,
                    disposition_id="Greet",
                    flag=DEFAULT_FLAG,
                )
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("greet_count", int(greet_count) + 1),
            ]
        else:
            # dispatcher.utter_template("utter_RPC_3_"+template_structure,tracker,bot_name= agent_name,client_name=client_name) # notfound
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker,bot_name= agent_name,client_name=client_name) # notfound
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                user_message=user_message,
                flag=TIMEOUT_FLAG,
                disposition_id="Greet",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen"), AllSlotsReset()]



class ActionWait(Action):
    def name(self):
        return "action_wait"

    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        wait_count = tracker.get_slot("wait_count")
        template_structure = tracker.get_slot("template_structure")
        print("template_structure----------->",template_structure)
        # bot_gender = tracker.get_slot("bot_gender")
        if wait_count < 2:
            dispatcher.utter_template("utter_G_wait_"+template_structure,tracker) # notfound
            
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Wait",
                flag=WAIT_FLAG,
            )
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("wait_count", wait_count + 1),
            ]
        else:
            dispatcher.utter_template(
               "utter_G_talk_to_human_"+template_structure,tracker # notfound
            )
            user_message = tracker.latest_message.get("text")
            # helper.send_conversation_flag(TIMEOUT_FLAG, dispatcher)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                flag=TIMEOUT_FLAG,
                disposition_id="Human Handoff"
            )
            return [FollowupAction("action_listen"), AllSlotsReset()]


class ActionChangeLanguage(Action):
    def name(self):
        return "action_change_language"
    def run(self, dispatcher, tracker, domain):
        change_language_count = tracker.get_slot("change_language_count")
        emi_amount = tracker.get_slot("emi_amount_slot")
        loan_amount = tracker.get_slot("loan_amount")
        contact_no = tracker.get_slot("contact_no")
        flow_type = tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        language = tracker.get_slot("language")
        variation=tracker.get_slot("variation")
        bot_gender=tracker.get_slot("bot_gender")
        # bot_gender = tracker.get_slot("bot_gender")
        customer_language = tracker.get_slot("customer_language_slot")
        
        # SRP = SRP_value(customer_language,region)
        trail_count = tracker.get_slot("trail_count")
        change_specific_language_count = tracker.get_slot("change_specific_language_count")
        text = tracker.latest_message.get("text")
        supported_languages_again = tracker.get_slot("supported_languages")
        print("supported_languages_again>>>>>>>",supported_languages_again)
        supported_languages_1 = tracker.get_slot("supported_languages")
        print("supported_languages_1",supported_languages_1)
        supported_languages_1 = supported_languages_1.lower()
        supported_languages = supported_languages_1.split(",")
        print("The supported languages are", supported_languages)
        supported_languages = str(supported_languages)[1:-1]
        print("supported_languages->",supported_languages)
        print("change_language_count->",change_language_count)
        text = text.lower()
        print("text:::::::::::::::", text)
        all_languages = { #English,Hindi,Telugu,Kannada,Malayalam,Tamil,Bengali,Marathi,Punjabi,Gujarati 
            "english":["english","इंग्लिश","अंग्रेज़ी","ఇంగ్లీష్","ఆంగ్ల","ಇಂಗ್ಲಿಷ್","ಇಂಗ್ಲಿಶ್","ഇംഗ്ലീഷ്","ഇംഗ്ളീഷ്","இங்கிலீஷ்","ஆங்கிலம்",
                        "ইংলিশ","ইংরেজি","इंग्लिश","अंग्रेज़ी","अंग्रेझी","अंगरेझी","ਇੰਗਲਿਸ਼","ਅੰਗਰੇਜ਼ੀ","ઈંગ્લીશ","અંગ્રેજી","ઇંગ્લિશ","अंग्रेजी","ഇംഗ്ലിഷ്","ഇംഗ്ലീഷു","இங்கிலிஷ்"],
            "hindi":["hindi","हिंदी","हिन्दी","हिंदि","హిందీ","హింది","హిన్దీ","హిన్ది","ಹಿಂದಿ","ಹಿಂದೀ","ഹിന്ദി","ഹിൻഡി","ஹிந்தி","இந்தி",
                        "হিন্দি","হিন্দী","हिंदी","हिन्दी","हिंदि","ਹਿੰਦੀ","ਹਿਦੀ","હિન્દી","હિંદી"],
            "telugu":["telugu","तेलुगु","तेलगू","తెలుగు","ತೆಲುಗು","ತೆಲಗು","തെലുങ്ക്","തെലുങ്കു","തെലുഗു","തെലഗു","தெலுங்கு","தெலுகு",
                        "তেলেগু","তেলেগূ","तेलुगु","तेलुगू","तेलगू","तेलगु","तेल्गु","तेल्गू","ਤੇਲਗੂ","ਤੇਲਗੁ","ਤੇਲੁਗੁ","ਤੇਲੁਗੂ","તેલુગુ","તેલૂગૂ","તેલુગૂ","તેલૂગુ"],
            "kannada": ["kannada","कन्नड़","कन्नड़ा","कन्नड","కన్నడ","కన్నడా","కంనడ","ಕನ್ನಡ","ಕನ್ನಡ್","കന്നഡ","കന്നഡ്","கன்னடம்","கன்னடா",
                        "কন্নড়","কান্নাডা","कन्नड़","कनाडा","कनडा","कनड","ਕੰਨੜ","ਕੰਨੜਾ","કન્નડ","કન્નડા"],
            "malayalam": ["malayalam","मलयालम","मलायलम","मलयाळम","మలయాళం","మళయాళం","మళయాలం","మాలయాలం","మలయాలమ్","మళయాలమ్",
                        "ಮಲಯಾಳಂ","ಮಲಯಾಳಮ್","ಮಳ್ಯಾಳುಂ","മലയാളം","மலையாளம்","মালায়লাম","মালায়ালাম","मलयालम","मल्यालम","मलयाल्म","मलयाळम",
                        "ਮਲਿਆਲਮ","ਮਲਿਆਲਮਾ","મલયાલમ"],
            "tamil": ["tamil","तमिल","तमिळ","तमील","తమిళ్","తమిల్","తమిళ","తమిల","ತಮಿಳ್","ತಮಿಳು","ತಮಿಲ್","തമിഴ്","തമിൾ","തമിള്","தமிழ்",
                        "தமிழில்","তামিল","তামীল","तमिल","तामिळ","तमिळ","तामीळ","तामील","ਤਾਮਿਲ","ਤਮਿਲ","તમિલ","તામિલ","તામીલ","તમીલ"],
            "bengali": ["bengali","बांगला","बेंगली","बांगला","बेंगली","ಬಂಗಾಳಿ","ಬಂಗಾಲಿ","ಬೆಂಗಾಲಿ","ബംഗാളി","ബംഗ്ളാ","ബംഗ്ലാ","பெங்காலி",
                        "বাংলা","বেঙ্গলি","बांगला","बेंगली","बांग्ला","बंग्ला","बंगाली","ਬੰਗਲਾ","ਬਾਂਗਲਾ","ਬੰਗਾਲੀ","બંગાળી","બંગાલી","બાંગ્લા","બનગાળી","બંગાલિ"],
            "marathi": ["marathi","मराठी","माराठी","మరాఠీ","మరాఠి","ಮರಾಠಿ","ಮರಾತಿ","മറാത്തി","മറാഠി","മറാത്ത","மராத்தி","மராட்டி",
                        "মারাঠি","মারাঠী","मराठि","माराठी","मराटी","ਮਰਾਠੀ","ਮਰਾਠਿ","ਮਰਾਟੀ","મરાઠી"],
            "punjabi": ["punjabi","पंजाबी","पँजाबी","पन्जाबी","पञ्जाबी","పంజాబీ","ಪಂಜಾಬಿ","ಪಂಜಾಬೀ","പഞ്ചാബി","പഞ്ചാബീ","பஞ்சாபி","পাঞ্জাবি","পাঞ্জাবী",
                        "पंजाबी","पंजाबि","ਪੰਜਾਬੀ","ਪਜਾਬੀ","પંજાબી","પજાબી","પનજાબી","પંજાબિ"],
            "gujarati": ["gujarati","गुजराती","गुज़राती","గుజరాతీ","గుజరాతి","ಗುಜರಾತಿ","ಗುಜುರಾತಿ","ഗുജറാത്തി","ഗുജ്‌റാത്തി","குஜ்ராத்தி","குஜராத்தி",
                        "গুজরাটি","গুজরাটী","गुजराती","गुजराथी","गुजराति","ਗੁਜਰਾਤੀ","ਗੁਜਰਾਥੀ","ગુજરાતી"],
            "odia" : ["மொழியில்","ओड़िया","ओडिया","odia","odiya","ஓடியா","ఒడియా","ಒಡಿಯಾ","ഒഡിയ","ਓਡੀਆ","ஒடியா"],
        }
        supported_dict = {}
        unsupported_dict = {}
        existed = 0
        unexisted = 0
        for key,value in all_languages.items():
            if key in supported_languages:
                supported_dict[key] = value
        for key,value in supported_dict.items():
            for k in range(0,len(value)):
                if value[k] in text:
                    existed+=1
                    lan = key
                    break
        for key,value in all_languages.items():
            if key not in supported_languages:
                unsupported_dict[key] = value
        langauge_1 = None
        for key,value in unsupported_dict.items():
            for k in range(0,len(value)):
                if value[k] in text:
                    langauge_1=key
                    unexisted+=1
        if change_language_count < 2:
            print("existed", existed)
            print("Unexisted",unexisted)
            if existed == 0 and unexisted == 0:
                print("in existed == 0 and unexisted == 0")
                # my_list = supported_languages_again
                # print("type.......:",type(my_list))
                # print("myList >>>>>>",my_list)
                # my_string = ', '.join(my_list)
                # result = ', '.join(re.findall(r'"([^"]+)"', supported_languages_again))
                # print("my_string >>>>>>",result)
                my_list = eval(supported_languages_again)
                result = '", "'.join(my_list)
                result = result.replace("\"","")
                template_name =  (
                                "utter_language_change_no_language_" + variation + flow_type + "_static_" + bot_gender
                            )
                dispatcher.utter_template(template_name,tracker,languages_supported="english, hindi, malayalam")
                send_and_store_disposition_details(
                    tracker,
                    dispatcher,
                    flag=DEFAULT_FLAG,
                    disposition_id="Language Change - Without Language",
                    flow_type=flow_type,
                )
                return [FollowupAction("action_listen")]
            if existed >= 1:
                print("existed >= 1")
                print("The ln value ",lan)
                my_list = eval(supported_languages_again)
                result = '", "'.join(my_list)
                result = result.replace("\"","")
                send_and_store_disposition_details(
                    tracker,
                    dispatcher,
                    flag=DEFAULT_FLAG,
                    disposition_id="Language Change - Supported",
                    language=lan,
                    flow_type=flow_type,
                )
                return [
                    FollowupAction("lg_rpc_form"),
                    SlotSet(REQUESTED_SLOT, None),
                    SlotSet("trail_count", 0),
                    SlotSet("change_specific_language_count",change_specific_language_count + 1),
                    SlotSet("change_language_count", change_language_count + 2),
                    SlotSet("customer_language_slot", lan),
                ]
            elif unexisted >= 1:
                print("unexisted >= 1")
                print("language-else11111111",supported_languages)
                ###
                template_name =  (
                                "utter_language_not_supported_insurance_" + variation + flow_type + "_static_" + bot_gender
                            )
                dispatcher.utter_template(template_name,tracker,languages_supported="english, hindi, malayalam")
                send_and_store_disposition_details(
                    tracker,
                    dispatcher,
                    flag=TIMEOUT_FLAG,
                    disposition_id="Language Change - Not Supported",
                    flow_type=flow_type,
                )
                return [FollowupAction("action_listen"), AllSlotsReset()]
            else:
                template_name =  (
                                "utter_language_change_no_language_" + variation + flow_type + "_static_" + bot_gender
                            )
                dispatcher.utter_template(template_name,tracker,languages_supported="english, hindi, malayalam")
                send_and_store_disposition_details(
                    tracker,
                    dispatcher,
                    flag=DEFAULT_FLAG,
                    disposition_id="Language Change - Not Supported", 
                    language=language,
                    flow_type=flow_type,
                )
                return [FollowupAction("action_listen")]
        else:
            print("language-else",supported_languages)
            template_name =  (
                                "utter_language_not_supported_insurance_" + variation + flow_type + "_static_" + bot_gender
                            )
            dispatcher.utter_template(template_name,tracker,languages_supported="english, hindi, malayalam")
            send_and_store_disposition_details(
                tracker,
                dispatcher,
                flag=TIMEOUT_FLAG,
                disposition_id="Human Handoff",
                language=language,
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionDefault(Action):
    def name(self): 
        return "action_default"

    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        # bot_gender = tracker.get_slot("bot_gender")
        customer_language = tracker.get_slot("customer_language_slot")
        # SRP = SRP_value(customer_language,region)
        default_count = tracker.get_slot("default_count")
        gender = tracker.get_slot("gender_slot")
        contact_no = tracker.get_slot("contact_no")
        # if gender == "F":
        #     bot_gender = "_M"
        # else:
        #     bot_gender = "_F"
        print(default_count, "default_count-1")
        print("Entering into defualt comment")
        if default_count < 2:
            dispatcher.utter_template("utter_G_gibberish_a_"+template_structure, tracker) #notfound
            send_and_store_disposition_details(
                tracker,
                dispatcher,
                flag=DEFAULT_FLAG,
                disposition_id="Not understood",
                flow_type=flow_type,
            )
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("default_count", default_count + 1),
            ]
        else:
            dispatcher.utter_template("utter_G_out_of_context_a_WC_"+template_structure,tracker) #notfound
            send_and_store_disposition_details(
                tracker,
                dispatcher,
                flag=TIMEOUT_FLAG,
                disposition_id="Human handoff",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen"), AllSlotsReset()]



class ActionWrongName(Action):
    def name(self):
        return "action_wrong_name"
    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        wrong_name_count = tracker.get_slot("wrong_name_count")
        if wrong_name_count < 2:
            dispatcher.utter_template("utter_RPC_deny_general_ask_inform_name_pronunciation_wrong_name_"+template_structure, tracker) #notfound
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                flag=DEFAULT_FLAG,
                disposition_id="Deny - Wrong Name",       
                flow_type=flow_type,
            )
            return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                SlotSet("wrong_name_count",wrong_name_count+1),
                FollowupAction(tracker.active_form.get("name")),
            ]
        else:
            dispatcher.utter_template("utter_RPC_deny_wrong_number_", tracker) #notfound
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                flag=TIMEOUT_FLAG,
                disposition_id="Deny - Wrong Name",
            )
        return [FollowupAction("action_listen"), AllSlotsReset()]



class ActionBye(Action):  # Template not there
    def name(self):
        return "action_bye"
    def run(self, dispatcher, tracker, domain):
        template_structure = tracker.get_slot("template_structure")
        dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker)  #notfound
        send_and_store_disposition_details(
            tracker=tracker,
            dispatcher=dispatcher,
            flag=TIMEOUT_FLAG,
            disposition_id="Greet",
            )
        return [FollowupAction("action_listen"), AllSlotsReset()]



class ActionNoMessage(Action):
    def name(self):
        return "action_no_message"

    def run(self, dispatcher, tracker, domain):
        print("action_no_message***")
        flow_type=tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        print("template_structure",template_structure)
        # bot_gender = tracker.get_slot("bot_gender")
        customer_language = tracker.get_slot("customer_language_slot")
        request_slot = tracker.get_slot("REQUESTED_SLOT")
        # SRP = SRP_value(customer_language,region)
        no_response_count = tracker.get_slot("no_response_count")
        print("****************",request_slot)
        came_from_form_slot = tracker.get_slot("came_from_form_slot")
        current_main_slot = tracker.get_slot("current_main_slot")
        print("-------->",came_from_form_slot)
        print("-------->",current_main_slot)
        if no_response_count is None or no_response_count<2:
            if tracker.active_form.get("name") is not None:
                print("ok1")
                no_response_count = no_response_count + 1
                template = ("utter_G_default_b_WC_"+template_structure) #notfound
                dispatcher.utter_template(template, tracker)
                return [
                    SlotSet(REQUESTED_SLOT, None),
                    SlotSet("trail_count", get_trail_count(tracker)),
                    FollowupAction(tracker.active_form.get("name")),
                    SlotSet("no_response_count", int(no_response_count))
                ]
            print("ok2")
            template = ("utter_G_default_b_WC_"+template_structure) #notfound
            print("template----<>",template)
            # template = "utter_reply_greaterthan_5sec_"+flow_type+"_static" + bot_gender
            dispatcher.utter_template(template, tracker)
            return [FollowupAction("action_listen"), SlotSet("no_response_count", 1)]
        else:
            dispatcher.utter_template("utter_G_are_you_there_threshold_lessthan_2_b_WC_"+template_structure,tracker) #notfound
            # dispatcher.utter_template(template,tracker,) 
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                user_message="no_message",
                flag=TIMEOUT_FLAG,
                disposition_id="No Response",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen"), AllSlotsReset()]

class ActionRepeat(Action): # Need to add template
    def name(self):
        return 'action_repeat'

    def run(self, dispatcher, tracker, domain):
        emi_flow=tracker.get_slot("emi_flow")
        sheet_name=tracker.get_slot("sheet_name")
        repeat_count=tracker.get_slot("repeat_count")
        template_structure=tracker.get_slot("template_structure")
        if repeat_count < 2:
            dispatcher.utter_template("utter_G_speak_clear_"+template_structure, tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Repeat", flag=DEFAULT_FLAG)
            # return [
            # SlotSet(REQUESTED_SLOT, None),
            # SlotSet("trail_count", None),
            # SlotSet("repeat_count", repeat_count+1),
            # FollowupAction(tracker.active_form.get("name")),
            return get_return_values(tracker)
        # ]
        else:
            dispatcher.utter_template("utter_G_customer_care_contact_"+template_structure, tracker)
            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Human Handoff", flag=TIMEOUT_FLAG)
            return [FollowupAction("action_listen")]

class ActionHowAreYou(Action):
    def name(self):
        return "action_how_are_you"

    def run(self, dispatcher, tracker, domain):
        how_are_you_slot = tracker.get_slot("how_are_you_slot")
        flow_type = tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        contact_no = tracker.get_slot("contact_no")
        if how_are_you_slot<2:
            dispatcher.utter_template(
                "utter_G_out_of_context_a_WC_",+template_structure,
                tracker
            )
            send_and_store_disposition_details(
                tracker=tracker,
                flag=DEFAULT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Out Of Context",
                flow_type=flow_type,
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("how_are_you_slot", how_are_you_slot+1)
        ]
        else:
            dispatcher.utter_template(
                "utter_G_out_of_context_a_WC_"+template_structure,
                tracker, customer_care_number = contact_no 
            )
            dispatcher.utter_template("utter_G_out_of_context"+template_structure,tracker)  # Template is not there
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Out Of Context",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen")]


class ActionWhoAreYou(Action):
    def name(self):
        return "action_who_are_you"
    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        utter_client_name =tracker.get_slot("utter_client_name_slot")
        utter_flow =tracker.get_slot("utter_flow_slot")
        utter_type =tracker.get_slot("utter_type_slot")
        utter_category =tracker.get_slot("utter_category_slot")
        utter_bot_gender =tracker.get_slot("utter_bot_gender_slot")
        client_name = tracker.get_slot("client_name_slot")
        who_are_you_slot=tracker.get_slot("who_are_you_slot")
        template_structure = tracker.get_slot("template_structure")
        agent_name = tracker.get_slot("agent_name")
        requested_slot = tracker.get_slot(REQUESTED_SLOT)
        greet_count = tracker.get_slot("greet_count")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")
        vehicle_detail = tracker.get_slot("vehicle_detail")
        
        if who_are_you_slot<2:
            if greet_count < 2:
                if requested_slot == "name_confirmation":
                    print("okie")
                # dispatcher.utter_template("utter_FQ_iQ1_no_repeat_TVS_LG_CC_instaplus_F",tracker)
                    # send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Agent Identification", flag=DEFAULT_FLAG)
                else:
                    if flow_type == "insurance_renewal":
                        template_name =  "utter_FAQ_who_are_you_" + variation + flow_type + "_static_" + bot_gender
                    else:
                        template_name =  "utter_FAQ_client_name_" + variation + flow_type + "_static_" + bot_gender
                    dispatcher.utter_template(template_name,tracker,client_name=client_name,vehicle_detail=vehicle_detail) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=DEFAULT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Ask Client Info",
                flow_type=flow_type,
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("who_are_you_slot", who_are_you_slot+1)
        ]
        else:
            dispatcher.utter_template(
                "utter_G_bot_capability_2_"+template_structure,
                tracker)
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Agent Identification",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen")]

class ActionAreYouThere(Action):
    def name(self):
        return "action_are_you_there"

    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        utter_client_name =tracker.get_slot("utter_client_name_slot")
        utter_flow =tracker.get_slot("utter_flow_slot")
        utter_type =tracker.get_slot("utter_type_slot")
        utter_category =tracker.get_slot("utter_category_slot")
        utter_bot_gender =tracker.get_slot("utter_bot_gender_slot")
        are_you_there_slot=tracker.get_slot("are_you_there_slot")
        template_structure = tracker.get_slot("template_structure")
        print("faq_action_are_you_there")
        # dispatcher.utter_template("utter_G_general_are_you_there_"+template_structure,tracker)
        # send_and_store_disposition_details(
        #     tracker=tracker,
        #     dispatcher=dispatcher,
        #     disposition_id="General - No Message",
        #     flag=DEFAULT_FLAG,
        #     flow_type=flow_type,
        # )
        # return get_return_values(tracker)
        if are_you_there_slot<2:
            dispatcher.utter_template("utter_G_general_are_you_there_"+template_structure,tracker)
            send_and_store_disposition_details(
                tracker=tracker,
                flag=DEFAULT_FLAG,
                dispatcher=dispatcher,
                disposition_id="No Response",
                flow_type=flow_type,
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("are_you_there_slot", are_you_there_slot+1)
        ]
        else:
            # dispatcher.utter_template("utter_G_general_are_you_there_"+template_structuretracker)
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="No Response",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen")]

class ActionCustomerName(Action):
    def name(self):
        return "action_customer_name"

    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        intent = tracker.latest_message.get("intent").get("name")
        emp_name = tracker.get_slot("customer_name")
        customer_name_slot=tracker.get_slot("customer_name_slot")
        if customer_name_slot<2:
            dispatcher.utter_template("utter_FAQ_general_action_by_bot_client_name_who_are_you_"+template_structure, tracker,customer_name =emp_name)
            send_and_store_disposition_details(
                tracker=tracker,
                flag=DEFAULT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Greet",
                flow_type=flow_type,
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("customer_name_slot", customer_name_slot+1)
        ]
        else:
            # dispatcher.utter_template("utter_RPC_alt_"+template_structure, tracker,customer_name =emp_name)
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) # Template is not there.
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Greet",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen")]

class ActionOutOfContext(Action):
    def name(self):
        return "action_out_of_context"

    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        out_of_context_count=tracker.get_slot("out_of_context_count")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")

        if out_of_context_count<2:
            template_name =  "utter_FAQ_out_of_context_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker,customer_care_number = customer_care_number)
            send_and_store_disposition_details(
                tracker=tracker,
                flag=DEFAULT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Out Of Context",        ##dispo
                flow_type=flow_type,
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("out_of_context_count", out_of_context_count+1)
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)  
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Out Of Context",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen")]


class ActionClientName(Action):
    def name(self):
        return "action_client_name"
    def run(self, dispatcher, tracker, domain):
        flow_type = tracker.get_slot("flow_type")
        client_name = tracker.get_slot("client_name_slot")
        template_structure = tracker.get_slot("template_structure")
        agent_name = tracker.get_slot("agent_name")
        customer_name=tracker.get_slot("customer_name")
        client_name_slot_1=tracker.get_slot("client_name_slot_1")
        requested_slot = tracker.get_slot(REQUESTED_SLOT)

        if client_name_slot_1<2:
            if requested_slot == "name_confirmation":
                send_and_store_disposition_details(
                tracker=tracker,
                            flag=DEFAULT_FLAG,
                            dispatcher=dispatcher,
                            disposition_id="Ask Client Name",                  
                            flow_type=flow_type
                )
            else:
                dispatcher.utter_template("utter_G_bot_capability_2_"+template_structure,tracker,agent_name =agent_name,client_name=client_name)
                send_and_store_disposition_details(
                tracker=tracker,
                            flag=DEFAULT_FLAG,
                            dispatcher=dispatcher,
                            disposition_id="Ask Client Name",                  
                            flow_type=flow_type
                )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("client_name_slot_1", client_name_slot_1+1)
            ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Ask Client Name",
                flow_type=flow_type,
            )
            return [FollowupAction("action_listen")]


class Actionaskoffer(Action):
    def name(self):
        return "action_ask_offer"
    def run(self, dispatcher, tracker, domain):
        ask_offer_count = tracker.get_slot("ask_offer_count")
        template_structure = tracker.get_slot("template_structure")
        # customer_care_number = tracker.get_slot("customer_care_number")
        flow_type = tracker.get_slot("flow_type")
        if flow_type == "creditwise_wc_tw":

            customer_care_number = "06262260260"
            customer_care_email = "care@creditwisecapital.com"
        else: 
            customer_care_email = "customer.care@herohfl.com"
            customer_care_number = tracker.get_slot("customer_care_number") # add slot

        
        if ask_offer_count <2:         
            dispatcher.utter_template("utter_FAQ_ask_offer_"+template_structure, tracker,customer_care_number=customer_care_number)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Product Offer",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("ask_offer_count", ask_offer_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
        
class Actioninterestrate(Action):
    def name(self):
        return "action_interest_rate"
    def run(self, dispatcher, tracker, domain):
        interest_rate_count = tracker.get_slot("interest_rate_count")
        template_structure = tracker.get_slot("template_structure")
        # customer_care_number = tracker.get_slot("customer_care_number")
        flow_type = tracker.get_slot("flow_type")
        if flow_type == "creditwise_wc_tw":
            customer_care_number = "06262260260"
            customer_care_email = "care@creditwisecapital.com"
        else: 
            customer_care_email = "customer.care@herohfl.com"
            customer_care_number = tracker.get_slot("customer_care_number") # add slot

        delay_reason = tracker.latest_message.get("delay_reason").get("name")
        
        if interest_rate_count <2:
            if delay_reason == "high_interest_rate":
                dispatcher.utter_template("utter_NOIN_not_interested_reason_captured_"+template_structure,tracker)
                disposition = "Not Interested Reason - "+mapping_delay_reasons.get(delay_reason,"No Reason")
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id=disposition,delay_reason = disposition)
                return [FollowupAction("action_listen")]
            else:
                dispatcher.utter_template("utter_FAQ_loan_interest_rate_"+template_structure, tracker)
                send_and_store_disposition_details(
                    tracker=tracker,
                    dispatcher=dispatcher,
                    disposition_id="Ask Interest Rate",
                    flag=DEFAULT_FLAG,  
                )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("interest_rate_count", interest_rate_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Ask Interest Rate"
            )
            return [FollowupAction("action_listen")]
        
# class Actiontenure(Action):
#     def name(self):
#         return "action_tenure"
#     def run(self, dispatcher, tracker, domain):
#         tenure_count = tracker.get_slot("tenure_count")
#         template_structure = tracker.get_slot("template_structure")
#         customer_care_number = tracker.get_slot("customer_care_number")
        
#         if tenure_count <2:         
#             dispatcher.utter_template("utter_FAQ_loan_tenure_"+template_structure, tracker)
#             send_and_store_disposition_details(
#                 tracker=tracker,
#                 dispatcher=dispatcher,
#                 disposition_id="",
#                 flag=DEFAULT_FLAG,  
#             )
#             return [
#             SlotSet(REQUESTED_SLOT, None),
#             SlotSet("trail_count", get_trail_count(tracker)),
#             FollowupAction(tracker.active_form.get("name")),
#             SlotSet("tenure_count", tenure_count+1),
#         ]
#         else:
#             dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
#             send_and_store_disposition_details(
#                 tracker=tracker,
#                 flag=TIMEOUT_FLAG,
#                 dispatcher=dispatcher,
#                 disposition_id="Others"
#             )
#             return [FollowupAction("action_listen")]
        
class Actiondocumentsrequired(Action):
    def name(self):
        return "action_documents_required"
    def run(self, dispatcher, tracker, domain):
        documents_required_count = tracker.get_slot("documents_required_count")
        template_structure = tracker.get_slot("template_structure")
        # customer_care_number = tracker.get_slot("customer_care_number")
        flow_type = tracker.get_slot("flow_type")
        if flow_type == "creditwise_wc_tw":

            customer_care_number = "06262260260"
            customer_care_email = "care@creditwisecapital.com"
        else: 
            customer_care_email = "customer.care@herohfl.com"
            customer_care_number = tracker.get_slot("customer_care_number") # add slot


        
        if documents_required_count <2:         
            dispatcher.utter_template("utter_FAQ_loan_documents_required_"+template_structure, tracker)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Document Required",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("documents_required_count", documents_required_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Ask Document Required"
            )
            return [FollowupAction("action_listen")]


        
        
class Actioninformation(Action):
    def name(self):
        return "action_information"
    def run(self, dispatcher, tracker, domain):
        information_count = tracker.get_slot("information_count")
        template_structure = tracker.get_slot("template_structure")
        context = tracker.latest_message.get("context").get("name")
        # customer_care_number = tracker.get_slot("customer_care_number")
        flow_type = tracker.get_slot("flow_type")
        if flow_type == "creditwise_wc_tw":

            customer_care_number = "06262260260"
            customer_care_email = "care@creditwisecapital.com"
        else: 
            customer_care_email = "customer.care@herohfl.com"
            customer_care_number = tracker.get_slot("customer_care_number") # add slot

        
        if information_count <2:

            if (context == "home_loan" or context == "two_wheeler_loan"  or context == "gold_loan" or context == "four_wheeler_loan" or 
            context == "three_wheeler_loan" or context == "property_loan" or context == "travel_loan" or 
            context == "wedding_loan" or context == "business_loan"): 
                
                dispatcher.utter_template("utter_FAQ_home_loan/two_wheeler_loan/gold_loan/three_wheeler_loan/four_wheeler_loan/property_loan/travel_loan/wedding_loan/business_loaninformation_"+template_structure, tracker,customer_care_number=customer_care_number)
                send_and_store_disposition_details(
                    tracker=tracker,
                    dispatcher=dispatcher,
                    disposition_id="",
                    flag=DEFAULT_FLAG,  
                )
                return [SlotSet(REQUESTED_SLOT, None),SlotSet("trail_count", get_trail_count(tracker)),FollowupAction(tracker.active_form.get("name")),
                SlotSet("information_count", information_count+1),]
            else:
                dispatcher.utter_template("utter_FAQ_loan_general_payment_application_location_timings_change_income_proof_send_executive_visit_exchange_scheme_vehicle_purchase_"+template_structure, tracker,customer_care_number=customer_care_number)
                send_and_store_disposition_details(
                    tracker=tracker,
                    dispatcher=dispatcher,
                    disposition_id="",
                    flag=DEFAULT_FLAG,  
                )
                return [SlotSet(REQUESTED_SLOT, None),SlotSet("trail_count", get_trail_count(tracker)),FollowupAction(tracker.active_form.get("name")),
                SlotSet("information_count", information_count+1),]
                    
                
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]

class Actionprocessingtime(Action):
    def name(self):
        return "action_processing_time"
    def run(self, dispatcher, tracker, domain):
        processing_time_count = tracker.get_slot("processing_time_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        
        if processing_time_count <2:         
            dispatcher.utter_template("utter_FAQ_loan_processing_time_"+template_structure, tracker)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask for Another Product",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("processing_time_count", processing_time_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Ask for Another Product"
            )
            return [FollowupAction("action_listen")]
        
class Actiongeneral(Action):
    def name(self):
        return "action_general"
    def run(self, dispatcher, tracker, domain):
        general_count = tracker.get_slot("general_count")
        template_structure = tracker.get_slot("template_structure")
        context = tracker.latest_message.get("context").get("name")
        customer_care_number = tracker.get_slot("customer_care_number")
    
        if general_count <2:  
            if (context == "loan" or context == "general" or context == "payment" or  context == "application"):    
                dispatcher.utter_template("utter_FAQ_loan_general_payment_application_location_timings_change_income_proof_send_executive_visit_exchange_scheme_vehicle_purchase_"+template_structure, tracker,customer_care_number=customer_care_number)
                send_and_store_disposition_details(
                    tracker=tracker,
                    dispatcher=dispatcher,
                    disposition_id="",
                    flag=DEFAULT_FLAG,  
                )
                return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("general_count", general_count+1),]
            else:
                dispatcher.utter_template("utter_FAQ_home_loan/two_wheeler_loan/gold_loan/three_wheeler_loan/four_wheeler_loan/property_loan/travel_loan/wedding_loan/business_loaninformation_"+template_structure, tracker,customer_care_number=customer_care_number)
                send_and_store_disposition_details(
                    tracker=tracker,
                    dispatcher=dispatcher,
                    disposition_id="",
                    flag=DEFAULT_FLAG,  
                )
                return [
                SlotSet(REQUESTED_SLOT, None),
                SlotSet("trail_count", get_trail_count(tracker)),
                FollowupAction(tracker.active_form.get("name")),
                SlotSet("general_count", general_count+1),]    
            
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
# ---------------> Updated FAQ ---------------<<<<<<<<<<<       
class ActionEmiAmount(Action):
    def name(self):
        return "action_emi_amount"
    def run(self, dispatcher, tracker, domain):
        emi_amount_count = tracker.get_slot("emi_amount_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        
        if emi_amount_count <2:         
            dispatcher.utter_template("utter_FAQ_emi_amount_WC_"+template_structure, tracker,emi_amount=emi_amount)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask EMI Amount",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("emi_amount_count", emi_amount_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
        
class ActionDueDate(Action):
    def name(self):
        return "action_due_date"
    def run(self, dispatcher, tracker, domain):
        due_date_count = tracker.get_slot("due_date_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        due_date = tracker.get_slot("due_date")
        due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y").strftime("%d %B %Y")
        if due_date_count <2:         
            dispatcher.utter_template("utter_FAQ_due_date_WC_"+template_structure, tracker,due_date=due_date)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask EMI Due Date",
                flag=DEFAULT_FLAG,  
            )
            print(tracker.active_form.get("name"),"1180",flush= True)
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("due_date_count", due_date_count+1),
            ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
        
class ActionTenureNew(Action):
    def name(self):
        return "action_tenure"
    def run(self, dispatcher, tracker, domain):
        loan_tenure_count = tracker.get_slot("loan_tenure_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        loan_amount = tracker.get_slot("loan_amount")
        loan_tenure = tracker.get_slot("loan_tenure")
        
        if loan_tenure_count <2:         
            dispatcher.utter_template("utter_FAQ_tenure_WC_"+template_structure, tracker,loan_amount=loan_amount,loan_tenure=loan_tenure)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Tenure",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("loan_tenure_count", loan_tenure_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]

class ActionCreditLimitNew(Action):
    def name(self):
        return "action_credit_limit"
    def run(self, dispatcher, tracker, domain):
        credit_limit_new_count = tracker.get_slot("credit_limit_new_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        loan_amount = tracker.get_slot("loan_amount")
        loan_tenure = tracker.get_slot("loan_tenure")
        
        if credit_limit_new_count <2:         
            dispatcher.utter_template("utter_FAQ_tenure_WC_"+template_structure, tracker,loan_amount=loan_amount,loan_tenure=loan_tenure)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Loan Amount",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("credit_limit_new_count", credit_limit_new_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
        
class ActionBounceCharge(Action):
    def name(self):
        return "action_bounce_charges"
    def run(self, dispatcher, tracker, domain):
        bounce_charge_count = tracker.get_slot("bounce_charge_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        
        if bounce_charge_count <2:         
            dispatcher.utter_template("utter_FAQ_bounce charges_WC_"+template_structure, tracker,)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Bounce Charges",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("bounce_charge_count", bounce_charge_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
        
class ActionPenaltyCharge(Action):
    def name(self):
        return "action_penalty_charges"
    def run(self, dispatcher, tracker, domain):
        penalty_charge_count = tracker.get_slot("penalty_charge_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        
        if penalty_charge_count <=2:         
            dispatcher.utter_template("utter_FAQ_penalty_charges_WC_"+template_structure, tracker,emi_amount=emi_amount)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Late Payment Charges",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("penalty_charge_count", penalty_charge_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
        
class ActionTalktoHumanNew(Action):
    def name(self):
        return "action_talk_to_human_agent"
    def run(self, dispatcher, tracker, domain):
        talk_count = tracker.get_slot("talk_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        
        if talk_count <=2:         
            dispatcher.utter_template("utter_FAQ_talk_to_human_agent_WC_"+template_structure, tracker,customer_care_number=customer_care_number)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Customer Care Contact",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("talk_count", talk_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]


class ActionProcessingFees(Action):
    def name(self):
        return "action_processing_fees"
    def run(self, dispatcher, tracker, domain):
        processing_count = tracker.get_slot("processing_count")
        template_structure = tracker.get_slot("template_structure")
        flow_type = tracker.get_slot("flow_type")
        # customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        # customer_care_email = "customer.care@herohfl.com"
        if flow_type == "creditwise_wc_tw":
            customer_care_number = "06262260260"
            customer_care_email = "care@creditwisecapital.com"
        else: 
            customer_care_email = "customer.care@herohfl.com"
            customer_care_number = tracker.get_slot("customer_care_number") # add slot

        
        
        if processing_count <= 7:         
            dispatcher.utter_template("utter_FAQ_credit_score_interest_rate_processing_time_preclosure_period_processing_fees_WC_"+template_structure, tracker,customer_care_number=customer_care_number,customer_care_email=customer_care_email)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Other Details",
                flag=TIMEOUT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("processing_count", processing_count+1),
        ]
        else:
            dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]


###########################   NEWLY---------ADDED--------  FAQ  ###################
class ActionBenefits(Action):
    def name(self):
        return "action_benefits"
    def run(self, dispatcher, tracker, domain):
        benefits_count = tracker.get_slot("benefits_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")

        if benefits_count <=2:         
            template_name =  "utter_FAQ_benifits_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Benefits",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("benefits_count", benefits_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]

class ActionPremiumAmount(Action):
    def name(self):
        return "action_premium_amount"
    def run(self, dispatcher, tracker, domain):
        premium_amount_count = tracker.get_slot("premium_amount_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")
        
        if premium_amount_count <=2:         
            template_name =  "utter_FAQ_premium_amount_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Premium Amount",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("premium_amount_count", premium_amount_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
     
class ActionDocuments(Action):
    def name(self):
        return "action_documents"
    def run(self, dispatcher, tracker, domain):
        documents_count = tracker.get_slot("documents_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")
        
        if documents_count <=2:         
            template_name =  "utter_FAQ_documents_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Documents Required",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("documents_count", documents_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
   
class ActionOffer(Action):
    def name(self):
        return "action_offer"
    def run(self, dispatcher, tracker, domain):
        offer_count = tracker.get_slot("offer_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")
        
        if offer_count <=2:         
            template_name =  "utter_FAQ_offer_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker) 
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Offer",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("offer_count", offer_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)  
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
  
class ActionValidity(Action):
    def name(self):
        return "action_validity"
    def run(self, dispatcher, tracker, domain):
        validity_count = tracker.get_slot("validity_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")

        if validity_count <=2:      
            template_name =  "utter_FAQ_validity_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Validity",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("validity_count", validity_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)  
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
  
class ActionSettlement(Action):
    def name(self):
        return "action_settlement"
    def run(self, dispatcher, tracker, domain):
        settlement_count = tracker.get_slot("settlement_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")
        
        if settlement_count <=2:         
            template_name =  "utter_FAQ_settelment_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker,customer_care_number = customer_care_number)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Claim Process",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("settlement_count", settlement_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)  
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
  
class ActionHealthInsurance(Action):
    def name(self):
        return "action_health_insurance"
    def run(self, dispatcher, tracker, domain):
        health_insurance_count = tracker.get_slot("health_insurance_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")

        if health_insurance_count <=6:         
            template_name =  "utter_FAQ_other_insurance_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker,customer_care_number=customer_care_number)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask Other Insurance",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("health_insurance_count", health_insurance_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)  
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]

class ActionInsuranceInfo(Action):
    def name(self):
        return "action_insurance_info"
    def run(self, dispatcher, tracker, domain):
        insurance_info_count = tracker.get_slot("insurance_info_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number = tracker.get_slot("customer_care_number")
        emi_amount = tracker.get_slot("emi_amount")
        customer_care_number = tracker.get_slot("customer_care_number")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
        flow_type = tracker.get_slot("flow_type")

        if insurance_info_count <=2:         
            template_name =  "utter_FAQ_insurance_info_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)
            send_and_store_disposition_details(
                tracker=tracker,
                dispatcher=dispatcher,
                disposition_id="Ask  Insurance Info",
                flag=DEFAULT_FLAG,  
            )
            return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
            SlotSet("insurance_info_count", insurance_info_count+1),
        ]
        else:
            template_name =  "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
            dispatcher.utter_template(template_name,tracker)  
            send_and_store_disposition_details(
                tracker=tracker,
                flag=TIMEOUT_FLAG,
                dispatcher=dispatcher,
                disposition_id="Others"
            )
            return [FollowupAction("action_listen")]
  
class ActionInitialMessage(Action):
    def name(self):
        return "action_initial_message"

    def run(self, dispatcher, tracker, domain):
        
        customer_details = get_user_details(tracker)
        threshold_time = customer_details["threshold_time"]
        customer_language = customer_details["language"]
        flow_type = customer_details["flow_type"]
        customer_name = customer_details["employee_name"]
        client_name = customer_details["utter_client_name_slot"]
        client_name = client_name.replace(" Testing","")
        agent_name = customer_details["agent_name"]
        threshold_days = customer_details["threshold_days"]
        supported_lang = customer_details["supported_languages"]
        sender_id = tracker.sender_id
        red_lang.set(str(sender_id)+"supported_languages",str(supported_lang))
        customer_care_number = customer_details["customerCareNumber"]
        expiry_date = customer_details["expiry_date"]
        vehicle_detail = customer_details["vehicle_detail"]
        gender = customer_details["gender"]
        accountName = customer_details["accountName"]
        product = customer_details["product"]
        variation = customer_details["variation"]
        product_category = customer_details["product_category"]
        insurance_product = customer_details["insurance_product"]
        policy_name=tracker.get_slot=tracker.get_slot("policy_name")
        
        account_name = str(accountName)+"_"+str(product)+"_"+str(product_category)
        
        
        if gender == "F":
            bot_gender = "M_" + str(account_name)
        else:
            bot_gender = "F_" + str(account_name)
        
        
        if variation == "v1" or variation == "":
            variation = ""
        else:
            variation = variation + "_"
        
        
        
        if flow_type == "insurance_renewal":          
            return [
                FollowupAction("lg_rpc_form"),
                SlotSet("customer_name", str(customer_name)),
                SlotSet("client_name_slot", str(client_name)),
                SlotSet("agent_name", str(agent_name)),
                SlotSet("vehicle_detail", str(vehicle_detail)),
                SlotSet("insurance_product", str(insurance_product)),
                SlotSet("expiry_date", str(expiry_date)),
                SlotSet("policy_name", str(policy_name)),
                SlotSet("product", str(product)),
                SlotSet("product_category", str(product_category)),
                SlotSet("flow_type", str(flow_type)),
                SlotSet("supported_languages", str(supported_lang)),
                SlotSet("threshold_days_slot", str(threshold_days)),
                SlotSet("threshold_time_slot",str(threshold_time)),
                SlotSet("bot_gender",bot_gender),
                SlotSet("variation",variation),   
                SlotSet("customer_care_number",customer_care_number),
                SlotSet("nlu_data_list", []),
                SlotSet("audio_server", "True"),
                SlotSet("cust_lang", customer_language),
            ] 