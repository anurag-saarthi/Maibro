import requests
import csv
import datetime

def get_sender_id(data):
    return data['sender_id'] if 'sender_id' in data else None


def get_user_id(data):
    return data['user_id'] if 'user_id' in data else None

def get_sender_id(data):
    return data["sender_id"] if "sender_id" in data else None
    
def get_request_id(data):
    return data['request_id'] if 'request_id' in data else None


def get_event_type(data):
    return data['event'] if 'event' in data else None


def get_intent_name(data):
    if 'parse_data' in data:
        if 'intent' in data['parse_data']:
            return data['parse_data']['intent']['name']
        else:
            return None
    else:
        return None


def get_intent_confidence(data):
    if 'parse_data' in data:
        if 'intent' in data['parse_data']:
            return data['parse_data']['intent']['confidence']
        else:
            return None
    else:
        return None


def get_entity(data):
    if 'parse_data' in data:
        if 'entities' in data['parse_data']:
            entities = data['parse_data']['entities']

            if entities:
                return entities
        else:
            return None
    else:
        return None


def get_action_name(data):
    if data['event'] == 'action' and data['name'] != 'action_listen':
        return data['name']
    return None


def get_action_confidence(data):
    if data['event'] == 'action' and data['name'] != 'action_listen':
        return data['confidence']
    return None


def get_timestamp(data):
    return data['timestamp']
