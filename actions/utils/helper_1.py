import csv

import pytz
import redis
import pickle
import json
import pandas as pd
import datetime
from rasa_sdk.forms import REQUESTED_SLOT
from ruamel import yaml
import time
import datetime
import requests
from rasa_sdk.events import SlotSet, FollowupAction
from actions.utils.common_imports import *
import numpy as np
from handle_bulk_data import red_maia_customers, red_maia_config


customer_informed_disagree_to_proceed = 0
customer_informed_agree_to_pay = 1
customer_informed_call_later = 2
customer_informed_decline_reason = 3
customer_informed_wrong_info = 4
customer_informed_bye = 5
customer_no_response = 18
customer_asked_human_handoff = 19
customer_informed_disagree_to_pay = 20
customer_says_hello_only = 21
customer_informed_not_audible = 22
customer_informed_partial_payment = 23
customer_informed_payment_done = 24
bot_unable_to_catch_partial_amount = 25
decline_reason_disposition_id = {
    "business_loss": "Lockdown Impact - No Income",
    "cycle_date_issue": "Cycle Date Issue",
    "insufficient_funds": "Funds Unavailable",
    "job_loss": "Loss of Job",
    "medical_issue": "Medical Expense Family/Self",
    "technical_issue": "Technical Issue",
    "family_dispute": "Family Dispute",
    "foreclosing_through_own_funds": "Foreclosing Through Own Funds",
    "branch_issue": "Branch Issue",
    "account_not_working": "Account Not Working",
    "change_account_for_deduction": "Change Account for Deduction",
    "transfer_to_another_hfc": "Transfer to another HFC",
    "salary_issue": "Salary Issue",
}
mapping_delay_reasons={
        'turn_around_time_issue' : 'Long Processing Time',
        'pre_paying_issue' : 'Pre-pay Issue',
        'tenure_issue' : 'Tenure Issue',
        'credit_limit_issue' : 'Loan Amount Issue',
        'high_interest_rate' : 'High Interest Rate',
        'insufficient_funds' : 'Insufficient Funds',
        'payment_gateway_issue' : 'Payment Gateway Issue',
        'looking_for_another_product' : 'Interested In Another Product',
        'customer_death' : 'User Death',
        'death_in_family' : 'Death In Family',
        'family_health_issue' : 'Family Health Issue',
        'family_matter' : 'Family Matter',
        'job_loss' : 'Jobloss',
        'jobless' : 'Jobless',
        'fraud_sale' : 'Fraud Sales',
        'natural_disaster' : 'Natural Disaster',
        'out_of_station' : 'Out Of Station',
        'personal_issue' : 'Personal Issue',
        'property_dispute' : 'Property Dispute',
        'salary_not_received' : 'Salary Issue',
        'salary_time_specific_delay' : 'Salary Time Delayed',
        'unable_to_find_work' : 'Jobless',
        'unprofessional_employee' : 'Jobless',
        'user_health_issue' : 'User Health Issue',
        'user_technical_issue' : 'Technical Issue',
        'dont_have_vehicle' : 'No Vehicle',
        'already_taken_from_others' : 'Already Taken From Others',
        'no_delay_reason' : 'Others',
        "business_loss": "Business Loss"
}

mapping_utter_flow = {
    'lead_generation':'LG',
    'lead_qualification':'LQ',
    'kyc':'KYC',
    'status':'STATUS',
    'follow_up':'FU',
}

def get_time(current_time):
    four_hours_from_now = '{:%H:%M}'.format(datetime.datetime.now() + datetime.timedelta(hours=4))
    current = time.strptime(current_time, "%H:%M")
    timevalue_current = time.strftime( "%I:%M %p", current )
    next = time.strptime(four_hours_from_now, "%H:%M")
    timevalue_12hour = time.strftime( "%I:%M %p", next )
    if timevalue_current > "03:00 PM":
        return('10:00')
    else:
        return timevalue_12hour


