const axios = require('axios');
const API_GATEWAY_URL = 'http://localhost:4000/predict';
const testPayloads = require('./testPayload.json')

async function runTests() {
  for (const payload of testPayloads) {
    try {
      const response = await axios.post(API_GATEWAY_URL, payload);
      console.log('Request:', payload);
      console.log('Response:', response.data);
      console.log('--------------------------');
    } catch (error) {
      console.error('Error for payload:', payload);
      if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
      } else {
        console.error('Error message:', error.message);
      }
      console.log('--------------------------');
    }
  }
}

runTests();