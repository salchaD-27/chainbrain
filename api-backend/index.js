// api-gateway/index.js

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');

const authjs = require('./routes/auth')
const predictjs = require('./routes/predict')
const refreshtokenjs = require('./routes/refresh-token')
const predictionhistoryjs = require('./routes/predictionhistory')
const app = express();

// allowing reqs from frontend origin
app.use(cors({
  origin: 'http://localhost:3001',
  credentials: true, // if using cookies or auth headers
  allowedHeaders: ['Authorization', 'Content-Type'],
}));

// Middleware to parse JSON body requests
app.use(express.json());

// HTTP request logger middleware for logging incoming requests with details
app.use(morgan('combined'));


// Rate limiting middleware to limit repeated requests from same IP
const limiter = rateLimit({
  windowMs: 1 * 60 * 1000,  // 1 minute
  max: 60,                  // limit each IP to 60 requests per windowMs
  message: {
    error: 'Too many requests, please try again later.'
  }
});
app.use(limiter);


// POST /predict endpoint to receive prediction requests
app.use('/predict', predictjs);

// POST /api/auth -> auth.js (user auth login)
app.use('/api/auth', authjs)
// POST /api/refresh-token -> refresh-token.js
app.use('/api/refresh-token', refreshtokenjs)
// GET /api/prediction-history -> refresh-token.js
app.use('/api/prediction-history', predictionhistoryjs)

// Start the API Gateway server
const PORT = 4000;
app.listen(PORT, () => {
  console.log(`API Gateway listening on port ${PORT}`);
});
