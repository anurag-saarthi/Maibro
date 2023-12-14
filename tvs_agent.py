import json


flow_data = [
{
    "lead_generation": {
        "initial": [{
            "label": "lq_rpc_form",
            "next": "slot1"
        }],
        "slot1": [{
            "label": "sales_pitch_form",
            "next": "slot2"
        }],
        "slot2": [{
            "Interested": {
                "initial": [{
                    "flow": "lead_qualification",
                }]
            },
            "Not_Interested": {
                "initial": [{
                    "label": "Nurturing",
                    "next": "subSlot1"
                }],
                "subSlot1": [{
                    "label": "Nurturing",
                    "next": "subSlot2"
                }],
                "subSlot2": [{
                    "Interested": {
                        "initial": [{
                            "label": "Later_Date_Approach",
                            "next": "slot3"
                        }]
                    },
                    "Not_Interested": {
                        "initial": [{
                            "label": "Nurturing",
                            "next": "subsubSlot1"
                        }],
                        "subsubSlot1": [{
                            "label": "Later_Date_Approach",
                            "next": "subsubSlot2"
                        }],
                        "subsubSlot2": [{
                            "flow": "lead_qualification"
                        }]
                    }
                }],
                # "subSlot2": [{
                #     "label": "Later_Date_Approach",
                #     "next": "subSlot3"
                # }],
                "subSlot3": [{
                    "flow": "feed_back"
                }]
            }
        }],
        "slot3": [{
            "label": "Sales Pitch Message",
            "next": "slot2"
        }]
    }
},
{
    "lead_qualification": {
        "initial": [{
            "label": "lead_qualification_Questions",
            "next": "subSlot1"
        }],
        "subSlot1": [{
            "flow": "feed_back"
        }]
    }
},
{
    "feed_back": {
        "initial": [{
            "label": "stop_conversation"
        }]
    }
}]
























