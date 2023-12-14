from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class LaterDateForm(FormAction):
    def name(self):  # type: () -> Text
        return "interested_renew_form" 
    print("In interested_renew_form")    

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("innnslot")
        stop_conversation = tracker.get_slot("stop_conversation")
        interested_renew = tracker.get_slot("interested_renew")
        

        if stop_conversation == "TRUE":
            return []
        return["interested_renew"]

    def slot_mappings(self):  
        return {
            "interested_renew": [
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
                trail_count_interested_renew=tracker.get_slot("trail_count_interested_renew")
                callback_alt = tracker.get_slot("callback_alt")
                interested_renew = tracker.get_slot("interested_renew")
                flow_type = tracker.get_slot("flow_type")
                bot_gender=tracker.get_slot("bot_gender")
                variation=tracker.get_slot("variation")
                insurance_product=tracker.get_slot("insurance_product")
                customer_care_number = tracker.get_slot("customer_care_number")
        
        
                if trail_count_interested_renew <=2:

                    if trail_count is None or trail_count == 0:  
                        trail_count = 0
                        template_name =  (
                            "utter_affirm_interested_renew_general_chat_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,toll_free_numeber = customer_care_number) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag= DEFAULT_FLAG)
                    else: 
                        template_name =  (
                            "utter_affirm_interested_renew_general_chat_" + variation + flow_type + "_static_" + bot_gender
                        )
                        dispatcher.utter_template(template_name,tracker,toll_free_numeber = customer_care_number) 
                        send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag= DEFAULT_FLAG)
                    
                   
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                            SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),
                            SlotSet("trail_count_interested_renew",trail_count_interested_renew+1)]
                  
                else:
                    template_name =  (
                            "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
                        )
                    dispatcher.utter_template(template_name,tracker,toll_free_numeber = customer_care_number) 
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG,disposition_id="intent repeat")
                    return {"interested_renew":"filled","stop_conversation": "TRUE"}

    @staticmethod
    def validate_interested_renew(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("in_validate_interested_renew")
        if value == "TRUE":
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
            rpc_slot=tracker.get_slot("rpc_slot")
            interested_renew = tracker.get_slot("interested_renew")

            return {"interested_renew":value,"stop_conversation":"TRUE"} 

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
        
        return [FollowupAction("action_listen"), AllSlotsReset()] 
      