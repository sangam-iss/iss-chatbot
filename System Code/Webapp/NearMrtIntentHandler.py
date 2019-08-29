import pydialogflow_fulfillment as pf
from fuzzywuzzy import fuzz


class NearMrtIntentHandler:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,attraction_db):
        print("Handling Near MRT Intent")
        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message="Fetching Near MRT Details")

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

        print(f"near MRT for place :{place}")
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

        nearest_mrt = desired_place['nearestMrtStation']
        if nearest_mrt is not None and nearest_mrt!="":
            response = f"the nearest MRT station to {desired_place['name']} is {nearest_mrt}"
        else:
            response = "nearest MRT information is not available for this place"
        aog.add(pf.SimpleResponse(response,response))
        # new_output_context = pf.OutputContexts(parsed_query.get_project_id(),self.request_data["session"].split('/')[-1],
        #                                            'attractiondetailsintent-followup', 3,
        #                                            {'place-attraction': place})
        # aog.add(new_output_context)
        return aog.get_final_response()