from datetime import timedelta
import datetime
from re import template
import time
from actions.utils.common_imports import *
from actions.utils.helper import *
helper = Helper()


class SalesPitchForm(FormAction):
    def name(self):  # type: () -> Text
        return "already_renewed_form" # return "maia_pre_emi_male"
    print("In already_renewed_form")    

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("innnslot")
        stop_conversation = tracker.get_slot("stop_conversation")
        already_renewed = tracker.get_slot("already_renewed")

        if stop_conversation == "TRUE":
            return []
        return["already_renewed"] 


    def slot_mappings(self):  
        return {
            "already_renewed": [
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
                already_renewed_count = tracker.get_slot("already_renewed_count")
                loan_amount = tracker.get_slot("loan_amount")
                credit_product = "personal loan"
                emi_amount =tracker.get_slot("emi_amount")
                due_date =tracker.get_slot("due_date")
                due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y").strftime("%d %B %Y")
                loan_availed_slot =tracker.get_slot("loan_availed_slot")
                # nach = tracker.get_slot("nach")
                bot_gender=tracker.get_slot("bot_gender")
                variation=tracker.get_slot("variation")
                if trail_count <=2:
                    template_name =  (
                                "utter_insurance_already_renewed_"+ variation + flow_type + "_static_" + bot_gender 
                            )
                    
                    dispatcher.utter_template(template_name,tracker)
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,disposition_id="Insurance Already Renewed",flag=DEFAULT_FLAG)

                else:
                    template_name =  (
                            "utter_insurance_already_renewed_alt_" + variation + flow_type + "_static_" + bot_gender
                        )
                    dispatcher.utter_template(template_name,tracker) 
                    send_and_store_disposition_details(tracker=tracker,dispatcher=dispatcher,flag=TIMEOUT_FLAG)
                    return {"third_party_cont":"filled","stop_conversation": "TRUE"}

                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot), 
                            SlotSet("timestamp", time.time()),SlotSet("trail_count",trail_count+1),SlotSet("current_main_slot",slot),
                            SlotSet("came_from_form_slot","sales_pitch_form")]
               

                    
    @staticmethod
    def validate_already_renewed(
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
        bot_gender=tracker.get_slot("bot_gender")
        variation=tracker.get_slot("variation")
            
        if value == "TRUE":
            if entities:
                for entity in entities:
                    if entity["entity"] == "organisation":
                        template_name =  (
                            "utter_competitor_name_"+ flow_type + "_static_" + bot_gender 
                        )
                        org_name = entity["value"]
                        send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag=TIMEOUT_FLAG,interest = "Yes",Competitor=org_name)
                        dispatcher.utter_template(template_name,tracker)
                        return {"already_renewed": value,"stop_conversation":"TRUE"}
            template_name =  (
                            "utter_competitor_name_"+ flow_type + "_static_" + bot_gender 
                        )
            send_and_store_disposition_details(tracker=tracker, dispatcher=dispatcher,disposition_id="Interested Insurance Renewal",flag=TIMEOUT_FLAG,interest = "Yes")
            dispatcher.utter_template(template_name,tracker)
            return {"already_renewed": value,"stop_conversation":"TRUE"}
        else:
            return {"already_renewed": None}

            
       
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
        
        return [FollowupAction("action_listen"), AllSlotsReset()] 
