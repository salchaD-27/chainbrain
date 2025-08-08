const express = require('express');
const router = express.Router();
const { Pool } = require('pg');
const authenticateToken = require('../middleware/authenticateToken')

// PostgreSQL pool configuration
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// GET /api/prediction-history/
// Supports optional query params: page (default 1), limit (default 20)
router.get('/', authenticateToken, async (req, res) => {
  try {
    // Parse pagination query parameters, with defaults
    const page = Math.max(parseInt(req.query.page) || 1, 1);
    const limit = Math.min(Math.max(parseInt(req.query.limit) || 20, 1), 100); // Max 100 per page
    const offset = (page - 1) * limit;

    // Query total count for pagination
    const countResult = await pool.query('SELECT COUNT(*) FROM prediction_history');
    const totalCount = parseInt(countResult.rows[0].count);
    const totalPages = Math.ceil(totalCount / limit);

    // Query paginated prediction history records ordered by latest first
    const queryText = `
      SELECT 
        id,
        hour,
        day_of_week,
        transactionsCount,
        gasUsed,
        tokenTransfersCount,
        totalTokenAmount,
        uniqueSenders,
        uniqueReceivers,
        prediction,
        created_at
      FROM prediction_history
      ORDER BY created_at DESC
      LIMIT $1 OFFSET $2
    `;
    const { rows } = await pool.query(queryText, [limit, offset]);

    res.json({
      page,
      limit,
      totalCount,
      totalPages,
      data: rows,
    });
  } catch (error) {
    console.error('Error fetching prediction history:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