def flow_mapping(flow_data,flow_list,dispo):
    data = flow_list[-1]
    # print("74",data)
    if "initial" in data:
        data1 = data["initial"][0]
        if "label" in data1:
            ans = data["initial"][0]["label"]
            if ans == "stop_conversation":
                next_form = "stop_conversation"
                flow_list=["End_Call"]
            else:
                next_form = data["initial"][0]["next"]
                next_data = data[next_form]
                flow_list.append(next_data)
            # print("80")
        elif "flow" in data1:
            # ans = None
            next_form = data["initial"][0]["flow"]
            # a=0
            # for dict in flow_data:
            #     for key in dict.keys():
            #         if key==next_form:
            #             i=a
            #         else:
            #             a+=1
            next_data = flow_data[0][next_form]
            flow_list = [next_data]
    else:
        data1 = data[0]
        data = flow_list[-2]
        if dispo in data1:
            temp_data = data1[dispo]["initial"][0]
            if "label" in temp_data:
                ans = data1[dispo]["initial"][0]["label"]
                if ans == "stop_conversation":
                    next_form = "stop_conversation"
                    flow_list=["End_Call"]
                else:
                    next_form = data1[dispo]["initial"][0]["next"]
                    for keys in data1[dispo].keys():
                        if next_form == keys:
                            current_data = data1[dispo]              #current level
                            flow_list[-1]=current_data
                            next_data = data1[dispo][next_form]      #next_form value in current level
                            flow_list.append(next_data)
                            temp = -9
                        else:
                            temp = len(flow_list)
                            while temp>=2:
                                try:
                                    next_data = flow_list[-2][next_form]
                                    flow_list[-1]=next_data
                                    temp = -9
                                    break
                                except:
                                    flow_list.pop()
                                    temp = temp-1
                    if temp<=1 and temp!= -9:
                        next_form = "ERROR: can't find slot: "+next_form
                                    
            elif "flow" in temp_data:
                # ans = None
                next_form = data1[dispo]["initial"][0]["flow"]
                # a=0
                # for dict in flow_data:
                #     for key in dict.keys():
                #         if key==next_form:
                #             i=a
                #         else:
                #             a+=1
                next_data = flow_data[0][next_form]
                flow_list = [next_data]
        elif "label" in data1:
            ans = data1["label"]
            if ans == "stop_conversation":
                next_form = "stop_conversation"
                flow_list=["End_Call"]
            else:
                temp = len(flow_list)
                next_form = data1["next"]
                # i=0
                while temp>=2:
                    # i= i +1
                    # print("while",i,"   temp",temp)
                    try:
                        next_data = flow_list[-2][next_form]
                        flow_list[-1]=next_data
                        temp = -9
                        # print("try",temp)
                    except:
                        # print("except")
                        flow_list.pop()
                        temp = temp-1
                    # except:
                    #     print("final",temp)
                    #     next_form = "ERROR: can't find slot"
                    #     temp = -1
                # print
                if temp<=1 and temp!= -9:
                    next_form = "ERROR: can't find slot: "+next_form
        elif "flow" in data1:
            # ans = None
            next_form = data1["flow"]
            # a=0
            # for dict in flow_data:
            #     for key in dict.keys():
            #         if key==next_form:
            #             i=a
            #         else:
            #             a+=1
            next_data = flow_data[0][next_form]
            flow_list = [next_data]
    return ans,next_form,flow_list


def repeat_verifier(nlu_data_list,nlu_data):
    nlu_data_list = ["general"]
    if nlu_data_list == None:
        nlu_data_list = []
    count = False
    nlu_data_list.append(nlu_data)
    print("nlu_data",nlu_data)
    print("repeat_verifier214",nlu_data_list)
    if len(nlu_data_list) >= 2:
        last = nlu_data_list[-1]
        last_second = nlu_data_list[-2]
        last_third = nlu_data_list[-3]
        if last == last_second == last_third:
            print("helper219")
            # return [FollowupAction("action_repeating_count")]
            count = True
    return nlu_data_list,count

customer_informed_payment_not_done = 1
customer_informed_promise_to_pay_date_with_in_7_days = 2
customer_informed_promise_to_pay_date_after_7_days = 15
customer_informed_ptp_date_with_count_greater_than_2 = 16
customer_informed_payment_later = 3
customer_informed_payment_issue = 4
customer_informed_payment_link_issue = 6
customer_informed_human_hand_off = 7
customer_informed_pay_with_another_method = 10
customer_informed_payment_today = 12
bot_unable_to_understand = 14
customer_informed_do_not_call = 17
customer_informed_other_language = 19
language_issue = 20


# config = pd.read_csv("config.csv")
# config.replace(np.nan, "no", inplace=True)
# print(config)


# def get_details_from_config(client_id, flow_type):
#     print(type(client_id))
#     print(type(flow_type))
#     print(client_id)
#     print(flow_type)
#     df = config[
#         (config["client_id"] == int(client_id)) & (config["flow_type"] == flow_type)
#     ]
#     c_name = df["client_name"].astype(str)
#     agent_name = df["agent_name"].astype(str)
#     typology = df["typology"].astype(str)
#     print("inside get_details_from_config")

#     c_name = list(c_name)
#     agent_name = list(agent_name)
#     typology = list(typology)
#     print(c_name)
#     print(agent_name)
#     print(typology)
#     return str(c_name[0]), str(agent_name[0]), str(typology[0])


