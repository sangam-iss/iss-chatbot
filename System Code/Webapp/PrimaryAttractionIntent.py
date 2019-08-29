import pydialogflow_fulfillment as pf


class PrimaryAttractionIntent:
    DEFAULT_RESPONSE = """1. Merlion Park\n2. Gardens by the Bay\n3. Universal Studios Singapore\n\nWould you like to explore more attractions ?"""
    DEFAULT_SPEECH_RESPONSE = "These are some of the Top attractions I could find in Singapore. Would you like to explore more attractions ?"

    def __init__(self,query):
        self.query = query
        self.response = {}


    def handle_intent(self):
        print("Handling PrimaryAttractionIntent")
        location = self.query['parameters'].get('geo-city',None)
        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message=PrimaryAttractionIntent.DEFAULT_RESPONSE)
        if location is not None and location != "" and location.lower() != "singapore":
            print(location)
            aog.add(pf.SimpleResponse("Sorry. We support only singapore location.",
                                      "Sorry. We support only singapore location."))
            return aog.get_final_response()
        aog.add(pf.SimpleResponse(PrimaryAttractionIntent.DEFAULT_RESPONSE,
                                  PrimaryAttractionIntent.DEFAULT_SPEECH_RESPONSE))
        return aog.get_final_response()