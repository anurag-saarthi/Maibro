{
	"clientName": "TradeCred Testing",
	"agentName": "Payal",
	"domain": "Sales and onboarding",
	"subDomain": "Insurance",
	"productType": "investment platform",
	"parentFlow": [{
		"flow": "tradecred_lr_ip",
		"isParent": true,
		"isChild": false,
		"channel": ["Call"],
		"type": "Female",
		"language": ["English"],
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
		"tradecred_lr_ip": {
			"initial": [{
				"label": "lg_rpc_form",
				"next": "slot1"
			}],
			"slot1": [{
				"label": "sales_pitch_form",
				"next": "slot2"
			}],
			"slot2": [{
				"already_invested": {
					"initial": [{
						"label": "already_invested_form",
						"next": "subSlot1"
					}],
					"subSlot1": [{
						"label": "stop_conversation"
					}]
				},
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