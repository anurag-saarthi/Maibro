{
    "clientName": "Vindhya E-Infomedia Testing",
    "agentName": "Kiran",
    "domain": "Sales and onboarding",
    "subDomain": "Insurance",
    "productType": "personal loan",
    "parentFlow": [
        {
            "flow": "vindhya_bf_lg_pl",
            "isParent": true,
            "isChild": false,
            "channel": [
                "Call"            ],
            "type": "Female",
            "language": [
                "Tamil"
                ],
            "Call": {
                "voice": "Saarthi TTS",
                "thresholdDateCallBack": 2,
                "thresholdTimeCallBack": 30            },
            "Whatsapp": {
                "slotReminder": [
                    {
                        "slot0": 120,
                        "slot1": 300                    }
                ]
            },
            "startDate": "04/09/2022",
            "endDate": "04/09/2022",
            "startTime": 540,
            "endTime": 1120,
            "dispositionNextNudge": [
                {
                    "value": "Interested",
                    "nextFlow": "Feedback",
                    "callBackTime": 120                },
                {
                    "value": "Already Availed",
                    "nextFlow": "Feedback",
                    "callBackTime": 120                }
            ]
        }
    ],
    "callFlow": [{
            "vindhya_bf_lg_pl": {
                        "initial": [{
                            "label": "lg_rpc_form",
                            "next": "slot1"                            
                            }],
                        "slot1": [{
                            "label": "sales_pitch_form",
                            "next": "slot2"                            
                            }],
                        "slot2": [{
                            "loan_rejected": {
                                "initial": [{
                                    "label": "loan_rejection_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "stop_conversation"                                   
                                     }]
                            },
                            "loan_availed": {
                                "initial": [{
                                    "label": "loan_availed_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "stop_conversation"                                    
                                    }]       
                            },
                            "interested": {
                                "initial": [{
                                    "label": "interested_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "number_confirmation_form",                                   
                                    "next": "subSlot2"                                   
                                     }],
                                "subSlot2": [{
                                    "label": "stop_conversation"                                    
                                    }]       
                            },
                            "not_interested":{
                                "initial": [{
                                    "label": "not_interested_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "stop_conversation"                                    
                                    }]
                            },
                            "interested_later": {
                                "initial": [{
                                    "label": "interested_later_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "stop_conversation"                                    
                                    }]
                            }
                        }]                                                      
            }
        }]
}