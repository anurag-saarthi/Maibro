{
    "clientName": "Fullerton",
    "agentName": "Dia",
    "domain": "Sales and onboarding",
    "subDomain": "Insurance",
    "productType": "two wheeler loan",
            "parentFlow": [
                {
                    "flow": "fullerton_2wl",
                    "isParent": true,
                    "isChild": false,
                    "channel": [
                        "Call"                    ],
                    "type": "Female",
                    "language": [
                        "Hindi"                    ],
                    "Call": {
                        "voice": "Saarthi TTS",
                        "thresholdDateCallBack": 2,
                        "thresholdTimeCallBack": 30                    },
                    "Whatsapp": {
                        "slotReminder": [
                            {
                                "slot0": 120,
                                "slot1": 300                            }
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
                            "callBackTime": 120                        },
                        {
                            "value": "Already Availed",
                            "nextFlow": "Feedback",
                            "callBackTime": 120                        }
                    ]
                }
            ],
            "callFlow": [
                {
                    "fullerton_2wl": {
                        "initial": [
                            {
                                "label": "lq_rpc_form",
                                "next": "slot1"                            }
                        ],
                        "slot1": [
                            {
                                "label": "sales_pitch_form",
                                "next": "slot2"                            }
                        ],
                        "slot2": [
                            {
                                "loan_rejected": {
                                    "initial": [
                                        {
                                            "label": "loan_rejection_form",
                                            "next": "sub1Slot1"                                        }
                                    ],
                                    "sub1Slot1": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "sub1Slot2"                                        }
                                    ],
                                    "sub1Slot2": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "loan_availed": {
                                    "initial": [
                                        {
                                            "label": "loan_availed_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "loan_availed_gs_form",
                                            "next": "subSlot2"                                        }
                                    ],
                                    "subSlot2": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot3"                                        }
                                    ],
                                    "subSlot3": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "not_interested": {
                                    "initial": [
                                        {
                                            "label": "not_interested_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested": {
                                    "initial": [
                                        {
                                            "label": "interested_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_personal": {
                                    "initial": [
                                        {
                                            "label": "interested_personal_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_others": {
                                    "initial": [
                                        {
                                            "label": "interested_others_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_later": {
                                    "initial": [
                                        {
                                            "label": "interested_later_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "loan_availed_gs": {
                                    "initial": [
                                        {
                                            "label": "loan_availed_gs_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot2"                                        }
                                    ],
                                    "subSlot2": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "another_product_pitch": {
                                    "initial": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    "fullerton_pl": {
                        "initial": [
                            {
                                "label": "lq_rpc_form",
                                "next": "slot1"                            }
                        ],
                        "slot1": [
                            {
                                "label": "sales_pitch_form",
                                "next": "slot2"                            }
                        ],
                        "slot2": [
                            {
                                "loan_rejected": {
                                    "initial": [
                                        {
                                            "label": "loan_rejection_form",
                                            "next": "sub1Slot1"                                        }
                                    ],
                                    "sub1Slot1": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "sub1Slot2"                                        }
                                    ],
                                    "sub1Slot2": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "loan_availed": {
                                    "initial": [
                                        {
                                            "label": "loan_availed_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "loan_availed_gs_form",
                                            "next": "subSlot2"                                        }
                                    ],
                                    "subSlot2": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot3"                                        }
                                    ],
                                    "subSlot3": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "not_interested": {
                                    "initial": [
                                        {
                                            "label": "not_interested_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested": {
                                    "initial": [
                                        {
                                            "label": "interested_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_personal": {
                                    "initial": [
                                        {
                                            "label": "interested_personal_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_others": {
                                    "initial": [
                                        {
                                            "label": "interested_others_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_later": {
                                    "initial": [
                                        {
                                            "label": "interested_later_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "loan_availed_gs": {
                                    "initial": [
                                        {
                                            "label": "loan_availed_gs_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot2"                                        }
                                    ],
                                    "subSlot2": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "another_product_pitch": {
                                    "initial": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    "fullerton_gl": {
                        "initial": [
                            {
                                "label": "lq_rpc_form",
                                "next": "slot1"                            }
                        ],
                        "slot1": [
                            {
                                "label": "sales_pitch_form",
                                "next": "slot2"                            }
                        ],
                        "slot2": [
                            {
                                "loan_rejected": {
                                    "initial": [
                                        {
                                            "label": "loan_rejection_form",
                                            "next": "sub1Slot1"                                        }
                                    ],
                                    "sub1Slot1": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "sub1Slot2"                                        }
                                    ],
                                    "sub1Slot2": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "loan_availed": {
                                    "initial": [
                                        {
                                            "label": "loan_availed_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "loan_availed_gs_form",
                                            "next": "subSlot2"                                        }
                                    ],
                                    "subSlot2": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot3"                                        }
                                    ],
                                    "subSlot3": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "not_interested": {
                                    "initial": [
                                        {
                                            "label": "not_interested_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested": {
                                    "initial": [
                                        {
                                            "label": "interested_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_personal": {
                                    "initial": [
                                        {
                                            "label": "interested_personal_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_others": {
                                    "initial": [
                                        {
                                            "label": "interested_others_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "interested_later": {
                                    "initial": [
                                        {
                                            "label": "interested_later_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "loan_availed_gs": {
                                    "initial": [
                                        {
                                            "label": "loan_availed_gs_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot2"                                        }
                                    ],
                                    "subSlot2": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                },
                                "another_product_pitch": {
                                    "initial": [
                                        {
                                            "label": "another_product_pitch_form",
                                            "next": "subSlot1"                                        }
                                    ],
                                    "subSlot1": [
                                        {
                                            "label": "stop_conversation"                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
}