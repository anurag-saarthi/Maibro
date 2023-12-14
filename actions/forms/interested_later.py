from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class LaterDateForm(FormAction):
    def name(self):  # type: () -> Text
        return "interested_later_form" 
    print("In interested_later_form")    

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("innnslot")
        stop_conversation = tracker.get_slot("stop_conversation")
        interested_later = tracker.get_slot("interested_later")
        

        if stop_conversation == "TRUE":
            return []
        return["interested_later"]

    def slot_mappings(self):  
        return {
            "interested_later": [
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
                trail_count_interested_later=tracker.get_slot("trail_count_interested_later")
                callback_alt = tracker.get_slot("callback_alt")
                interested_later = tracker.get_slot("interested_later")
                bot_gender=tracker.get_slot("bot_gender")
                variation=tracker.get_slot("variation")
                insurance_product=tracker.get_slot("insurance_product")
                flow_type = tracker.get_slot("flow_type")
                
        
        
                if trail_count_interested_later <=2:

                    if trail_count is None:  
                        trail_count = 0
                        # No Problem. When can I call you back?
                        template_name = (
                            "utter_interested_later_main_response_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Interested Later",flag= DEFAULT_FLAG)
                    else: 
                        template_name = (
                            "utter_interested_later_alt_response_" + variation + flow_type + "_static_" + bot_gender
                        )
                        # When can I get back to you for insurance renewal?
                        dispatcher.utter_template(template_name,tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Interested Later",flag=DEFAULT_FLAG)
                    
                   
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                            SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),
                            SlotSet("trail_count_interested_later",trail_count_interested_later+1)]
                  
                else:
                    dispatcher.utter_template("utter_G_bye_WC_"+template_structure,tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="intent repeat")
                    return {"interested_later":"filled","stop_conversation": "TRUE"}

    @staticmethod
    def validate_interested_later(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("in_validate_interested_later")
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
            interested_later = tracker.get_slot("interested_later")
            bot_gender = tracker.get_slot("interested_later")

            template_time_given = "utter_interested_later_bot_call_later_date_given_"+ flow_type + "_static_" + bot_gender
            template_time_not_given = "utter_interested_later_general_chat_renew_date_not_given_"+ flow_type + "_static_" + bot_gender
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
                                    # Renew Date Provided
                                    dispatcher.utter_template(template_time_given,tracker) # callback_date =given_date, callback_time= given_time
                                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later",callback_time=time_date + " "+ time_entity)
                                    return {"interested_later":value,"stop_conversation":"TRUE"} 
                                elif date == "true":
                                    # Renew Date Provided
                                    dispatcher.utter_template(template_time_given,tracker) # callback_date =given_date, callback_time= given_time
                                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later",callback_time=time_date + " "+ time_entity)
                                    return {"interested_later":value,"stop_conversation":"TRUE"}
                                else:
                                    # Renew Date Provided
                                    dispatcher.utter_template(template_time_given,tracker)
                                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later")
                                    return {"interested_later":value,"stop_conversation":"TRUE"} 
                                    
                        if date=="previous":
                            # dispatcher.utter_template("utter_RPC_right_party_time_date_not_given_"+template_structure,tracker) # Only callback_date ----------------->
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id="Callback Time Given")
                            return {"interested_later":None}
                        
                        elif date == "true" or date == "today":
                            dispatcher.utter_template(template_time_given,tracker) # Only callback_date ----------------->
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later",callback_time=time_date)
                            return {"interested_later":value,"stop_conversation": "TRUE"}
                        else:
                            dispatcher.utter_template(template_time_given,tracker)
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later",callback_time=time_date)
                            return {"interested_later":value,"stop_conversation":"TRUE"} 
                    else:
                        dispatcher.utter_template(template_time_not_given,tracker)
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later")
                        return {"interested_later":value,"stop_conversation":"TRUE"} 

            # elif (sub_intent == "general_ask_inform") and sub_context == "future_bot_action" and (signal == "timings" or signal == "bot_call_later"):
            #      # Renew Date Provided
            #     dispatcher.utter_template(template_time_given,tracker) # callback_date =given_date, callback_time= given_time
            #     send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Callback Time Given",callback_time=time_date + " "+ time_entity)
            #     return {"interested_later":value,"stop_conversation":"TRUE"}

            else:
                # Renew Date not given
                dispatcher.utter_template(template_time_not_given,tracker)
                send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="Interested - Later")
                return {"interested_later":value,"stop_conversation":"TRUE"} 

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
      