# def get_all_deatils_from_config(client_id, flow_type):
#     df = config[(config["client_id"] == client_id) & (config["flow_type"] == flow_type)]
#     df = df.astype(str)
#     return df


# customer_data=pd.read_csv("customer_details_new.csv")
# customer_data.replace(np.nan,"",regex=True,inplace=True)
def send_and_store_disposition_details(
    tracker=None,
    dispatcher=None,
    flag=702,
    disposition_id=None,
    user_message=None,
    ptp_date=None,
    partial_amount=None,
    delay_reason=None,
    flow_type=None,
    language=None,
    outstanding_payment=None,
    customer_name=None,
    website = None,
    loan_id=None,
    emi_amount=None,
    loan_amount= None,
    contact_no = None,
    due_date=None,
    payment_link=None,
    ptp_recheck=None,
    sheet_name=None,
    client_id=None,
    bot_gender = None,
    interest = None,
    callback_time = None,
    reason = None,
    right_party_contact = None,
    slot_number = None,
    visit_status = None,
    visit_type = None,
    visit_date = None,
):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    helper = Helper()
    customer_name = tracker.get_slot("customer_name")
    flow_type = tracker.get_slot("flow_type")
    loan_id = tracker.get_slot("loan_id")
    # website = tracker.get_slot("website_name")
    emi_amount = tracker.get_slot("emi_amount_slot")
    loan_amount = tracker.get_slot("loan_amount")
    contact_no = tracker.get_slot("contact_no")
    due_date = tracker.get_slot("due_date")
    
    # bot_gender = tracker.get_slot("bot_gender")
    # gender = bot_gender.split("_")[1]

    helper.send_conversation_flag(
        flag,
        dispatcher,
        delay_reason=delay_reason,
        message=user_message,
        disposition_id=disposition_id,
        ptp_date=ptp_date,
        time=time,
        partial_amount=partial_amount,
        customer_name=customer_name,
        website = website,
        loan_id=loan_id,
        emi_amount=emi_amount,
        loan_amount = loan_amount,
        contact_no = contact_no,
        due_date=due_date,
        payment_link=payment_link,
        ptp_recheck=ptp_recheck,
        sheet_name=sheet_name,
        flow_type=flow_type,
        # bot_gender = gender,
        slot_number = slot_number,
        reason = reason,
        right_party_contact = right_party_contact,
        callback_time = callback_time,
        interest =interest,
        visit_status = visit_status,
        visit_type = visit_type,
        visit_date = visit_date,
    )


def store_call_log(
    disposition_id=None,
    tracker=None,
    user_message=None,
    ptp_date=None,
    partial_amount=None,
    delay_reason=None,
    flow_type=None,
    language=None,
    outstanding_payment=None,
    time=None,
):
    # TODO need to handle the if phone number coming from tracker having string -> it leads to expection
    print("------------Store call getlog------------")
    phone_number = tracker.user_id
    try:
        with open("call_logs.csv", "r+", newline="") as file:
            data = csv.reader(file)
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            if len(list(data)) == 0:
                writer.writerows(
                    [
                        [
                            "date",
                            "phone number",
                            "disposition id",
                            "user message",
                            "ptp_date",
                            "partial_amount",
                            "delay_reason",
                            "emi flow",
                            "time",
                        ],
                        [
                            current_date.strftime("%d/%m/%Y"),
                            phone_number,
                            disposition_id,
                            user_message,
                            ptp_date,
                            partial_amount,
                            delay_reason,
                            flow_type,
                            time,
                        ],
                    ]
                )
            else:
                writer.writerow(
                    [
                        current_date.strftime("%d/%m/%Y"),
                        phone_number,
                        disposition_id,
                        user_message,
                        ptp_date,
                        partial_amount,
                        delay_reason,
                        flow_type,
                        time,
                    ]
                )
    except IOError:
        with open("call_logs.csv", "w+", newline="") as file:
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            writer.writerows(
                [
                    [
                        "date",
                        "phone number",
                        "disposition id",
                        "user message",
                        "ptp_date",
                        "partial_amount",
                        "delay_reason",
                        "emi flow",
                        "time",
                    ],
                    [
                        current_date.strftime("%d/%m/%Y"),
                        phone_number,
                        disposition_id,
                        user_message,
                        ptp_date,
                        partial_amount,
                        delay_reason,
                        flow_type,
                        time,
                    ],
                ]
            )


def get_ptp_day_count(tracker):
    phone_number = tracker.user_id
    data = pd.read_csv("call_logs.csv")
    try:
        data["month"] = pd.to_datetime(data["date"], format="%d/%m/%Y").dt.month
        employee_records = data.loc[
            (data["phone number"] == int(phone_number))
            & (data["month"] == datetime.datetime.now().month)
        ]
        print(employee_records)
        return len(employee_records)
    except:
        return 0


