from flask import Flask, request
app = Flask(__name__)

@app.route('/dialogflow-fulfillment-webhook', methods=['POST'])
def dialogflowFulfillmentWebhook():
  print('Dialogflow fulfillment webhook hit.')
  if request.method == 'POST':
    resp = {
      'fulfillmentText': 'Perfect, thank you', # Dialogflow's closing remarks before switching back to Studio
      'end_interaction': True, # Manually ends the caller interaction with Dialogflow
    }
    return resp
  else:
    print('Please use the POST method type')

# Storing in a global variable is the easiest way to demonstrate passing context
# However, it is ephemeral and not secure. 
# Other options for data storage: airtable, database, redis, JSON / text file
generalData = ''
stepOneData = ''
stepTwoData = ''
@app.route('/virtual-agent-callback', methods=['POST'])
def virtualAgentCallback():
  print('Twilio Virtual Agent callback hit')
  if request.method == 'POST':
    bodyDict = request.form.to_dict()
    queryText = bodyDict.get('QueryText')
    if queryText:
      print('QueryText from Dialogflow is: ', queryText)

      # OPTIONAL:
      # If there is more than one VirtualAgent widget in the Studio flow
      # and they need to be designated from each other, add a query string
      # in the callback URL saved in the widget. For example, ?step=one
      step = request.args.get('step')
      if step == 'one':
        stepOneData = queryText
      elif step == 'two':
        stepTwoData = queryText
      else:
        generalData = queryText
    else:
      print('No QueryText returned')
  else:
    print('Please use the POST method type')
  # return no content
  return ('', 204)

@app.route('/get-stored-dialogflow-data', methods=['POST'])
def getDialogflowDataCallback():
  print('Get stored Dialogflow data hit')
  step = request.args.get('step')
  payload = {}
  if step == 'one':
    payload = { 'stepOneData': stepOneData }
  elif step == 'two':
    payload = { 'stepTwoData': stepTwoData }
  else:
    payload = { 'generalData': generalData }
  # return payload
  return { 'name': 'Krista' }


if __name__ == '__main__':
    app.run(host="localhost", port=8081, debug=True)