# flow_data = [
#                     {
#                     'kyc': {
#                     'initial': [{
#                         'label': 'lg_rpc_form',
#                         'next': 'slot1'
#                     }],
#                     'slot1': [{
#                         'label': 'spm_agent_branch_later_3_form',
#                         'next': 'slot2'
#                     }],
#                     'slot2': [{
#                         'visit_agent': {
#                             'initial': [{
#                                 'label': 'agent_visit_1_form',
#                                 'next': 'subSlot1'
#                             }],
#                             'subSlot1': [{
#                                 'label': 'beyond_tt_end_form',
#                                 'next': 'subSlot2'
#                                 }],
#                             'subSlot2': [{
#                                 'label': 'stop_conversation'
#                             }]
#                         },
#                         'visit_branch': {
#                             'initial': [{
#                                 'label': 'branch_visit_1_form',
#                                 'next': 'subSlot1'
#                             }],
#                             'subSlot1': [{
#                                 'label': 'beyond_tt_end_form',
#                                 'next': 'subSlot2'
#                             }],
#                             'subSlot2': [{
#                                 'label': 'stop_conversation'
#                             }]        
#                         },
#                         'interested_later': {
#                             'initial': [{
#                                 'label': 'interested_later_form',
#                                 'next': 'subSlot1'
#                             }],
#                             'subSlot1': [{
#                                 'label': 'stop_conversation'
#                             }]
#                         }
#                     }]
#                 },
#                     'follow_up': {
#                                 'initial': [{
#                                     'label': 'lg_rpc_form',
#                                     'next': 'slot1'
#                                 }],
#                                 'slot1': [{
#                                     'branch_visit':{
#                                         'initial': [{
#                                             'label':'spm_branch_visit_form',
#                                             'next': 'subSlot1'
#                                         }],
#                                         'subSlot1': [{
#                                             'affirm': {
#                                                 'initial': [{
#                                                     'label': 'branch_visit_1_form',
#                                                     'next': 'sub1Slot1'
#                                                 }],
#                                                 'sub1Slot1': [{
#                                                     'label': 'beyond_tt_end_form',
#                                                     'next': 'sub1Slot2'
#                                                 }],
#                                                 'sub1Slot2': [{
#                                                     'label': 'stop_conversation'
#                                                 }]
#                                             },
#                                             'nurturing': {
#                                                 'initial': [{
#                                                     'label': 'nurturing_agent_branch_2_form',
#                                                     'next': 'subSlot1'
#                                                 }],
#                                                 'subSlot1': [{
#                                                     'branch_visit': {
#                                                         'initial': [{
#                                                             'label': 'branch_visit_1_form',
#                                                             'next': 'sub2Slot1'
#                                                         }],
#                                                         'sub2Slot1': [{
#                                                             'label': 'beyond_tt_end_form',
#                                                             'next': 'sub3Slot1'
#                                                         }],
#                                                         'sub3Slot1':[{
#                                                             'label':'stop_conversation'
#                                                         }],
#                                                     },
#                                                     'agent_visit': {
#                                                         'initial': [{
#                                                             'label': 'agent_visit_1_form',
#                                                             'next': 'sub2Slot1'
#                                                         }],
#                                                         'sub2Slot1': [{
#                                                             'label': 'beyond_tt_end_form',
#                                                             'next': 'sub3Slot1'
#                                                         }],
#                                                         'sub3Slot1':[{
#                                                             'label':'stop_conversation'
#                                                         }],
#                                                     }
#                                                 }]
#                                             },
#                                             'interested_later': {
#                                                 'initial': [{
#                                                     'label': 'interested_later_form',
#                                                     'next': 'subSlot1'
#                                                 }],
#                                                 'subSlot1': [{
#                                                     'label': 'stop_conversation'
#                                                 }]
#                                             },
#                                             'beyond_tt':{
#                                                 'initial':[{
#                                                     'label':'beyond_tt_end_form',
#                                                     'next':'subSlot1'
#                                                 }],
#                                                 'subSlot1':[{
#                                                     'label': 'stop_conversation'
#                                                 }]
#                                             }
#                                         }]
#                                         },
#                                     'executive_visit': {
#                                         'initial': [{
#                                                 'label':'spm_agent_visit_form',
#                                                 'next': 'subSlot1'
#                                     }],
#                                         'subSlot1': [{
#                                             'agent_visit_1_form': {
#                                                 'initial': [{
#                                                     'label': 'agent_visit_1_form',
#                                                     'next': 'sub1Slot1'
#                                                 }],
#                                                 'sub1Slot1':[{
#                                                             'label': 'beyond_tt_end_form',
#                                                             'next': 'sub2Slot1'
#                                                 }],
#                                                 'sub2Slot1':[{
#                                                             'label': 'stop_conversation'
#                                                 }]
                                                    
#                                             },
#                                             'nurturing': {
#                                             'initial': [{
#                                                 'label': 'nurturing_agent_branch_2_form',
#                                                 'next': 'subSlot1'
#                                             }],
#                                             'subSlot1': [{
#                                                 'branch_visit': {
#                                                     'initial': [{
#                                                         'label': 'branch_visit_1_form',
#                                                         'next': 'sub2Slot1'
#                                                     }],
#                                                     'sub2Slot1': [{
#                                                         'label': 'beyond_tt_end_form',
#                                                         'next': 'sub3Slot1'
#                                                     }],
#                                                     'sub3Slot1':[{
#                                                         'label':'stop_conversation'
#                                                     }],
#                                                 },
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
#                                             'interested_later': {
#                                                 'initial': [{
#                                                     'label': 'interested_later_form',
#                                                     'next': 'subSlot1'
#                                                 }],
#                                                 'subSlot1': [{
#                                                     'label': 'stop_conversation'
#                                                 }]
#                                             },
#                                             'beyond_tt':{
#                                                 'initial':[{
#                                                     'label':'beyond_tt_end_form',
#                                                     'next':'subSlot1'
#                                                 }],
#                                                 'subSlot1':[{
#                                                     'label': 'stop_conversation'
#                                                 }]
#                                             }
#                                     }]
#                                     }
#                                 }],
                            
#                             }   
#                     }
#                 ]