def set_ptp_day_count(tracker):
    pass


def get_trail_count(tracker):
    trail_count = tracker.get_slot("trail_count")
    if trail_count is None:
        return 1
    else:
        try:
            trail_count = int(trail_count) + 1
            return trail_count
        except:
            return 1


def get_return_values(tracker):
    if tracker.active_form.get("name") is not None:
        return [
            SlotSet(REQUESTED_SLOT, None),
            SlotSet("trail_count", get_trail_count(tracker)),
            FollowupAction(tracker.active_form.get("name")),
        ]
    # print("tracker.active_form.get()",tracker.active_form.get("name"))
    return [FollowupAction("action_listen")]


def get_disposition_id(intent):
    disposition_id = None
    if intent == "deny" or intent == "disagree_to_pay":
        disposition_id = customer_informed_disagree_to_pay
    if intent == "disagree_to_proceed":
        disposition_id = customer_informed_disagree_to_proceed
    if intent == "pay_later":
        disposition_id = customer_informed_payment_later
    if intent == "inform_pay_with_other_method":
        disposition_id = customer_informed_pay_with_another_method
    if intent == "bye":
        disposition_id = customer_informed_bye
    if intent == "inform_wrong_info":
        disposition_id = customer_informed_wrong_info
    if intent == "inform_payment_going_on":
        disposition_id = customer_informed_wrong_info
    if intent == "inform_payment_done":
        disposition_id = customer_informed_payment_done
    return disposition_id


def get_user_details_2(tracker):
    phone_number = tracker.user_id
    user_details = requests.get(
        "http://13.92.118.170/sheetapi/navi/userDetails?phone_number={}".format(
            phone_number
        )
    )
    print(user_details)
    if user_details.status_code == 200:
        user_details = user_details.json()
        if user_details.get("status") == 200 and "response" in user_details:
            print(user_details["response"])
            if (
                "response" in user_details["response"]
                and len(user_details["response"]["response"]) > 0
            ):
                formatted_data = {
                    "name": user_details["response"]["response"][0]["name"].lower(),
                    "monthly_emi": user_details["response"]["response"][0]["emi_amt"],
                    "language": user_details["response"]["response"][0][
                        "custom_field_2"
                    ],
                }
                emi_date = user_details["response"]["response"][0]["emi_date"]
                if emi_date:
                    emi_date = datetime.datetime.strptime(emi_date, "%d-%m-%Y")
                formatted_data["monthly_emi_date"] = emi_date.strftime("%d %B %Y")
                print(emi_date)
                return formatted_data
    formatted_data = {
        "name": "",
        "language": "en",
        "monthly_emi": 1000,
        "monthly_emi_date": datetime.datetime.now().strftime("%d %B %Y"),
    }
    return formatted_data


mapped_languages = {
    "english": "en",
    "hindi": "hi",
    "tamil": "tam",
    "telugu": "tel",
    "kannada": "ka",
    "malayalam": "ml",
    "marathi": "ma",
    "punjabi": "pa",
    "bangla": "bn",
    "gujarati": "gu",
}


