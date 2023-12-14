from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class SalesPitchForm(FormAction):
    def name(self):  # type: () -> Text
        return "sales_pitch_form" # return "maia_pre_emi_male"
    print("In sales_pitch_form")    

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("innnslot")
        stop_conversation = tracker.get_slot("stop_conversation")
        sales_pitching = tracker.get_slot("sales_pitching")

        if stop_conversation == "TRUE":
            return []

        return["sales_pitching"] 


    def slot_mappings(self):  
        return {
            "sales_pitching": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),
            ]
        }
            

    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        print("imhere5")
        return tracker.get_slot(slot_name) is None

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                threshold_days = tracker.get_slot("threshold_days_slot")
                threshold_time = tracker.get_slot("threshold_time_slot")
                contact_no = tracker.get_slot("contact_no")
                entities = tracker.latest_message["entities"]
                user_message = tracker.latest_message.get("text")
                flow_type = tracker.get_slot("flow_type")
                trail_count = tracker.get_slot("trail_count")
                out_of_context_count = tracker.get_slot("out_of_context_count_slot")  
                template_structure = tracker.get_slot("template_structure")
                sales_pitching_count = tracker.get_slot("sales_pitching_count")
                loan_amount = tracker.get_slot("loan_amount")
                credit_product = "personal loan"
                loan_availed_slot =tracker.get_slot("loan_availed_slot")
                loan_tenure = tracker.get_slot("loan_tenure")
                account_number = tracker.get_slot("account_number")
                account_number = account_number[-5:]
                client_name = tracker.get_slot("client_name_slot")
                vehicle_detail = tracker.get_slot("vehicle_detail")
                expiry_date = tracker.get_slot("expiry_date")
                bot_gender=tracker.get_slot("bot_gender")
                variation=tracker.get_slot("variation")
                insurance_product=tracker.get_slot("insurance_product")
                
                if sales_pitching_count<=4:
                    if slot == "sales_pitching":
                        print("sales_pitching_requested",trail_count)
                        if trail_count is None:
                            trail_count = 0
                            template_name =  (
                                "utter_slot_1_continue_call_main_response_" + variation + flow_type + "_static_" + bot_gender
                            )
                            dispatcher.utter_template(template_name,tracker,client_name = client_name,vehicle_detail = vehicle_detail,expiry_date=expiry_date) 
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Renewal Information Conveyed")
                        else:
                            template_name =  (
                                "utter_slot_1_continue_call_alt_response_" + variation + flow_type + "_static_" + bot_gender
                            )
                            dispatcher.utter_template(template_name,tracker,client_name = client_name,vehicle_detail = vehicle_detail,expiry_date=expiry_date)
                            send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Renewal Information Conveyed")
                        
                    print("haha")
                    return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot),
                            SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("current_main_slot",slot),
                            SlotSet("came_from_form_slot","sales_pitch_form"),SlotSet("sales_pitching_count",int(sales_pitching_count)+1)]
                else:
                    template_name =  (
                            "utter_G_bye_WC_" + variation + flow_type + "_static_" + bot_gender
                        )
                    dispatcher.utter_template(template_name,tracker) 
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Others",flag=TIMEOUT_FLAG)
                    
    @staticmethod
    def validate_sales_pitching(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("insales_pitch")
        print("entering_into_sales_pitch")
        intent = tracker.latest_message.get("intent").get("name")
        print(intent)
        sub_intent = tracker.latest_message.get("sub_intent").get("name")
        Humiliate = tracker.latest_message.get("Humiliate").get("name")
        sub_context = tracker.latest_message.get("sub_context").get("name")
        delay_reason = tracker.latest_message.get("delay_reason").get("name")
        sentiment = tracker.latest_message.get("sentiment").get("name")
        context = tracker.latest_message.get("context").get("name")
        third_person = tracker.latest_message.get("third_person").get("name")
        signal = tracker.latest_message.get("signal").get("name")
        threshold_days = tracker.get_slot("threshold_days_slot")
        threshold_time = tracker.get_slot("threshold_time_slot")
        flow_type = tracker.get_slot("flow_type")
        entities = tracker.latest_message["entities"]
        contact_no = tracker.get_slot("contact_no")
        trail_count = tracker.get_slot("trail_count")
        template_structure = tracker.get_slot("template_structure")
        customer_care_number= tracker.get_slot("customer_care_number") # add slot
        customer_care_email = tracker.get_slot("customer_care_email") # add slot
        client_name = tracker.get_slot("client_name_slot")
        vehicle_detail = tracker.get_slot("vehicle_detail")
        expiry_date = tracker.get_slot("expiry_date")
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
        insurance_product=tracker.get_slot("insurance_product")
            
        if value == "TRUE":
              
            if(sub_intent == "affirm" or sub_intent == "general_ask_inform") and (signal == "interested" or signal == "general_chat") and (context == "insurance_renewal" or context == "general") and (sub_context == "action_by_customer" or sub_context == "general"):
                # template_name =  ( "utter_affirm_interested_renew_general_chat_" + variation + flow_type + "_static_" + bot_gender)
                # dispatcher.utter_template(template_name,tracker,toll_free_numeber = customer_care_number) 
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag=TIMEOUT_FLAG,interest = "Yes")
                return {"go_to_form_slot":"interested_renew","stop_conversation": "TRUE"}
                # return {"sales_pitching":value,"stop_conversation":"TRUE"}

            if (sub_intent == "general_ask_inform" and signal == "already_renewed" and sub_context == "past_customer_action" and (context == " insurance_renewal" or context == "general")):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Insurance Already Renewed",flag=DEFAULT_FLAG,interest = "No")
                return {"go_to_form_slot":"already_renewed","stop_conversation":"TRUE"}

            if (sub_intent == "deny" and (signal == "interested" or signal == "general_chat") and sub_context == "action_by_customer" and (context == " insurance_renewal" or context == "general")):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Not Interested",flag=DEFAULT_FLAG,interest = "No")
                return {"go_to_form_slot":"renew_not_interested","stop_conversation":"TRUE"}

            if (sub_intent == "affirm" or sub_intent == "general_ask_inform") and context == "general" and (sub_context == "action_by_customer" or sub_context == "general") and (signal == "interested_later"):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Later",flag=DEFAULT_FLAG,interest = "Yes")
                return {"go_to_form_slot":"interested_later_form","stop_conversation":"TRUE"}
          
            if (sub_intent == "affirm" or sub_intent == "general_ask_inform") and context == "general" and (sub_context == "action_by_customer" or sub_context == "future_bot_action") and (signal == "timings" or signal == "bot_call_later"):
            #    Got it. We will get back to you. Have a nice day!
                template_name =  (
                            "utter_interested_later_timings_bot_call_later_" + variation + flow_type + "_static_" + bot_gender
                        )
                dispatcher.utter_template(template_name,tracker,client_name = client_name,vehicle_detail = vehicle_detail,expiry_date=expiry_date)                
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested - Later(time given)",flag=TIMEOUT_FLAG,interest = "Yes")
                return {"sales_pitching":value,"stop_conversation":"TRUE"}
            
            else:

                print("sales_pitch_else")
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,flag=DEFAULT_FLAG,disposition_id= "Out of Context")
                return {"sales_pitching": None,"trail_count":trail_count+1}
        else:
               return {"sales_pitching": None,"trail_count":trail_count + 1}
       
    def submit(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        print("Info submit sales pitch form")
        go_to_form = tracker.get_slot("go_to_form_slot")
        flow_data = tracker.get_slot("flow_data_slot")
        flow_list = tracker.get_slot("flow_list_slot")
        
        if go_to_form == "already_renewed":
            return [FollowupAction("already_renewed_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("go_to_form_slot",None),SlotSet("stop_conversation",None),SlotSet("call_back_form",None)]
        if go_to_form == "interested_renew":
           return [FollowupAction("interested_renew_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("go_to_form_slot",None),SlotSet("stop_conversation",None),SlotSet("call_back_form",None)]
        if go_to_form == "renew_not_interested":
            return [FollowupAction("renew_not_interested_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("go_to_form_slot",None),SlotSet("stop_conversation",None),SlotSet("call_back_form",None)]
        if go_to_form == "interested_later_form" :
            return [FollowupAction("interested_later_form"), SlotSet(REQUESTED_SLOT,None),SlotSet("trail_count",None),SlotSet("go_to_form_slot",None),SlotSet("stop_conversation",None),SlotSet("nlu_data_list",None)]
        return [FollowupAction("action_listen"), AllSlotsReset()] 
