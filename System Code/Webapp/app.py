from flask import Flask
from flask import request,jsonify
from PrimaryAttractionIntent import PrimaryAttractionIntent
from AttractionDetails import AttractionDetailsIntent
import pydialogflow_fulfillment as pf
from TimingIntentHandler import TimingIntentHandler
from NearMrtIntentHandler import NearMrtIntentHandler
from FareIntentHandler import FareIntentHandler
from OneDayIntentHandler import OneDayIntentHandler
from EventFindIntentHandler import EventFindIntentHandler
from ActivateRecommendIntentHandler import ActivateRecommendIntentHandler
from tourIntentHandler import TourIntentHandler
import json

app = Flask(__name__)

attraction_db = None


def make_default_response(response):
    ff_response = pf.dialogflow_response.DialogflowResponse()
    ff_response.add(pf.SimpleResponse(response,response))
    return ff_response.get_final_response()


def make_error_response(code):
    response = f"Sorry ! unable to process your request! Error - {code}"
    return make_default_response(response)


@app.before_first_request
def get_database():
    global attraction_db
    with open('tourist_data_clean.json') as fh:
        attraction_db = json.load(fh)
    print(attraction_db[0])


@app.route('/v1/tourism/',methods=['POST'])

def intent_resolver():
    req = request.get_json()
    print("\n\n")
    print(req)
    print("\n\n")
    query = req.get('queryResult',None)
    if query is None:
        return jsonify(make_error_response("Query Result is Empty"))
    intent = query.get('intent')
    if intent is None:
        return jsonify(make_error_response("intent is Empty"))
    intent_name = intent.get("displayName", "defaultResponse")

    if intent_name == "AttractionIntent":
        intent_handler = PrimaryAttractionIntent(query)
        response = intent_handler.handle_intent()
    elif intent_name == "AttractionDetailsIntent":
        intent_handler = AttractionDetailsIntent(query)
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "TimingIntent" or intent_name == "TimingWithPlaceIntent":
        intent_handler = TimingIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "NearMrtIntent" or intent_name == "NearMrtWithPlaceIntent":
        intent_handler = NearMrtIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "FareIntent" or intent_name == "FareWithPlaceIntent":
        intent_handler = FareIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "AttractionIntentPositiveBranchSelection":
        intent_handler = AttractionDetailsIntent(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "EventFindIntent":
        intent_handler = EventFindIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "ActivateRecommendIntent":
        intent_handler = ActivateRecommendIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "RecommendPlacesIntent":
        intent_handler = ActivateRecommendIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "OneDayTourIntent":
        intent_handler = OneDayIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    elif intent_name == "TourIntent":
        intent_handler = TourIntentHandler(json.dumps(req))
        response = intent_handler.handle_intent(attraction_db)
    else:
        response = make_default_response("Intent Matching Failed, Can you please rephrase the question")
    print("\n\n")
    print(response)
    print("\n\n")
    return response

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