def get_user_details(tracker):
    phone_number = tracker.user_id
    cust_details = red_maia_customers.hgetall(phone_number)

    print("The initial customer details (((((((()))))))) ",cust_details)
    formatted_data = {
        "employee_name": "",
        "language": "en",
        "emi_date": datetime.datetime.now().strftime("%d %B %Y"),
        "EMI Amount": 1000,
        "website": "",
        "customer_status": "",
        "no_of_days": "",
        "Hin_Audio_ID_1": "",
        "bucket_list": "",
        "area": "",
        "Due date": datetime.datetime.now().strftime("%d %B %Y"),
        "flow_type": "",
        "payment_link": "",
        "loan_id": "",
        "job_id": "",
        "sheet_name": "",
        "threshold_time":"",
        "supported_languages":""
    }
    if len(cust_details) > 0:
        # formatted_data["EMI Amount"] = int(cust_details.get("loanAccountDetails.loanAmount"))
        print("helper571",cust_details)
        # emi_date = cust_details.get("loanAccountDetails.emiDueDate")
        # if emi_date:
        #     formatted_data["emi_date"] = emi_date
        formatted_data["employee_name"] = cust_details.get("primaryInfo.firstName").lower()
        lang = cust_details.get("primaryInfo.language").lower()
        formatted_data["language"] = mapped_languages[lang]
        formatted_data["contact_no"] = "18001022468" #cust_details.get("contact_no")
        formatted_data["flow_type"] = cust_details.get("primaryInfo.flow")
        formatted_data["client_name"] = cust_details.get("client_name")
        # formatted_data["website_name"] = cust_details.get("website.primary")
        formatted_data["agent_name"] = "Divya" #cust_details.get("agent_name")
        formatted_data["supported_languages"] = cust_details.get("supported_languages")
       
        formatted_data["disposition"] = cust_details.get("disposition")
        

        # agent_config = {
        #         "clientName": "TVS Credit Testing",
        #         "agentName": "Divya",
        #         "domain": "BFSI",
        #         "subDomain": "Insurance",
        #         "productType": "personal loan",
        #         # "threshold_days": "3",
        #         # "threshold_time": "19:00",
        #         # "utter_bot_gender_slot": "F",
        #         # "utter_category_slot": "general",
        #         # "utter_client_name_slot": "Bajaj",
        #         # "utter_type_slot": "G",
        #         # "website.primary": "www.bajajfinserv.in",
        #         "parentFlow": [
        #             {
        #                 "flow": "lead_generation",
        #                 "isParent": True,
        #                 "isChild": False,
        #                 "channel": [
        #                     "Voice"
        #                 ],
        #                 "type": "Male",
        #                 "language": [
        #                     "Tamil"
        #                 ],
        #                 "voice": {
        #                     "voice": "Saarthi TTS",
        #                     "thresholdDateCallBack": 2,
        #                     "thresholdTimeCallBack": 30
        #                 },
        #                 "whatsapp": {
        #                     "slotReminder": [
        #                         {
        #                             "slot0": 120,
        #                             "slot1": 300
        #                         }
        #                     ]
        #                 },
        #                 "startDate": "04/09/2022",
        #                 "endDate": "04/09/2022",
        #                 "startTime": 540,
        #                 "endTime": 1120,
        #                 "dispositionNextNudge": [
        #                     {
        #                         "value": "Interested",
        #                         "nextFlow": "Feedback",
        #                         "callBackTime": 120
        #                     },
        #                     {
        #                         "value": "Already Availed",
        #                         "nextFlow": "Feedback",
        #                         "callBackTime": 120
        #                     }
        #                 ]
        #             },
        #             {
        #                 "flow": "lead_qualification",
        #                 "isParent": False,
        #                 "isChild": True
        #             },
        #             {
        #                 "flow": "feedback",
        #                 "isParent": True,
        #                 "isChild": True,
        #                 "channel": [
        #                     "Email"
        #                 ],
        #                 "type": "Male",
        #                 "language": [
        #                     "English"
        #                 ],
        #                 "voice": {
        #                     "voice": "Saarthi TTS",
        #                     "thresholdDateCallBack": 2,
        #                     "thresholdTimeCallBack": 30
        #                 },
        #                 "whatsapp": {
        #                     "slotReminder": [
        #                         {
        #                             "slot0": 120,
        #                             "slot1": 300
        #                         }
        #                     ]
        #                 },
        #                 "startDate": "04/09/2022",
        #                 "endDate": "04/09/2022",
        #                 "startTime": 540,
        #                 "endTime": 1120
        #             }
        #         ],
        #         "callFlow": [
        #             {
        #             "lead_generation": {
        #                 "initial": [{
        #                     "label": "lg_rpc_form",
        #                     "next": "slot1"
        #                 }],
        #                 "slot1": [{
        #                     "label": "sales_pitch_form",
        #                     "next": "slot2"
        #                 }],
        #                 "slot2": [{
        #                     "Interested": {
        #                         "initial": [{
        #                             "flow": "lead_qualification",
        #                         }]
        #                     },
        #                     "Not_Interested": {
        #                         "initial": [{
        #                             "label": "Nurturing",
        #                             "next": "subSlot1"
        #                         }],
        #                         "subSlot1": [{
        #                             "label": "Nurturing",
        #                             "next": "subSlot2"
        #                         }],
        #                         "subSlot2": [{
        #                             "Interested": {
        #                                 "initial": [{
        #                                     "label": "Later_Date_Approach",
        #                                     "next": "slot3"
        #                                 }]
        #                             },
        #                             "Not_Interested": {
        #                                 "initial": [{
        #                                     "label": "Nurturing",
        #                                     "next": "subsubSlot1"
        #                                 }],
        #                                 "subsubSlot1": [{
        #                                     "label": "Later_Date_Approach",
        #                                     "next": "subsubSlot2"
        #                                 }],
        #                                 "subsubSlot2": [{
        #                                     "flow": "lead_qualification"
        #                                 }]
        #                             }
        #                         }],
        #                         "subSlot3": [{
        #                             "flow": "feed_back"
        #                         }]
        #                     }
        #                 }],
        #                 "slot3": [{
        #                     "label": "Sales Pitch Message",
        #                     "next": "slot2"
        #                 }]
        #             },   
        #             'kyc': {
        #                 'initial': [{
        #                     'label': 'lg_rpc_form',
        #                     'next': 'slot1'
        #                 }],
        #                 'slot1': [{
        #                     'label': 'spm_agent_branch_later_3_form',
        #                     'next': 'slot2'
        #                 }],
        #                 'slot2': [{
        #                     'visit_agent': {
        #                         'initial': [{
        #                             'label': 'agent_visit_1_form',
        #                             'next': 'subSlot1'
        #                         }],
        #                         'subSlot1': [{
        #                             'label': 'beyond_tt_end_form',
        #                             'next': 'subSlot2'
        #                             }],
        #                         'subSlot2': [{
        #                             'label': 'stop_conversation'
        #                         }]
        #                     },
        #                     'visit_branch': {
        #                         'initial': [{
        #                             'label': 'branch_visit_1_form',
        #                             'next': 'subSlot1'
        #                         }],
        #                         'subSlot1': [{
        #                             'label': 'beyond_tt_end_form',
        #                             'next': 'subSlot2'
        #                         }],
        #                         'subSlot2': [{
        #                             'label': 'stop_conversation'
        #                         }]        
        #                     },
        #                     'interested_later': {
        #                         'initial': [{
        #                             'label': 'interested_later_form',
        #                             'next': 'subSlot1'
        #                         }],
        #                         'subSlot1': [{
        #                             'label': 'stop_conversation'
        #                         }]
        #                     }
        #                 }]
        #             },
        #             'follow_up': {
        #                         'initial': [{
        #                             'label': 'lg_rpc_form',
        #                             'next': 'slot1'
        #                         }],
        #                         'slot1': [{
        #                             'branch_visit':{
        #                                 'initial': [{
        #                                     'label':'spm_branch_visit_form',
        #                                     'next': 'subSlot1'
        #                                 }],
        #                                 'subSlot1': [{
        #                                     'affirm': {
        #                                         'initial': [{
        #                                             'label': 'branch_visit_1_form',
        #                                             'next': 'sub1Slot1'
        #                                         }],
        #                                         'sub1Slot1': [{
        #                                             'label': 'beyond_tt_end_form',
        #                                             'next': 'sub1Slot2'
        #                                         }],
        #                                         'sub1Slot2': [{
        #                                             'label': 'stop_conversation'
        #                                         }]
        #                                     },
        #                                     'nurturing': {
        #                                         'initial': [{
        #                                             'label': 'nurturing_agent_branch_2_form',
        #                                             'next': 'subSlot1'
        #                                         }],
        #                                         'subSlot1': [{
        #                                             'branch_visit': {
        #                                                 'initial': [{
        #                                                     'label': 'branch_visit_1_form',
        #                                                     'next': 'sub2Slot1'
        #                                                 }],
        #                                                 'sub2Slot1': [{
        #                                                     'label': 'beyond_tt_end_form',
        #                                                     'next': 'sub3Slot1'
        #                                                 }],
        #                                                 'sub3Slot1':[{
        #                                                     'label':'stop_conversation'
        #                                                 }],
        #                                             },
        #                                             'agent_visit': {
        #                                                 'initial': [{
        #                                                     'label': 'agent_visit_1_form',
        #                                                     'next': 'sub2Slot1'
        #                                                 }],
        #                                                 'sub2Slot1': [{
        #                                                     'label': 'beyond_tt_end_form',
        #                                                     'next': 'sub3Slot1'
        #                                                 }],
        #                                                 'sub3Slot1':[{
        #                                                     'label':'stop_conversation'
        #                                                 }],
        #                                             }
        #                                         }]
        #                                     },
        #                                     'interested_later': {
        #                                         'initial': [{
        #                                             'label': 'interested_later_form',
        #                                             'next': 'subSlot1'
        #                                         }],
        #                                         'subSlot1': [{
        #                                             'label': 'stop_conversation'
        #                                         }]
        #                                     },
        #                                     'beyond_tt':{
        #                                         'initial':[{
        #                                             'label':'beyond_tt_end_form',
        #                                             'next':'subSlot1'
        #                                         }],
        #                                         'subSlot1':[{
        #                                             'label': 'stop_conversation'
        #                                         }]
        #                                     }
        #                                 }]
        #                                 },
        #                             'executive_visit': {
        #                                 'initial': [{
        #                                         'label':'spm_agent_visit_form',
        #                                         'next': 'subSlot1'
        #                             }],
        #                                 'subSlot1': [{
        #                                     'agent_visit': {
        #                                         'initial': [{
        #                                             'label': 'agent_visit_1_form',
        #                                             'next': 'sub1Slot1'
        #                                         }],
        #                                         'sub1Slot1':[{
        #                                                     'label': 'beyond_tt_end_form',
        #                                                     'next': 'sub2Slot1'
        #                                         }],
        #                                         'sub2Slot1':[{
        #                                                     'label': 'stop_conversation'
        #                                         }]
                                                    
        #                                     },
        #                                     'nurturing': {
        #                                     'initial': [{
        #                                         'label': 'nurturing_agent_branch_2_form',
        #                                         'next': 'subSlot1'
        #                                     }],
        #                                     'subSlot1': [{
        #                                         'branch_visit': {
        #                                             'initial': [{
        #                                                 'label': 'branch_visit_1_form',
        #                                                 'next': 'sub2Slot1'
        #                                             }],
        #                                             'sub2Slot1': [{
        #                                                 'label': 'beyond_tt_end_form',
        #                                                 'next': 'sub3Slot1'
        #                                             }],
        #                                             'sub3Slot1':[{
        #                                                 'label':'stop_conversation'
        #                                             }],
        #                                         },
        #                                     'agent_visit': {
        #                                         'initial': [{
        #                                             'label': 'agent_visit_1_form',
        #                                             'next': 'sub2Slot1'
        #                                         }],
        #                                         'sub2Slot1': [{
        #                                             'label': 'beyond_tt_end_form',
        #                                             'next': 'sub3Slot1'
        #                                         }],
        #                                         'sub3Slot1':[{
        #                                             'label':'stop_conversation'
        #                                         }],
        #                                     }

        #                                 }]
        #                             },
        #                                     'interested_later': {
        #                                         'initial': [{
        #                                             'label': 'interested_later_form',
        #                                             'next': 'subSlot1'
        #                                         }],
        #                                         'subSlot1': [{
        #                                             'label': 'stop_conversation'
        #                                         }]
        #                                     },
        #                                     'beyond_tt':{
        #                                         'initial':[{
        #                                             'label':'beyond_tt_end_form',
        #                                             'next':'subSlot1'
        #                                         }],
        #                                         'subSlot1':[{
        #                                             'label': 'stop_conversation'
        #                                         }]
        #                                     }
        #                             }]
        #                         }
        #                     }],
        #                 }   
        #             }
        #         ]
        #     }
        agent_config = cust_details.get("agent_config")
        agent_config = json.loads(agent_config)
        # print("583helper",type(agent_config),agent_config)
        formatted_data["flow_data"] = agent_config.get("callFlow")
        formatted_data["agent_name"] = agent_config.get("agentName")
        formatted_data["threshold_days"] = agent_config.get("threshold_days")
        formatted_data["threshold_time"] =  agent_config.get("threshold_time")
        formatted_data["utter_client_name_slot"]= agent_config.get("utter_client_name_slot")
        # formatted_data["utter_flow_slot"]=cust_details.get("utter_flow_slot")
        formatted_data["utter_type_slot"]= agent_config.get("threshold_days")
        formatted_data["utter_category_slot"]= agent_config.get("utter_category_slot")
        formatted_data["utter_bot_gender_slot"]= agent_config.get("utter_bot_gender_slot")

        return formatted_data       
    else:
        cust_details = red_maia_customers.hgetall("9851197922")
        if len(cust_details) > 0:
            formatted_data["employee_name"] = "Arvind"  # cust_details.get("primaryInfo.firstName")
            # formatted_data["EMI Amount"] = int(cust_details.get("loanAccountDetails.loanAmount"))
            lang = cust_details.get("primaryInfo.language").lower()
            formatted_data["language"] = mapped_languages[lang]
            formatted_data["payment_link"] = "https://rzp.io/i/IoaIycnilE"
            formatted_data["loan_id"] = "Demo-12345"
            formatted_data["flow_type"] = cust_details.get("primaryInfo.flow")
            formatted_data["loan_amount"] = cust_details.get("loan_amount")
            formatted_data["contact_no"] = cust_details.get("contact_no")
            formatted_data["website"] = cust_details.get("website.primary")
            emi_date = cust_details.get("loanAccountDetails.emiDueDate")
            formatted_data["region"] = "urban"
            formatted_data["ptp_days"] = 20
            formatted_data["no_of_loans"] = cust_details.get("no_of_loans")
            formatted_data["typology"] = cust_details.get("typology")
            formatted_data["age"] = cust_details.get("age")
            formatted_data["gender"] = cust_details.get("gender")
            formatted_data["geographic_location"] = cust_details.get("geographic_location")
            formatted_data["collared"] = cust_details.get("collared")
            formatted_data["client_name"] = cust_details.get("client_name")
            formatted_data["total_loan_amount"] = cust_details.get("total_loan_amount")
            formatted_data["interest_rate"] = cust_details.get("interest_rate")
            formatted_data["principal_amount"] = cust_details.get("principal_amount")
            formatted_data["late_fees"] = cust_details.get("late_fees")
            formatted_data["loan_start_date"] = cust_details.get("loan_start_date")
            formatted_data["loan_end_date"] = cust_details.get("loan_end_date")
            formatted_data["loan_amount_remaining"] = cust_details.get("loan_amount_remaining")
            formatted_data["tenure_left"] = cust_details.get("tenure_left")
            formatted_data["agent_name"] = "Maia"
            formatted_data["supported_languages"] = ["English", "Hindi"]
            formatted_data["threshold_days"] = 2
            formatted_data["threshold_time"] = "07:00"
            formatted_data["partial_payment"] = "yes"
            formatted_data["level_of_negotiation"] = 2
            formatted_data["sms_integration"] = "No"
            formatted_data["minimum_nogotiation_percentage"] = 10
            formatted_data["utter_client_name_slot"]=cust_details.get("utter_client_name_slot")
            formatted_data["utter_flow_slot"]=cust_details.get("utter_flow_slot")
            formatted_data["utter_type_slot"]=cust_details.get("utter_type_slot")
            formatted_data["utter_category_slot"]=cust_details.get("utter_category_slot")
            formatted_data["utter_bot_gender_slot"]=cust_details.get("utter_bot_gender_slot")
            emi_date = cust_details.get("loanAccountDetails.emiDueDate")
            if emi_date:
                formatted_data["emi_date"] = emi_date
            return formatted_data
    return formatted_data