flow_data =[{
			'fullerton_2wl': {
                        'initial': [{
                            'label': 'lq_rpc_form',
                            'next': 'slot1'
                        }],
                        'slot1': [{
                            'label': 'sales_pitch_form',
                            'next': 'slot2'
                        }],
                        'slot2': [{
                            'loan_rejected': {
                                'initial': [{
                                    'label': 'loan_rejection_form',
                                    'next': 'slot3'
                                }]
                            },
                            'loan_availed': {
                                'initial': [{
                                    'label': 'loan_availed_form',
                                    'next': 'subSlot1'
                                }],
                                'subSlot1': [{
                                    'label': 'loan_availed_gs_form',
                                    'next': 'slot3'
                                }]       
                            },
                            'not_interested':{
                                'initial': [{
                                    'label': 'not_interested_form',
                                    'next': 'subSlot1'
                                }],
                                'subSlot1': [{
                                    'label': 'stop_conversation'
                                }]

                            },
                            'interested_later': {
                                'initial': [{
                                    'label': 'interested_later_form',
                                    'next': 'subSlot1'
                                }],
                                'subSlot1': [{
                                    'label': 'stop_conversation'
                                }]
                            }, 
                            'loan_availed_gs':{
                                'initial': [{
                                    'label': 'loan_availed_gs_form',
                                    'next': 'slot3'
                                }]
                            }
                        }],
                        'slot3':[{
                                    'label':'another_product_pitch_form',
                                    'next': 'subSlot1'
                                }],
                                'subSlot1': [{
                                    'label': 'stop_conversation'
                                }]                              
            },
		
            'fullerton_pl':{
                    'initial': [{
                        'label': 'lq_rpc_form',
                        'next': 'slot1'
                    }],
                    'slot1': [{
                        'label': 'sales_pitch_form',
                        'next': 'slot2'
                    }],
                    'slot2': [{
                        'loan_rejected': {
                            'initial': [{
                                'label': 'loan_rejection_form',
                                'next': 'slot3'
                            }]
                        },
                        'loan_availed': {
                            'initial': [{
                                'label': 'loan_availed_form',
                                'next': 'subSlot1'
                            }],
                            'subSlot1': [{
                                'label': 'loan_availed_gs_form',
                                'next': 'slot3'
                            }]       
                        },
                        'interested_later': {
                            'initial': [{
                                'label': 'interested_later_form',
                                'next': 'subSlot1'
                            }],
                            'subSlot1': [{
                                'label': 'stop_conversation'
                            }]
                        }, 
                        'loan_availed_gs':{
                            'initial': [{
                                'label': 'loan_availed_gs_form',
                                'next': 'slot3'
                            }]
                        }
                    }],
                    'slot3':[{
                                'label':'another_product_pitch_form',
                                'next': 'subSlot1'
                            }],
                            'subSlot1': [{
                                'label': 'stop_conversation'
                            }]                              
            },

            'fullerton_gl':{
                    'initial': [{
                        'label': 'lq_rpc_form',
                        'next': 'slot1'
                    }],
                    'slot1': [{
                        'label': 'sales_pitch_form',
                        'next': 'slot2'
                    }],
                    'slot2': [{
                        'loan_rejected': {
                            'initial': [{
                                'label': 'loan_rejection_form',
                                'next': 'slot3'
                            }]
                        },
                        'loan_availed': {
                            'initial': [{
                                'label': 'loan_availed_form',
                                'next': 'subSlot1'
                            }],
                            'subSlot1': [{
                                'label': 'loan_availed_gs_form',
                                'next': 'slot3'
                            }]       
                        },
                        'interested_later': {
                            'initial': [{
                                'label': 'interested_later_form',
                                'next': 'subSlot1'
                            }],
                            'subSlot1': [{
                                'label': 'stop_conversation'
                            }]
                        }, 
                        'loan_availed_gs':{
                            'initial': [{
                                'label': 'loan_availed_gs_form',
                                'next': 'slot3'
                            }]
                        }
                    }],
                    'slot3':[{
                                'label':'another_product_pitch_form',
                                'next': 'subSlot1'
                            }],
                            'subSlot1': [{
                                'label': 'stop_conversation'
                            }]                              
            } 
        
}]


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
            ans = None
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
        # print("158data")
        # print(data1)
        if dispo in data1:
            temp_data = data1[dispo]["initial"][0]
            if "label" in temp_data:
                ans = data1[dispo]["initial"][0]["label"]
                # print("182",ans)
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
                ans = None
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
                        print("except")
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
            ans = None
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

