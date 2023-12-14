from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class SalesPitchForm(FormAction):
    def name(self):  # type: () -> Text
        return "renew_not_interested_form" # return "maia_pre_emi_male"
    print("In renew_not_interested form")    

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("innnslot")
        stop_conversation = tracker.get_slot("stop_conversation")
        renew_not_interested = tracker.get_slot("renew_not_interested")

        if stop_conversation == "TRUE":
            return []
        if renew_not_interested == "not_interested_reason":
            return["not_interested_reason"]
        
        return["renew_not_interested"] 


    def slot_mappings(self):  
        return {
            "renew_not_interested": [
                self.from_intent(intent="ask", value="TRUE"),
                self.from_intent(intent="inform", value="TRUE"),
            ],
            "not_interested_reason": [
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
                due_date = tracker.get_slot("due_date")
                due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y").strftime("%d %B %Y")
                credit_product = "personal loan"
                loan_availed_slot =tracker.get_slot("loan_availed_slot")
                nach = tracker.get_slot("nach")
                renew_not_interested = tracker.get_slot("renew_not_interested")
                not_interested_reason = tracker.get_slot("not_interested_reason")
                bot_gender = tracker.get_slot("bot_gender")

                
                # Tring to conveince not intrested customer
                if slot == "renew_not_interested":
                    template_name = "utter_affirm_insurance_insurance_renewal_interested_insurance_info_" + flow_type + "_static_" + bot_gender
                    dispatcher.utter_template(template_name,tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Not Interested")

                if slot == "not_interested_reason":
                    template_name = "utter_deny_insurance_insurance_renewal_interested_general_chat_" + flow_type + "_static_" + bot_gender
                    dispatcher.utter_template(template_name,tracker)
                    send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Not Interested")
                        
                   
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot), 
                            SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("current_main_slot",slot),
                            SlotSet("came_from_form_slot","sales_pitch_form")]
               
                    
    @staticmethod
    def validate_renew_not_interested(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("In renew_not_interested")
        print("entering_renew_not_interested")
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
        bot_gender = tracker.get_slot("bot_gender")
        customer_care_number= tracker.get_slot("customer_care_number") # add slot
            
        if value == "TRUE":

            # When customer got conveinced
            if(sub_intent == "affirm" or sub_intent == "general_ask_inform") and signal == "interested" and (context == "insurance_renewal" or context == "general") and (sub_context == "action_by_customer" or sub_context == "general"):
                template_name = "utter_affirm_insurance_insurance_renewal_interested_insurance_info_" + flow_type + "_static_" + bot_gender
                dispatcher.utter_template(template_name,tracker, customer_care_number=customer_care_number)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag=TIMEOUT_FLAG)
                return {"renew_not_interested": value,"stop_conversation":"TRUE"}

            if(sub_intent == "affirm") and (signal == "insurance_info") and (context == "payment") and (sub_context == "factual_data"):
                template_name = "utter_affirm_insurance_insurance_renewal_interested_insurance_info_" + flow_type + "_static_" + bot_gender
                dispatcher.utter_template(template_name,tracker, customer_care_number=customer_care_number)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag=TIMEOUT_FLAG)
                return {"renew_not_interested": value,"stop_conversation":"TRUE"}
            
            # When customer did not get conveinced
            if sub_intent == "deny" and (signal == "interested" or signal == "general_chat") and (context == "insurance_renewal" or context == "general") and (sub_context == "action_by_customer" or sub_context == "general"):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Not Interested",flag=DEFAULT_FLAG)
                return {"renew_not_interested": "not_interested_reason","trail_count": 0}

           
            else:
                return {"renew_not_interested": None}

        else:
            return {"renew_not_interested": None}


    @staticmethod
    def validate_not_interested_reason(
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        print("renew_not_interested")
        print("entering_into_not_interested reason")
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
        reasons_for_not_renewing = tracker.latest_message.get("reasons_for_not_renewing").get("name")
        threshold_days = tracker.get_slot("threshold_days_slot")
        threshold_time = tracker.get_slot("threshold_time_slot")
        flow_type = tracker.get_slot("flow_type")
        entities = tracker.latest_message["entities"]
        contact_no = tracker.get_slot("contact_no")
        trail_count = tracker.get_slot("trail_count")
        customer_care_number= tracker.get_slot("customer_care_number") # add slot
        renew_not_interested = tracker.get_slot("renew_not_interested")
        bot_gender = tracker.get_slot("bot_gender")

        if value == "TRUE":
            
            # Reason given for not interested as Already Renew
            if(sub_intent == "affirm" or sub_intent == "general_ask_inform") and (signal == "interested" or signal == "general_chat") and (context == "insurance_renewal") and (sub_context == "action_by_customer" or sub_context == "general"):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag=DEFAULT_FLAG,interest = "Yes",not_interested_reason = "Already Renewed")
                return {"go_to_form_slot":"already_renewed","stop_conversation":"TRUE"}
            
            # Reason given for not interested as Interested Later
            if (sub_intent == "affirm" or sub_intent == "general_ask_inform") and context == "general" and (sub_context == "action_by_customer" or sub_context == "general") and (signal == "interested_later"):
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Later",flag=DEFAULT_FLAG,interest = "Yes",not_interested_reason = "Renew Later")
                return {"go_to_form_slot":"interested_later_form","stop_conversation":"TRUE"}
            
            # Reason given for not interested
            if (reasons_for_not_renewing == "expensive_premium" or reasons_for_not_renewing == "vehicle_sold" or reasons_for_not_renewing == "vehicle_not_in_use" or  reasons_for_not_renewing == "bought_another_insurance" or reasons_for_not_renewing == "financial_issue" or reasons_for_not_renewing == "not_required" or reasons_for_not_renewing == "poor_service_experience"):
                template_name = "utter_not_interested_reason_given_" + flow_type + "_static_" + bot_gender
                dispatcher.utter_template(template_name,tracker)
                reason_mapping_for_not_interested_reason = {
                    "expensive_premium":"Expensive premium",
                    "vehicle_sold":"Vehicle Sold",
                    "vehicle_not_in_use":"Vehicle not in use",
                    "bought_another_insurance":"Bought another insurance",
                    "financial_issue":"Financial Hardship",
                    "not_required":"Not required",
                    "poor_service_experience":"Poor Service Experience",
                }
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Not Interested",flag=TIMEOUT_FLAG,not_interested_reason = reason_mapping_for_not_interested_reason[reasons_for_not_renewing])
                return {"not_interested_reason": value,"stop_conversation":"TRUE"}


            # Reason not given for not interested
            if sub_intent == "deny" and signal == "general_chat" and (sub_context == "action_by_customer" or sub_context == "general"):
                template_name = "utter_not_interested_disagree_to_proceed_general_chat_" + flow_type + "_static_" + bot_gender
                dispatcher.utter_template(template_name,tracker)
                send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Not Interested",flag=TIMEOUT_FLAG)
                return {"not_interested_reason": value,"stop_conversation":"True"}

            else:
                return {"not_interested_reason": None}
        else:
            return {"not_interested_reason": None}


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
        disposition = tracker.get_slot("disposition_slot")
        
        return [FollowupAction("action_listen"), AllSlotsReset()] 
