import pydialogflow_fulfillment as pf
import json

class OneDayIntentHandler:

    types = {
        "adventure":"Adventure",
        "education":"TopAttractions",
        "family":"Sentosa",
        "leisure":"Nature",
        "recreation":"Leisure",
        "shopping":"TopAttractions",
        "sports":"Adventure",
        "temple":"Heritage"
    }

    def __init__(self,query):
        self.query = query
        self.response = {}
        self.file = "oneDay.json"

    def handle_intent(self,attraction_db):
        print("Handling OneDayIntentHandler")

        parsed_query = pf.DialogflowRequest(self.query)
        ct = parsed_query.get_paramter('type')
        file_name = OneDayIntentHandler.types[ct]+".txt"
        with open(file_name,"r") as fh:
            response_list = fh.readlines()
        response = "\n".join(response_list)
        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message=response)
        aog.add(pf.SimpleResponse(response,"Here is your One Day Itinerary."))
        return aog.get_final_response()