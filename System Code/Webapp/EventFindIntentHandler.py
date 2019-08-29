import pydialogflow_fulfillment as pf
from getTouristDataUtil import TouristDatabase
from datetime import datetime

class EventFindIntentHandler:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,attraction_db):
        print("Handling EventFindIntentHandler")
        parsed_query = pf.DialogflowRequest(self.query)
        category = parsed_query.request_data["queryResult"]["parameters"].get("type", None)

        event_data = TouristDatabase(url='https://tih-api.stb.gov.sg', key='Pptc6mXV0ZbhNihfGOpAY94pj2m8WLUm').get_search_data(keyword=category)
        now = datetime.now()
        response = ""
        count=0

        for event in event_data:
            if count > 3:
                break
            start_date = datetime.strptime(event['startDate'], '%Y-%m-%dT%H:%M:%SZ')
            end_date = datetime.strptime(event['endDate'], '%Y-%m-%dT%H:%M:%SZ')
            delta = end_date - now
            print(delta.days)
            if delta.days > 1:
                count += 1
                text = f'{start_date.strftime("%d/%m")}-{end_date.strftime("%d/%m")} - {event["name"]}\n{event["description"]}\n'
                response = response + text
        if response == "":
            response = "There are no upcoming events right now!"
            ssml = response
        else:
            response = "These are some of the upcoming events.\n" + response
            ssml = "Here You Go!"

        aog = pf.dialogflow_response.DialogflowResponse(fulfillment_message=response)
        aog.add(pf.SimpleResponse(response,ssml))
        return aog.get_final_response()