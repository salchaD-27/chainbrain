// Validation middleware to check presence and types of required prediction features
function validatePredictionRequest(req, res, next) {
  const body = req.body;

  // List of required numeric fields with validation
  const numericFields = [
    'hour',
    'day_of_week',
    'transactionsCount',
    'gasUsed',
    'tokenTransfersCount',
    'totalTokenAmount',
    'uniqueSenders',
    'uniqueReceivers'
  ];

  for (const field of numericFields) {
    if (!(field in body)) {
      return res.status(400).json({ error: `Missing required field: ${field}` });
    }
    if (typeof body[field] !== 'number' || Number.isNaN(body[field])) {
      return res.status(400).json({ error: `Invalid type for field ${field}; expected number.` });
    }
  }

  // If all validations pass
  next();
}

module.exports = validatePredictionRequest