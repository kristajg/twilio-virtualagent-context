const http = require('http');
const express = require('express');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.post('/dialogflow-fulfillment-webhook', (req, res) => {
  console.log('Dialogflow fulfillment webhook hit ', req.body);
  return res.json({
    fulfillmentText: `Perfect, thank you`, // Dialogflow's closing remarks before switching back to Studio
    end_interaction: true, // Manually ends the caller interaction with Dialogflow
  });
});

// Storing in a global variable is the easiest way to demonstrate passing context
// However, it is ephemeral and not secure. 
// Other options for data storage: airtable, database, redis, JSON / text file
let generalData = '';
let stepOneData = '';
let stepTwoData = '';
app.post('/virtual-agent-callback', (req, res) => {
  console.log('Twilio Virtual Agent callback hit');
  const {
    query: {
      step = '',
    },
    body: {
      QueryText = '',
    },
  } = req;
  console.log('QueryText from Dialogflow is: ', QueryText);
  if (QueryText) {
    if (step === 'one') {
      stepOneData = QueryText;
    }
    if (step === 'two') {
      stepTwoData = QueryText;
    }
    generalData = QueryText;
  }
});

app.post('/get-stored-dialogflow-data', (req, res) => {
  console.log('Get stored Dialogflow data hit');
  const { step } = req.query;
  let payload = {};
  if (step === 'one') {
    payload = { stepOneData };
  } else if (step === 'two') {
    payload = { stepTwoData };
  } else {
    payload = { generalData };
  }
  res.json(payload);
});

http.createServer(app).listen(8081, () => {
  console.log('Express server listening on port 8081');
});