# next_form = "lead_generation"
# next_data = flow_data [0][next_form]

# flow = "lead_generation"
# a=0
# for dict in flow_data:
#     for key in dict.keys():
#         if key==flow:
#             i=a
#         else:
#             a+=1
flow = "fullerton_2wl"
flow_list = [flow_data[0][flow]]
dispo = None
# flow_list= [{'initial': [{'label': 'lq_rpc_form', 'next': 'slot1'}], 'slot1': [{'label': 'sales_pitch_form', 'next': 'slot2'}], 'slot2': [{'loan_rejected': {'initial': [{'label': 'loan_rejection_form', 'next': 'slot3'}]}, 'loan_availed': {'initial': [{'label': 'loan_availed_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}, 'not_interested': {'initial': [{'label': 'not_interested_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'interested_later': {'initial': [{'label': 'interested_later_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'loan_availed_gs': {'initial': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}}], 'slot3': [{'label': 'another_product_pitch_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, [{'label': 'sales_pitch_form', 'next': 'slot2'}]]
# flow_list= [{'initial': [{'label': 'lq_rpc_form', 'next': 'slot1'}], 'slot1': [{'label': 'sales_pitch_form', 'next': 'slot2'}], 'slot2': [{'loan_rejected': {'initial': [{'label': 'loan_rejection_form', 'next': 'slot3'}]}, 'loan_availed': {'initial': [{'label': 'loan_availed_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}, 'not_interested': {'initial': [{'label': 'not_interested_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'interested_later': {'initial': [{'label': 'interested_later_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'loan_availed_gs': {'initial': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}}], 'slot3': [{'label': 'another_product_pitch_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, [{'loan_rejected': {'initial': [{'label': 'loan_rejection_form', 'next': 'slot3'}]}, 'loan_availed': {'initial': [{'label': 'loan_availed_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}, 'not_interested': {'initial': [{'label': 'not_interested_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'interested_later': {'initial': [{'label': 'interested_later_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'loan_availed_gs': {'initial': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}}]]
# dispo = "loan_rejected"
# flow_list =[{'initial': [{'label': 'lq_rpc_form', 'next': 'slot1'}], 'slot1': [{'label': 'sales_pitch_form', 'next': 'slot2'}], 'slot2': [{'loan_rejected': {'initial': [{'label': 'loan_rejection_form', 'next': 'slot3'}]}, 'loan_availed': {'initial': [{'label': 'loan_availed_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}, 'not_interested': {'initial': [{'label': 'not_interested_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'interested_later': {'initial': [{'label': 'interested_later_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'loan_availed_gs': {'initial': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}}], 'slot3': [{'label': 'another_product_pitch_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, [{'label': 'another_product_pitch_form', 'next': 'subSlot1'}]]
flow_list =[{'initial': [{'label': 'lq_rpc_form', 'next': 'slot1'}], 'slot1': [{'label': 'sales_pitch_form', 'next': 'slot2'}], 'slot2': [{'loan_rejected': {'initial': [{'label': 'loan_rejection_form', 'next': 'slot3'}]}, 'loan_availed': {'initial': [{'label': 'loan_availed_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}, 'not_interested': {'initial': [{'label': 'not_interested_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'interested_later': {'initial': [{'label': 'interested_later_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, 'loan_availed_gs': {'initial': [{'label': 'loan_availed_gs_form', 'next': 'slot3'}]}}], 'slot3': [{'label': 'another_product_pitch_form', 'next': 'subSlot1'}], 'subSlot1': [{'label': 'stop_conversation'}]}, [{'label': 'stop_conversation'}]]
print("dispo",dispo)
print("")
ans,next_form,flow_list = flow_mapping(flow_data,flow_list,dispo)
if ans == None:
    print("changing flow-------")
    print(flow_list)
    print("In middle-------")
    print(flow_list[-1])
    print("")
    ans,next_form,flow_list = flow_mapping(flow_data,flow_list,dispo)
print("ans: ",ans," next_form: ",next_form)
print("")
print(flow_list)
print("")
# print(flow_list[-1])
