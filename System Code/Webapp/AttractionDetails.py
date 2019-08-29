from fuzzywuzzy import fuzz
import pydialogflow_fulfillment as pf

class AttractionDetailsIntent:

    DEFAULT_RESPONSE = "Hello"
    DEFAULT_SPEECH_RESPONSE = "Here you Go. Select One of the card to proceed further"

    def __init__(self, query):
        self.query = query

    def handle_intent(self,attraction_db):
        print("Handling AttractionDetails Branch")
        print(self.query['queryText'])
        place = self.query['parameters'].get('place-attraction', None)
        desired_place = None
        max_index = 0;
        for attraction in attraction_db:
            index = fuzz.token_set_ratio(attraction['name'],place)
            if index >= 95:
                desired_place = attraction
                break
            elif max_index < index:
                max_index = index
                desired_place = attraction
        print(f'desired place is {desired_place["name"]}')
        aog = pf.dialogflow_response.DialogflowResponse()
        aog.add(pf.SimpleResponse(desired_place['description'],"Here you go!"))
        aog.add(pf.Suggestions(["Timing","Fare","Nearest MRT"]))
        return aog.get_final_response()