{
	"clientName": "Manappuram Finance Testing",
	"agentName": "Meera",
	"domain": "Sales and onboarding",
	"subDomain": "Insurance",
	"productType": "personal loan",
	"parentFlow": [{
		"flow": "manappuram_lg_pl",
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
		"manappuram_lg_pl": {
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