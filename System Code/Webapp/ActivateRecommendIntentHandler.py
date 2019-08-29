import pydialogflow_fulfillment as pf


class ActivateRecommendIntentHandler:

    types = {
        "adventure":["Adventure","Hills and Trek"],
        "education":["Education","Museums","History"],
        "family":["Top Attraction","Fun and Entertainment","Top Attractions"],
        "leisure":["Nature","Leisure & Recreation","Resorts","Beaches","Top Attractions"],
        "recreation":["Theatre","Zoo","Top Attractions"],
        "shopping":["Shopping"],
        "sports":["Sports and Games"],
        "temple":["Religion and Culture","History & Culture"]
    }

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,attraction_db):
        print("Handling ActivateRecommendIntentHandler")
        parsed_query = pf.DialogflowRequest(self.query)
        category = parsed_query.get_paramter('type')
        response = []
        for data in attraction_db:
            if data["type"] in ActivateRecommendIntentHandler.types[category]:
                response.append(data)
                if len(response) >=5:
                    break
        response_string = "Recommendation based on your selection:\n"
        for data in response:
            text = f"{data['name']}\n"
            response_string = response_string + text

        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message=response_string)
        aog.add(pf.SimpleResponse(response_string,"Here are some of the top attractions based on your preference."))
        return aog.get_final_response()