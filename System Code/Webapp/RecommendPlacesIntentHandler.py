import pydialogflow_fulfillment as pf


class ActivateRecommendIntentHandler:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,attraction_db):
        print("Handling ActivateRecommendIntentHandler")
        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message="ActivateRecommendIntentHandler")
        aog.add(pf.SimpleResponse("activating recommend handler","activating recommend handler"))
        return aog.get_final_response()
