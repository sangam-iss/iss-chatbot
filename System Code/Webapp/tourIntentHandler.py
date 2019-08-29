import pydialogflow_fulfillment as pf
from fuzzywuzzy import fuzz
from getTouristDataUtil import TouristDatabase


class TourIntentHandler:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,attraction_db):
        print("Handling Tour Intent")
        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message="Fetching Tour Details")

        parsed_query = pf.DialogflowRequest(self.query)
        place = parsed_query.request_data["queryResult"]["parameters"].get("type",None)

        tour_data = TouristDatabase(url='https://tih-api.stb.gov.sg',
                                     key='Pptc6mXV0ZbhNihfGOpAY94pj2m8WLUm').get_tour_data(category=place)

        count = 0
        for tour in tour_data:
            response = ""
            count+=1
            if count >= 3:
                break
            response = response + f"{tour['name']}:\n"
            response = response + f"{tour['description']}\n\n"
            response = response + f"Contact: {tour['officialEmail']}\n"
            aog.add(pf.SimpleResponse(response, "Here You go!"))
        return aog.get_final_response()
