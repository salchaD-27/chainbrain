const express = require('express')
const axios = require('axios');
const {Pool} = require('pg');
const router = express.Router();
const validatePredictionRequest = require('../middleware/validatePredictionRequest')

// ML backend endpoint URL
const ML_BACKEND_URL = 'http://localhost:3000/predict';


const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Create prediction_history table if it doesn't exist (run once at startup)
(async () => {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS prediction_history (
        id SERIAL PRIMARY KEY,
        hour INT NOT NULL,
        day_of_week INT NOT NULL,
        transactionsCount INT NOT NULL,
        gasUsed BIGINT NOT NULL,
        tokenTransfersCount INT NOT NULL,
        totalTokenAmount BIGINT NOT NULL,
        uniqueSenders INT NOT NULL,
        uniqueReceivers INT NOT NULL,
        prediction INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log('prediction_history table ready.');
  } catch (error) {
    console.error('Error creating prediction_history table:', error);
  }
})();


// Function to save prediction record into DB asynchronously
async function savePredictionRecord(features, prediction) {
  // Use parameterized query to avoid SQL injection
  const query = `
    INSERT INTO prediction_history (
      hour, day_of_week, transactionsCount, gasUsed,
      tokenTransfersCount, totalTokenAmount, uniqueSenders,
      uniqueReceivers, prediction
    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
    RETURNING id
  `;
  const values = [
    features.hour,
    features.day_of_week,
    features.transactionsCount,
    features.gasUsed,
    features.tokenTransfersCount,
    features.totalTokenAmount,
    features.uniqueSenders,
    features.uniqueReceivers,
    prediction
  ];

  try {
    const result = await pool.query(query, values);
    console.log('Saved prediction record with id:', result.rows[0].id);
  } catch (dbError) {
    console.error('Error saving prediction record:', dbError);
  }
}






// Simple in-memory cache object to store responses keyed by request JSON string
// Note: For production use consider a Redis or persistent cache instead
const cache = new Map();

/**
 * Retry helper function to retry async operations multiple times with delay.
 * @param {Function} fn - async function to retry
 * @param {number} retries - number of retries
 * @param {number} delay - delay in milliseconds between retries
 */
const retryRequest = async (fn, retries = 3, delay = 1000) => {
  try {
    return await fn();
  } catch (err) {
    if (retries <= 0) throw err;
    console.warn(`Retrying request... attempts left: ${retries}, error: ${err.message}`);
    await new Promise(r => setTimeout(r, delay));
    return retryRequest(fn, retries - 1, delay);
  }
};

// POST /predict endpoint to receive prediction requests
router.post('/', validatePredictionRequest, async (req, res) => {
  const requestBody = req.body;

  // Use request JSON string as cache key
  const key = JSON.stringify(requestBody);

  if (cache.has(key)) {
    // Return cached prediction result
    console.log('Cache hit for request:', key);
    return res.json(cache.get(key));
  }

  try {
    // Call ML backend with retries
    const response = await retryRequest(() => axios.post(ML_BACKEND_URL, requestBody));
    const predictionData = response.data;

    // Cache the response data for future identical requests
    cache.set(key, predictionData);
    res.json(predictionData);

    // Save to DB asynchronously, don't wait for it before responding
    if (typeof predictionData.prediction === 'number') {savePredictionRecord(requestBody, predictionData.prediction);}
    else {console.warn('Prediction data missing prediction number:', predictionData);}
    
  } catch (error) {
    console.error('ML Backend request failed:', error.message);
    res.status(502).json({ error: "Bad Gateway: ML backend unavailable" });
  }
});


module.exports=router