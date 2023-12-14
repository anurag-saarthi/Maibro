{
	"clientName": "Hero Housing Finance Testing",
	"agentName": "Priya",
	"domain": "Sales and onboarding",
	"subDomain": "Insurance",
	"productType": "home loan",
	"parentFlow": [{
		"flow": "herohousing_wc_hl",
		"isParent": true,
		"isChild": false,
		"channel": ["Call"],
		"type": "Female",
		"language": ["English","Hindi"],
		"Call": {
			"voice": "Saarthi TTS",
			"thresholdDateCallBack": 2,
			"thresholdTimeCallBack": 30
		},
		"Whatsapp": {
			"slotReminder": [{
				"slot0": 120,
				"slot1": 300
			}]
		},
		"startDate": "04/09/2022",
		"endDate": "04/09/2022",
		"startTime": 540,
		"endTime": 1120,
		"dispositionNextNudge": [{
			"value": "Interested",
			"nextFlow": "Feedback",
			"callBackTime": 120
		}, {
			"value": "Already Availed",
			"nextFlow": "Feedback",
			"callBackTime": 120
		}]
	}],
	"callFlow": [{
		"herohousing_wc_hl": {
			"initial": [{
				"label": "lg_rpc_form",
				"next": "slot1"
			}],
			"slot1": [{
				"label": "sales_pitch_form",
				"next": "slot2"
			}],
			"slot2": [{
				"not_interested": {
					"initial": [{
						"label": "already_renewed_form",
						"next": "subSlot1"
					}],
					"subSlot1": [{
						"label": "stop_conversation"
					}]
				},
				"deny_first_emi": {
					"initial": [{
						"label": "deny_first_emi_form",
						"next": "subSlot1"
					}],
					"subSlot1": [{
						"label": "stop_conversation"
					}]
				},
                "service_experience": {
					"initial": [{
						"label": "service_experience_form",
						"next": "subSlot1"
					}],
					"subSlot1": [{
						"label": "stop_conversation"
					}]
				},
                "deny_assistance": {
					"initial": [{
						"label": "deny_assistance_form",
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