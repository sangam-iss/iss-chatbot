import pydialogflow_fulfillment as pf
from fuzzywuzzy import fuzz


class FareIntentHandler:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,attraction_db):
        print("Handling FareIntent")
        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message="Fetching Fare Details")
        parsed_query = pf.DialogflowRequest(self.query)
        output_context = parsed_query.get_single_ouputcontext('attractiondetailsintent-followup')
        place = parsed_query.request_data["queryResult"]["parameters"].get("place-attraction",None)

        if place is None or place == "":
            parameters = output_context.get('parameters',None)
            if parameters is None:
                aog.dialogflow_response["fulfillmentText"] = "I'm Sorry ! cannot retrieve place information"
                return aog.get_final_response()
            place = parameters['place-attraction']
            if place == "":
                aog.dialogflow_response["fulfillmentText"] = "I'm Sorry ! cannot retrieve place information"
                return aog.get_final_response()

        print(f"Fare for place :{place}")
        desired_place = None
        max_index = 0
        for attraction in attraction_db:
            index = fuzz.token_set_ratio(attraction['name'],place)
            if index >= 95:
                desired_place = attraction
                break
            elif max_index < index:
                max_index = index
                desired_place = attraction
        adult_price = desired_place['pricing']['adult']
        child_price = desired_place['pricing']['child']
        if adult_price is not None and adult_price!="":
            response = "Adult price is "+adult_price
            if child_price is not None and child_price!="":
                response = response + " and the child price is "+child_price
        else:
            response = "Price Information of the place is not available"
        aog.add(pf.SimpleResponse(response,"These are the prices of "+desired_place['name']))
        # new_output_context = pf.OutputContexts(parsed_query.get_project_id(),self.request_data["session"].split('/')[-1],
        #                                            'attractiondetailsintent-followup', 3,
        #                                            {'place-attraction': place})
        # aog.add(new_output_context)
        return aog.get_final_response()