from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class LaterDateForm(FormAction):
    def name(self):  # type: () -> Text
        return "call_back_form" 
    print("In_callback_form1")    

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("inslot1")
        stop_conversation = tracker.get_slot("stop_conversation")
        future_date = tracker.get_slot("future_date")

        if stop_conversation == "TRUE":
            return []
        return["future_date"] 

    def slot_mappings(self):  
        return {
            "future_date": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),  
            ]  
        }
            

    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        print("imincallback")
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
                emp_name = tracker.get_slot("customer_name")
                website = tracker.get_slot("website_name_slot")
                client_name = tracker.get_slot("client_name_slot")
                template_structure = tracker.get_slot("template_structure")
                trail_count_future_date=tracker.get_slot("trail_count_future_date")
                callback_alt = tracker.get_slot("callback_alt")
                flow_type = tracker.get_slot("flow_type")
                intent = tracker.latest_message.get("intent").get("name")
                template_structure = tracker.get_slot("template_structure")
                bot_gender=tracker.get_slot("bot_gender")
                variation=tracker.get_slot("variation")
                insurance_product=tracker.get_slot("insurance_product")
                
        
                busy_template = "utter_busy_right_party_callback_later_"+ variation + flow_type+"_static_"+ bot_gender
                busy_alt_template = "utter_busy_right_party_callback_later_alt_"+ variation + flow_type+"_static_"+ bot_gender
                if trail_count_future_date <=2:
                    if slot == "future_date":
                        if trail_count is None:  
                            trail_count = 0
                            if callback_alt==True:
                                
                                dispatcher.utter_template(busy_template,tracker) 
                                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Callback Time Not Given")     
                            else:    
                                dispatcher.utter_template(busy_alt_template,tracker) 
                                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Callback Time Not Given")
                        else:
                            if callback_alt==True:
                                dispatcher.utter_template(busy_template,tracker,customer_name=emp_name) 
                                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Third Party Contact")     
                            else: 
                                dispatcher.utter_template(busy_alt_template,tracker)
                                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Callback Time Not Given")
                    
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                            SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),
                            SlotSet("trail_count_future_date",trail_count_future_date+1)]
                else:
                    dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="intent repeat")
                    return {"future_date":"filled","stop_conversation": "TRUE"}

    @staticmethod
    def validate_future_date(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("in_validate_future_date")
        if value == "TRUE":
            print("entering_into_future_dte")
            intent = tracker.latest_message.get("intent").get("name")
            sub_intent = tracker.latest_message.get("sub_intent").get("name")
            Humiliate = tracker.latest_message.get("Humiliate").get("name")
            sub_context = tracker.latest_message.get("sub_context").get("name")
            delay_reason = tracker.latest_message.get("delay_reason").get("name")
            sentiment = tracker.latest_message.get("sentiment").get("name")
            context = tracker.latest_message.get("context").get("name")
            third_person = tracker.latest_message.get("third_person").get("name")
            signal = tracker.latest_message.get("signal").get("name")
            threshold_days = tracker.get_slot("threshold_days_slot")
            threshold_time_slot = tracker.get_slot("threshold_time_slot")
            contact_no = tracker.get_slot("contact_no")
            entities = tracker.latest_message["entities"]
            flow_type=tracker.get_slot("flow_type")
            user_message = tracker.latest_message.get("text")
            threshold_days = tracker.get_slot("threshold_days_slot")
            threshold_time = tracker.get_slot("threshold_time_slot")
            template_structure = tracker.get_slot("template_structure")
            rpc_slot=tracker.get_slot("rpc_slot")
            bot_gender=tracker.get_slot("bot_gender")
            variation=tracker.get_slot("variation")

            # if signal == "call" and sub_context == "action_by_bot":
            #     send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested",flag=DEFAULT_FLAG,)
            #     return {"go_to_form_slot":"continue","stop_conversation":"TRUE"}
            # if signal == "call" and sub_context == "action_by_bot":
            #     send_and_store_disposition_details(
            #     tracker=tracker, dispatcher=dispatcher, flag=DEFAULT_FLAG,disposition_id="Product Information Conveyed",right_party_contact = "Yes")
            #     return {"go_to_form_slot":"rpc_true","stop_conversation":"TRUE"}
            time_given_template = "utter_callback_date_time_given_bot_call_later_"+ variation + flow_type+ "_static_"+ bot_gender 
            time_not_given_template = "utter_interested_later_general_chat_renew_date_not_given_"+ variation + flow_type+"_static_"+ bot_gender
            if entities:
                for entity in entities:
                    if entity.get("entity", None) == "date":
                        time_date=entity["value"]
                        given_date,callback_date_1 = given_date_function(time_date)
                        date = date_value(given_date)
                        for entity_again in entities:
                            if entity_again.get("entity", None) == "time":
                                time_entity=entity_again["value"]
                                given_time = get_time(entity_again["value"])
                                if date == "today":
                                    dispatcher.utter_template(time_given_template,tracker) # callback_date =given_date, callback_time= given_time
                                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Given",callback_time=time_date + " "+ time_entity)
                                    return {"future_date":value,"stop_conversation":"TRUE"} 
                                elif date == "true":
                                    dispatcher.utter_template(time_given_template,tracker) # callback_date =given_date, callback_time= given_time
                                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Given",callback_time=time_date + " "+ time_entity)
                                    return {"future_date":value,"stop_conversation":"TRUE"}
                                else:
                                    dispatcher.utter_template(time_given_template,tracker)
                                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Given")
                                    return {"future_date":value,"stop_conversation":"TRUE"} 
                                    
                        if date=="previous":
                            # dispatcher.utter_template("utter_RPC_right_party_time_date_not_given_"+template_structure,tracker) # Only callback_date ----------------->
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Callback Time Given")
                            return {"future_date":None}
                        
                        elif date == "true" or date == "today":
                            dispatcher.utter_template(time_given_template,tracker) # Only callback_date ----------------->
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Given",callback_time=time_date)
                            return {"future_date":value,"stop_conversation": "TRUE"}
                        else:
                            dispatcher.utter_template(time_given_template,tracker)
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Given",callback_time=time_date)
                            return {"future_date":value,"stop_conversation":"TRUE"} 
                    else:
                        dispatcher.utter_template(time_given_template,tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Not Given")
                        return {"future_date":value,"stop_conversation":"TRUE"} 
            else:
                dispatcher.utter_template(time_not_given_template,tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Not Given")
                return {"future_date":value,"stop_conversation":"TRUE"} 

    def submit(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any] 
) -> List[EventType]:
        go_to_form_slot = tracker.get_slot("go_to_form_slot")
        came_from_form = tracker.get_slot("came_from_form_slot")
        flow_data = tracker.get_slot("flow_data_slot")
        disposition = tracker.get_slot("disposition_slot")
        print("in callback_submit")
        # if go_to_form_slot == "continue":
        #     return [FollowupAction(came_from_form), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",1),SlotSet("stop_conversation",None),SlotSet("go_to_form_slot",None),SlotSet("out_of_context_count_slot",0),SlotSet("nlu_data_list",None)]
        # if go_to_form_slot == "rpc_true":
        #     return [FollowupAction("sales_pitch_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("stop_conversation",None),SlotSet("go_to_form_slot",None),SlotSet("nlu_data_list",None),SlotSet("trail_count_rpc",None)]
        return [FollowupAction("action_listen"), AllSlotsReset()] 
      