def get_disposition_id(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "disposition_id" in data["data"]["custom"]:
                if data["data"]["custom"]["disposition_id"] is not None:
                    return data["data"]["custom"]["disposition_id"]
                return ""
            return ""
        return ""
    return ""
def get_delay_reason(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "delay_reason" in data["data"]["custom"]:
                if data["data"]["custom"]["delay_reason"] is not None:
                    return data["data"]["custom"]["delay_reason"]
                return ""
            return ""
        return ""
    return ""
def get_emi_amount(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "outstanding_payment" in data["data"]["custom"]:
                if data["data"]["custom"]["outstanding_payment"] is not None:
                    return data["data"]["custom"]["outstanding_payment"]
                return ""
            return ""
        return ""
    return ""
def get_language(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "language" in data["data"]["custom"]:
                if data["data"]["custom"]["language"] is not None:
                    return data["data"]["custom"]["language"]
                return ""
            return ""
        return ""
    return ""
def get_flow_type(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "flow_type" in data["data"]["custom"]:
                if data["data"]["custom"]["flow_type"] is not None:
                    return data["data"]["custom"]["flow_type"]
                return ""
            return ""
        return ""
    return ""
def get_ptp_date(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "ptp_date" in data["data"]["custom"]:
                if data["data"]["custom"]["ptp_date"] is not None:
                    return data["data"]["custom"]["ptp_date"]
                return ""
            return ""
        return ""
    return ""
def get_response_time(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "response_time" in data["data"]["custom"]:
                if data["data"]["custom"]["response_time"] is not None:
                    return data["data"]["custom"]["response_time"]
                return ""
            return ""
        return ""
    return ""
def get_partial_amount(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "partial_amount" in data["data"]["custom"]:
                if data["data"]["custom"]["partial_amount"] is not None:
                    return data["data"]["custom"]["partial_amount"]
                return ""
            return ""
        return ""
    return ""
def get_customer_name(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "customer_name" in data["data"]["custom"]:
                if data["data"]["custom"]["customer_name"] is not None:
                    return data["data"]["custom"]["customer_name"]
                return ""
            return ""
        return ""
    return ""
def get_loan_id(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "loan_id" in data["data"]["custom"]:
                if data["data"]["custom"]["loan_id"] is not None:
                    return data["data"]["custom"]["loan_id"]
                return ""
            return ""
        return ""
    return ""
def get_emi_amount(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "emi_amount" in data["data"]["custom"]:
                if data["data"]["custom"]["emi_amount"] is not None:
                    return data["data"]["custom"]["emi_amount"]
                return ""
            return ""
        return ""
    return ""
def get_due_date(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "due_date" in data["data"]["custom"]:
                if data["data"]["custom"]["due_date"] is not None:
                    return data["data"]["custom"]["due_date"]
                return ""
            return ""
        return ""
    return ""
def get_payment_link(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "payment_link" in data["data"]["custom"]:
                if data["data"]["custom"]["payment_link"] is not None:
                    return data["data"]["custom"]["payment_link"]
                return ""
            return ""
        return ""
    return ""
def get_interested_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "interest" in data["data"]["custom"]:
                if data["data"]["custom"]["interest"] is not None:
                    return data["data"]["custom"]["interest"]
                return ""
            return ""
        return ""
    return ""
def get_callback_time_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "callback_time" in data["data"]["custom"]:
                if data["data"]["custom"]["callback_time"] is not None:
                    return data["data"]["custom"]["callback_time"]
                return ""
            return ""
        return ""
    return ""
def get_right_party_contact_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "right_party_contact" in data["data"]["custom"]:
                if data["data"]["custom"]["right_party_contact"] is not None:
                    return data["data"]["custom"]["right_party_contact"]
                return ""
            return ""
        return ""
    return ""
def get_reason_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "reason" in data["data"]["custom"]:
                if data["data"]["custom"]["reason"] is not None:
                    return data["data"]["custom"]["reason"]
                return ""
            return ""
        return ""
    return ""

def get_ptp_recheck(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "ptp_recheck" in data["data"]["custom"]:
                if data["data"]["custom"]["ptp_recheck"] is not None:
                    return data["data"]["custom"]["ptp_recheck"]
                return ""
            return ""
        return ""
    return ""
def get_sheet_name(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "sheet_name" in data["data"]["custom"]:
                if data["data"]["custom"]["sheet_name"] is not None:
                    return data["data"]["custom"]["sheet_name"]
                return ""
            return ""
        return ""
    return ""
# Newly added keys
def get_visit_status_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "visit_status" in data["data"]["custom"]:
                if data["data"]["custom"]["visit_status"] is not None:
                    return data["data"]["custom"]["visit_status"]
                return ""
            return ""
        return ""
    return ""

def get_visit_type_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "visit_type" in data["data"]["custom"]:
                if data["data"]["custom"]["visit_type"] is not None:
                    return data["data"]["custom"]["visit_type"]
                return ""
            return ""
        return ""
    return ""

def get_visit_date_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "visit_date" in data["data"]["custom"]:
                if data["data"]["custom"]["visit_date"] is not None:
                    return data["data"]["custom"]["visit_date"]
                return ""
            return ""
        return ""
    return ""

def get_kyc_status_data(data):
    if "data" in data:
        if "custom" in data["data"] and data["data"]["custom"] is not None:
            if "kyc_status" in data["data"]["custom"]:
                if data["data"]["custom"]["kyc_status"] is not None:
                    return data["data"]["custom"]["kyc_status"]
                return ""
            return ""
        return ""
    return ""



def payment_link(response):
    loan_id=get_loan_id(response)
    phone_number=get_user_id(response)
    disposition_id=get_disposition_id(response)
    flow_type = get_flow_type(response)
    message="""Dear Customer, Your safety is of utmost importance to us. Pay your monthly EMI from Home for your Loan A/c no {0}
            Click on the link to make the payment https://customerportal.shriramhousing.in/pay-now?UTM=BOT
            Ignore if already paid
            Shriram Housing Finance Limited""".format(loan_id)
    data={
        "username":"shflcctxn",
        "password":"shflcc987",
        "to":phone_number,
        "message":message
    }
    print("The dispositio id",disposition_id)
    print("The flow type is ",flow_type)
    print("The loan id",loan_id)
    print("The phone number is ",phone_number)
    if disposition_id.lower()=="pic" and flow_type == "post_due_0_7":
        try:
            print("****************")
            r=requests.get("http://www.wizhcomm.co.in/wems/sendsms",params=data)
            print("SMS status code:", r.status_code)
        except:
            print("Unsucessful")

        
def store_in_csv(user_id,disposition_id,ptp_date,partial_amount,delay_reason,response_time,ptp_recheck,sheet_name):
    try:
        with open('call_logs.csv', 'r+', newline='') as file:
            data = csv.reader(file)
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            if len(list(data)) == 0:
                writer.writerows(
                    [["date", "phone number", "disposition id", "ptp_date", "partial_amount","delay_reason","time","ptp_recheck","sheet_name"], [
                        current_date.strftime("%d/%m/%Y"), user_id, disposition_id, ptp_date,partial_amount,delay_reason,response_time,ptp_recheck,sheet_name]])
            else:
                writer.writerow([current_date.strftime("%d/%m/%Y"), user_id, disposition_id,ptp_date, partial_amount,delay_reason,response_time,ptp_recheck,sheet_name])
    except IOError:
        with open('call_logs.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            current_date = datetime.datetime.now()
            writer.writerows(
                [["date", "phone number", "disposition id", "ptp_date", "partial_amount","delay_reason","time","ptp_recheck","sheet_name"], [
                    current_date.strftime("%d/%m/%Y"), user_id, disposition_id, ptp_date,partial_amount,delay_reason,response_time,ptp_recheck,sheet_name]])