class Helper:
    def __init__(self):
        pass

    def format_date(self, date):
        # Formats the date to readable format
        if date:
            date = str(date)[:-3]
            date_time = datetime.datetime.fromtimestamp(int(date)) + datetime.timedelta(
                hours=+8
            )
            date_string = date_time.strftime("%d/%m/%Y, %H:%M:%S")
            return date_string

    def send_conversation_flag(
        self,
        flag,
        dispatcher,
        message=None,
        time_limit=8,
        disposition_id=None,
        language_change=None,
        delay_reason=None,
        ptp_date=None,
        time=None,
        partial_amount=None,
        customer_name=None,
        website =None,
        loan_id=None,
        emi_amount=None,
        loan_amount = None,
        contact_no = None,
        due_date=None,
        payment_link=None,
        ptp_recheck=None,
        sheet_name=None,
        flow_type=None,
        bot_gender = None,
        callback_time = None,
        slot_number = None,
        reason = None,
        right_party_contact = None,
        interest = None,
        visit_status = None,
        visit_type = None,
        visit_date = None,

    ):
        # Send Flags to backend.

        conv_flag = dict()
        conv_flag["status"] = flag
        if message:
            conv_flag["message"] = message
        # if disposition_id:
        conv_flag["disposition_id"] = disposition_id
        conv_flag["delay_reason"] = delay_reason
        conv_flag["ptp_date"] = ptp_date
        conv_flag["time_limit"] = time_limit
        conv_flag["response_time"] = time
        conv_flag["partial_amount"] = partial_amount
        conv_flag["customer_name"] = customer_name
        conv_flag["website"] = website
        conv_flag["loan_id"] = loan_id
        conv_flag["emi_amount"] = emi_amount
        conv_flag["loan_amount"] = loan_amount
        conv_flag["contact_no"] = contact_no
        conv_flag["due_date"] = due_date
        conv_flag["payment_link"] = payment_link
        conv_flag["ptp_recheck"] = ptp_recheck
        conv_flag["sheet_name"] = sheet_name
        conv_flag["flow_type"] = flow_type
        conv_flag["bot_gender"] = bot_gender
        conv_flag["reason"] = reason
        conv_flag["right_party_contact"] = right_party_contact
        conv_flag["interest"] = interest
        conv_flag["visit_status"]=visit_status
        conv_flag["visit_type"]=visit_type
        conv_flag["visit_date"]=visit_date
        dispatcher.utter_custom_json(conv_flag)

    @staticmethod
    def get_daytime():
        tz_NY = pytz.timezone("Asia/Kolkata")
        datetime_NY = datetime.datetime.now(tz_NY)
        current_time = int(datetime_NY.strftime("%H"))
        print("dsfasfsfs", current_time)
        daytime = "good morning"
        if 12 <= int(current_time) < 17:
            daytime = "good afternoon"
        elif int(current_time) >= 17:
            daytime = "good evening"
        print(daytime)
        return daytime