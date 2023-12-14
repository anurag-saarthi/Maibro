from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class RPCForm(FormAction):
    def name(self):  
        return "lg_rpc_form" 

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        stop_conversation = tracker.get_slot("stop_conversation")
        name_confirmation = tracker.get_slot("name_confirmation")
        third_party_cont = tracker.get_slot("third_party_cont")
        customer_availability = tracker.get_slot("customer_availability")
        customer_availability_2 = tracker.get_slot("customer_availability_2")

        
        
        if stop_conversation == "TRUE":
            return []
        if customer_availability_2 == "customer_availability":
            return ["customer_availability"]
        if customer_availability == "customer_availability_2":
            return ["customer_availability_2"]
        if third_party_cont == "customer_availability_2":
            return ["customer_availability_2"]
        if third_party_cont == "customer_availability":
            return["customer_availability"]
        if name_confirmation=="third_party_cont":
            return["third_party_cont"]
        return["name_confirmation"] 


    def slot_mappings(self):  
        return {
            "name_confirmation": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),
            ],
            "third_party_cont": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),
                self.from_intent(intent="wait", value="TRUE"),
            ],
            "customer_availability": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),
                self.from_intent(intent="no_message", value="no_message"),
                self.from_intent(intent="wait", value="TRUE"),
            ],
            "customer_availability_2": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),
                self.from_intent(intent="no_message", value="no_message"),
                # self.from_intent(intent="wait", value="TRUE"),
            ],
        }


    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        print("imhererpc")
        return tracker.get_slot(slot_name) is None

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                trail_count = tracker.get_slot("trail_count")
                disposition_name = tracker.get_slot("disposition_name_slot")
                customer_name = tracker.get_slot("customer_name")
                client_name = tracker.get_slot("client_name_slot")
                agent_name = tracker.get_slot("agent_name")
                entities = tracker.latest_message["entities"]
                supported_languages =tracker.get_slot("supported_languages")
                nlu_data_list =tracker.get_slot("nlu_data_list")
                changing_slot = tracker.get_slot("changing_slot")
                flow_type = tracker.get_slot("flow_type")
                intent = tracker.latest_message.get("intent").get("name")
                trail_count_rpc=tracker.get_slot("trail_count_rpc")
                trail_count_third_party_cont=tracker.get_slot("trail_count_third_party_cont")
                customer_availability_count=tracker.get_slot("customer_availability_count")
                trail_count_name_confirmation=tracker.get_slot("trail_count_name_confirmation")
                trail_count_customer_availability_two=tracker.get_slot("trail_count_customer_availability_two")
                bot_gender=tracker.get_slot("bot_gender")
                variation=tracker.get_slot("variation")
                insurance_product=tracker.get_slot("insurance_product")
                
                if trail_count_name_confirmation <=2 and slot == "name_confirmation":
                    if trail_count == 0:
                        template_name =  (
                            "utter_slot_0_RPC_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name,insurance_product = insurance_product,agent_name=agent_name,client_name=client_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial_message")
                    else:
                        template_name =  (
                            "utter_slot_0_RPC_alt_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name,insurance_product = insurance_product,agent_name=agent_name,client_name=client_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="initial_message")
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("came_from_form_slot","lq_rpc_form"),
                        SlotSet("current_main_slot",slot),SlotSet("trail_count_name_confirmation",trail_count_name_confirmation+1)]   

                
                if trail_count_third_party_cont <=2 and slot == "third_party_cont":
                    if trail_count is None or trail_count == 0 :
                        trail_count = 0 
                        template_name =  (
                            "utter_deny_general_ask_inform_busy_third_party_affirm_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact",right_party_contact = "No")
                    else:
                        template_name =  (
                            "utter_deny_general_ask_inform_busy_third_party_affirm_alt_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact",right_party_contact = "No")
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("came_from_form_slot","lq_rpc_form"),
                        SlotSet("current_main_slot",slot),SlotSet("trail_count_third_party_cont",trail_count_third_party_cont+1)]   

                
                if customer_availability_count <=2 and slot == "customer_availability":
                    if trail_count is None or trail_count == 0:
                        trail_count = 0 
                        template_name =  (
                            "utter_customer_not_available_general_ask_inform_busy_third_party_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact",right_party_contact = "No")
                    else:
                        template_name =  (
                            "utter_customer_not_available_general_ask_inform_busy_third_party_alt_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact",right_party_contact = "No")

                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("came_from_form_slot","lq_rpc_form"),
                        SlotSet("current_main_slot",slot),SlotSet("customer_availability_count",customer_availability_count+1)]   

                
                if trail_count_customer_availability_two <= 2 and slot == "customer_availability_2":
                    if trail_count is None or trail_count == 0:
                        trail_count = 0 
                        template_name =  (
                            "utter_affirm_wait_general_chat_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact",right_party_contact = "No")
                    else:
                        template_name =  (
                            "utter_affirm_wait_general_chat_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact",right_party_contact = "No")
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                        SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("came_from_form_slot","lq_rpc_form"),
                        SlotSet("current_main_slot",slot),SlotSet("trail_count_customer_availability_two",trail_count_customer_availability_two+1)]   
                else:
                    template_name =  (
                            "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
                        )
                    dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG)
                    return {"third_party_cont":"filled","stop_conversation": "TRUE"}

    @staticmethod
    def validate_name_confirmation(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        if value == "TRUE":
            intent = tracker.latest_message.get("intent").get("name")
            sub_intent = tracker.latest_message.get("sub_intent").get("name")
            Humiliate = tracker.latest_message.get("Humiliate").get("name")
            sub_context = tracker.latest_message.get("sub_context").get("name")
            reasons_for_not_renewing = tracker.latest_message.get("reasons_for_not_renewing").get("name")
            sentiment = tracker.latest_message.get("sentiment").get("name")
            context = tracker.latest_message.get("context").get("name")
            third_person = tracker.latest_message.get("third_person").get("name")
            signal = tracker.latest_message.get("signal").get("name")
            threshold_days = tracker.get_slot("threshold_days_slot")
            threshold_time = tracker.get_slot("threshold_time_slot")
            contact_no = tracker.get_slot("contact_no")
            entities = tracker.latest_message["entities"]
            user_message = tracker.latest_message.get("text")
            flow_type = tracker.get_slot("flow_type")
            trail_count = tracker.get_slot("trail_count")
            out_of_context_count = tracker.get_slot("out_of_context_count_slot")  
            print("third_person------------->",third_person)
            reasons_for_not_renewing = tracker.latest_message.get("reasons_for_not_renewing").get("name")
            customer_name = tracker.get_slot("customer_name")
            client_name = tracker.get_slot("client_name_slot")
            agent_name = tracker.get_slot("agent_name")
            bot_gender=tracker.get_slot("bot_gender")
            variation=tracker.get_slot("variation")
            insurance_product=tracker.get_slot("insurance_product")
            policy_name=tracker.get_slot=tracker.get_slot("policy_name")
            expiry_date=tracker.get_slot=tracker.get_slot("expiry_date")

            if signal=="wrong_number":
                template_name =  (
                                "utter_deny_wrong_number_" + variation + flow_type + "_static_" + bot_gender
                            )
                dispatcher.utter_template(template_name,tracker,policy_name=policy_name,customer_name=customer_name,expiry_date=expiry_date) 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Wrong Number", right_party_contact = "No")
                return {"name_confirmation":value,"stop_conversation":"TRUE"}
            
            if signal=="wrong_name":
                template_name =  (
                            "utter_deny_wrong_name_" + variation + flow_type + "_static_" + bot_gender
                        )
                dispatcher.utter_template(template_name,tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Deny - Wrong Name", right_party_contact = "Yes")
                return {"name_confirmation": value,"go_to_form_slot":"rpc_true","stop_conversation": "TRUE"}
            
            if ((sub_intent == "affirm" or sub_intent == "general_ask_inform") and (signal == "continue_call" or signal == "general_chat" or signal == "continue_call") ) or signal == "continue_call":
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=DEFAULT_FLAG,disposition_id="Right Party Contact",right_party_contact = "Yes")
                return {"go_to_form_slot":"rpc_true","stop_conversation":"TRUE"}

            if  sub_intent == "deny" or third_person=="yes":
                if flow_type == "insurance_renewal":
                    template_name =  (
                                "utter_deny_wrong_number_" + variation + flow_type + "_static_" + bot_gender
                            )
                    dispatcher.utter_template(template_name,tracker,policy_name=policy_name,customer_name=customer_name,expiry_date=expiry_date) 
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Third Party Contact")
                    return {"name_confirmation":value,"stop_conversation":"TRUE"}
                else:
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Third Party Contact")
                    return {"name_confirmation": "third_party_cont","trail_count":None}
            
            if ((signal == "timings" or signal == "bot_call_later") and (sub_intent == "affirm" or sub_intent == "general_ask_inform" ) and (sub_context == "future_bot_action" or sub_context == "action_by_customer" or sub_context == "general" or sub_context == "action_by_bot")): 
 
                if entities:
                    for entity in entities:
                        print("entity",entity)
                        if entity.get("entity", None) == "date":
                            date_value=entity["value"]
                            for entity_again in entities:
                                print("entity_again",entity_again)
                                if entity_again.get("entity", None) == "time":
                                    time_entity=entity_again["value"]
                                    template_name =  (
                                                "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                                            )
                                    dispatcher.utter_template(template_name,tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=date_value + " "+ time_entity)
                                    return {"name_confirmation": value,"stop_conversation":"TRUE"}
                        else:
                            template_name =  (
                                                "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                                            )
                            dispatcher.utter_template(template_name,tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=date_value)
                            return {"name_confirmation": value,"stop_conversation":"TRUE"}

                else:
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Callback Time Not Given",)
                    return {"go_to_form_slot":"call_back_form","stop_conversation":"TRUE", "callback_alt":True}


            if signal == "busy":
                print("went_to_callback")
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Callback Time Not Given",)
                return {"go_to_form_slot":"call_back_form","stop_conversation":"TRUE"}

            else:
                return {"name_confirmation":None}
        else:
            return {"name_confirmation":None}


    @staticmethod
    def validate_third_party_cont(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        if value == "TRUE":
            intent = tracker.latest_message.get("intent").get("name")
            sub_intent = tracker.latest_message.get("sub_intent").get("name")
            Humiliate = tracker.latest_message.get("Humiliate").get("name")
            sub_context = tracker.latest_message.get("sub_context").get("name")
            reasons_for_not_renewing = tracker.latest_message.get("reasons_for_not_renewing").get("name")
            sentiment = tracker.latest_message.get("sentiment").get("name")
            context = tracker.latest_message.get("context").get("name")
            third_person = tracker.latest_message.get("third_person").get("name")
            signal = tracker.latest_message.get("signal").get("name")
            threshold_days = tracker.get_slot("threshold_days_slot")
            threshold_time = tracker.get_slot("threshold_time_slot")
            contact_no = tracker.get_slot("contact_no")
            entities = tracker.latest_message["entities"]
            user_message = tracker.latest_message.get("text")
            flow_type = tracker.get_slot("flow_type")
            trail_count = tracker.get_slot("trail_count")
            out_of_context_count = tracker.get_slot("out_of_context_count_slot")  
            callback_alt = tracker.get_slot("callback_alt")
            customer_name = tracker.get_slot("customer_name")
            client_name = tracker.get_slot("client_name_slot")
            agent_name = tracker.get_slot("agent_name")
            bot_gender=tracker.get_slot("bot_gender")
            variation=tracker.get_slot("variation")
            insurance_product=tracker.get_slot("insurance_product")
            
            if signal=="wrong_number":
                template_name =  (
                            "utter_deny_wrong_number_" + variation + flow_type + "_static_" + bot_gender
                        )
                dispatcher.utter_template(template_name,tracker) 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Wrong Number")
                return {"name_confirmation":value,"stop_conversation":"TRUE"}
            
            # go to Am I speaking to {customer_name}?
            # Agree/affirm+Wait Intent, Customer_reply > 5sec
            if sub_intent=="wait" or sub_intent=="affirm": 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Third Party Contact")
                return {"third_party_cont": "customer_availability_2","trail_count":None}
            
            if (sub_intent=="deny" or sub_intent == "general_ask_inform") and (signal == "busy" or signal == "general_chat") and (third_person == "yes"): 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Third Party Contact")
                return {"third_party_cont": "customer_availability","trail_count":None}
            
            if sub_intent == "deny":
                template_name =  (
                            "utter_deny_general_chat_third_party_" + variation + flow_type + "_static_" + bot_gender
                        )
                dispatcher.utter_template(template_name,tracker,customer_name = customer_name) 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Third Party Contact")
                return {"name_confirmation":value,"stop_conversation":"TRUE"}
            
            if (sub_intent == "affirm" or sub_intent=="general_ask_inform") and (signal == "continue_call" or signal == "general_chat"):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=DEFAULT_FLAG, disposition_id="Third Party Contact")
                return {"third_party_cont": "customer_availability","trail_count":None}
            
            if  signal == "busy":
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Third Party Contact")
                return {"go_to_form_slot":"call_back","callback_alt":True,"stop_conversation":"TRUE"}
            
            #call_back
            if ((signal == "timings" or signal == "bot_call_later" ) and (sub_intent == "affirm" or sub_intent == "general_ask_inform" ) and (sub_context == "future_bot_action" or sub_context == "action_by_customer" or sub_context == "general" or sub_context == "action_by_bot")): 
 
                if entities:
                    for entity in entities:
                        print("entity",entity)
                        if entity.get("entity", None) == "date":
                            date_value=entity["value"]
                            for entity_again in entities:
                                print("entity_again",entity_again)
                                if entity_again.get("entity", None) == "time":
                                    time_entity=entity_again["value"]
                                    template_name =  (
                                                "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                                            )
                                    dispatcher.utter_template(template_name,tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=date_value + " "+ time_entity)
                                    return {"third_party_cont": value,"stop_conversation":"TRUE"}
                        else:
                            template_name =  (
                                                "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                                            )
                            dispatcher.utter_template(template_name,tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=date_value)
                            return {"third_party_cont": value,"stop_conversation":"TRUE"}

                else:
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Callback Time Not Given",)
                    return {"go_to_form_slot":"call_back_form","stop_conversation":"TRUE", "callback_alt":True}

            else:
                return {"third_party_cont": None}           
        else:
                return {"third_party_cont": None}
            
            

    @staticmethod
    def validate_customer_availability(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("inrpc")
        print("value in 357",value)
        if value == "TRUE":
            intent = tracker.latest_message.get("intent").get("name")
            sub_intent = tracker.latest_message.get("sub_intent").get("name")
            Humiliate = tracker.latest_message.get("Humiliate").get("name")
            sub_context = tracker.latest_message.get("sub_context").get("name")
            reasons_for_not_renewing = tracker.latest_message.get("reasons_for_not_renewing").get("name")
            sentiment = tracker.latest_message.get("sentiment").get("name")
            context = tracker.latest_message.get("context").get("name")
            third_person = tracker.latest_message.get("third_person").get("name")
            signal = tracker.latest_message.get("signal").get("name")
            threshold_days = tracker.get_slot("threshold_days_slot")
            threshold_time = tracker.get_slot("threshold_time_slot")
            contact_no = tracker.get_slot("contact_no")
            entities = tracker.latest_message["entities"]
            user_message = tracker.latest_message.get("text")
            flow_type = tracker.get_slot("flow_type")
            trail_count = tracker.get_slot("trail_count")
            out_of_context_count = tracker.get_slot("out_of_context_count_slot")  
            callback_alt = tracker.get_slot("callback_alt")
            customer_name = tracker.get_slot("customer_name")
            client_name = tracker.get_slot("client_name_slot")
            agent_name = tracker.get_slot("agent_name")
            bot_gender=tracker.get_slot("bot_gender")
            variation=tracker.get_slot("variation")
            insurance_product=tracker.get_slot("insurance_product")

            if entities:
                for entity in entities:
                    if entity.get("entity", None) == "date" or entity.get("entity", None) == "time":
                        time_date=entity["value"]
                        template_name =  (
                            "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                            )
                        dispatcher.utter_template(template_name,tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=time_date)
                        return {"customer_availability": value,"stop_conversation":"TRUE"}
                    else:
                        template_name =  (
                                        "utter_date_time_not_given_general_chat_" + variation + flow_type + "_static_" + bot_gender
                                    )
                        dispatcher.utter_template(template_name,tracker)
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Not Given",)
                        return {"customer_availability": value,"stop_conversation":"TRUE"}
            else:
                template_name =  (
                                "utter_date_time_not_given_general_chat_" + variation + flow_type + "_static_" + bot_gender
                            )
                dispatcher.utter_template(template_name,tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Not Given",)
                return {"customer_availability": value,"stop_conversation":"TRUE"}
                
            return {"customer_availability": None}
   
      
        else:
            return {"customer_availability": None}
        
    @staticmethod
    def validate_customer_availability_2(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        if value == "TRUE":
            intent = tracker.latest_message.get("intent").get("name")
            sub_intent = tracker.latest_message.get("sub_intent").get("name")
            Humiliate = tracker.latest_message.get("Humiliate").get("name")
            sub_context = tracker.latest_message.get("sub_context").get("name")
            reasons_for_not_renewing = tracker.latest_message.get("reasons_for_not_renewing").get("name")
            sentiment = tracker.latest_message.get("sentiment").get("name")
            context = tracker.latest_message.get("context").get("name")
            third_person = tracker.latest_message.get("third_person").get("name")
            signal = tracker.latest_message.get("signal").get("name")
            threshold_days = tracker.get_slot("threshold_days_slot")
            threshold_time = tracker.get_slot("threshold_time_slot")
            contact_no = tracker.get_slot("contact_no")
            entities = tracker.latest_message["entities"]
            user_message = tracker.latest_message.get("text")
            flow_type = tracker.get_slot("flow_type")
            trail_count = tracker.get_slot("trail_count")
            out_of_context_count = tracker.get_slot("out_of_context_count_slot")  
            callback_alt = tracker.get_slot("callback_alt")
            customer_name = tracker.get_slot("customer_name")
            client_name = tracker.get_slot("client_name_slot")
            agent_name = tracker.get_slot("agent_name")
            bot_gender=tracker.get_slot("bot_gender")
            variation=tracker.get_slot("variation")
            insurance_product=tracker.get_slot("insurance_product")

            if ((sub_intent == "affirm" or sub_intent == "general_ask_inform") and (signal == "continue_call" or signal == "general_chat" or signal == "continue_call") ) or signal == "continue_call":
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=DEFAULT_FLAG,disposition_id="Right Party Contact",right_party_contact = "Yes")
                return {"go_to_form_slot":"rpc_true","stop_conversation":"TRUE"}

            if  signal == "busy":
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Wrong Party Contact")
                return {"go_to_form_slot":"call_back","callback_alt":True,"stop_conversation":"TRUE"}
            
            #call_back
            if ((signal == "timings" or signal == "bot_call_later" ) and (sub_intent == "affirm" or sub_intent == "general_ask_inform" ) and (sub_context == "future_bot_action" or sub_context == "action_by_customer" or sub_context == "general" or sub_context == "action_by_bot")): 
 
                if entities:
                    for entity in entities:
                        print("entity",entity)
                        if entity.get("entity", None) == "date":
                            date_value=entity["value"]
                            for entity_again in entities:
                                print("entity_again",entity_again)
                                if entity_again.get("entity", None) == "time":
                                    time_entity=entity_again["value"]
                                    template_name =  (
                                                "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                                            )
                                    dispatcher.utter_template(template_name,tracker)
                                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=date_value + " "+ time_entity)
                                    return {"customer_availability_2": value,"stop_conversation":"TRUE"}
                        else:
                            template_name =  (
                                                "utter_callback_date_time_given_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                                            )
                            dispatcher.utter_template(template_name,tracker)
                            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id= "Callback Time Given",callback_time=date_value)
                            return {"customer_availability_2": value,"stop_conversation":"TRUE"}

                else:
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Callback Time Not Given",)
                    return {"go_to_form_slot":"call_back_form","stop_conversation":"TRUE", "callback_alt":True}

            #out of context
            if (sub_intent == "deny" or signal == "general_chat"):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher, flag=DEFAULT_FLAG,disposition_id="Right Party Contact",right_party_contact = "Yes")
                return {"customer_availability_2":"customer_availability","trail_count":None}

            return {"customer_availability_2": None}        
        else:     
                return {"customer_availability_2": None}
        


    def submit(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        go_to_form_slot = tracker.get_slot("go_to_form_slot")
        flow_data = tracker.get_slot("flow_data_slot")
        flow_list = tracker.get_slot("flow_list_slot")
        disposition = tracker.get_slot("disposition_slot")
        number_given =tracker.get_slot("number_given")
        callback_alt = tracker.get_slot("callback_alt")
        
        if go_to_form_slot == "call_back_form" or go_to_form_slot == "callback" or go_to_form_slot=="call_back" :
            return [FollowupAction("call_back_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("stop_conversation",None),SlotSet("go_to_form_slot",None),SlotSet("nlu_data_list",None),SlotSet("trail_count_rpc",None),SlotSet("callback_alt",callback_alt)]  # SlotSet("go_to_form_slot",None),
        elif go_to_form_slot == "rpc_true":
            return [FollowupAction("sales_pitch_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("stop_conversation",None),SlotSet("go_to_form_slot",None),SlotSet("flow_list_slot",flow_list),SlotSet("out_of_context_count_slot",0),SlotSet("trail_count_rpc",None),SlotSet("sales_pitching",None),SlotSet("rpc_slot","true")]
        return [FollowupAction("action_listen"), AllSlotsReset()] 