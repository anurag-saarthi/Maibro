{
    "clientName": "Bajaj Housing Finance Limited Testing",
    "agentName": "Ria",
    "domain": "Sales and onboarding",
    "subDomain": "Insurance",
    "productType": "home loan",
    "parentFlow": [
        {
            "flow": "lead_generation_hl",
            "isParent": true,
            "isChild": false,
            "channel": [
                "Call"
            ],
            "type": "Female",
            "language": [
                "Hindi","English"
            ],
            "Call": {
                "voice": "Saarthi TTS",
                "thresholdDateCallBack": 2,
                "thresholdTimeCallBack": 30
            },
            "Whatsapp": {
                "slotReminder": [
                    {
                        "slot0": 120,
                        "slot1": 300
                    }
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
                    "callBackTime": 120
                },
                {
                    "value": "Already Availed",
                    "nextFlow": "Feedback",
                    "callBackTime": 120
                }
            ]
        }
    ],
    "callFlow": [{
            "lead_generation_hl": {
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
                                    "label": "another_product_pitch_form",                                
                                    "next": "subSlot2"                                    
                                    }],
                                "subSlot2": [{
                                    "label": "stop_conversation"                                    
                                    }]       
                            },
                            "loan_availed_positive": {
                                "initial": [{
                                    "label": "loan_availed_positive_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "another_product_pitch_form",                                
                                   "next": "subSlot2"                                    
                                   }],
                                "subSlot2": [{
                                    "label": "stop_conversation"                                    
                                    }]        
                            },
                            "loan_availed_negative": {
                                "initial": [{
                                    "label": "loan_availed_negative_form",
                                    "next": "subSlot1"                                    
                                    }],
                                "subSlot1": [{
                                    "label": "another_product_pitch_form",                               
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
                            "another_product_pitch": {
                                "initial": [{
                                    "label": "another_product_pitch_form",
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