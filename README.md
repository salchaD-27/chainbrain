# ChainBrain: Ethereum Blockchain Anomaly Detection Dashboard

## Overview

ChainBrain is a full-stack blockchain analytics platform designed to analyze Ethereum block data in real-time, extract meaningful features, run machine learning-based anomaly detection, and provide an interactive dashboard for visualization and predictions. The system leverages Kafka for data streaming, a Python ML backend for inference, and a modern React/Next.js frontend for user interaction.

---

## Key Features

- **Real-Time Blockchain Data Ingestion**  
  Kafka consumer pipelines ingest Ethereum block data continuously, extracting Web3 features including transaction counts, gas usage, and token transfers.

- **Machine Learning Backend**  
  A FastAPI Python service running Random Forest models to detect anomalies or classify blocks based on extracted features.

- **API Gateway**  
  Express.js server providing REST endpoints for prediction requests with input validation, retry logic, caching, and persistent PostgreSQL storage for prediction history.

- **User Dashboard**  
  React/Next.js frontend enables authenticated user login, manual feature input for predictions, batch JSON upload of block data, and dynamic charts showing historical prediction trends.

- **Prediction History Persistence**  
  PostgreSQL schema stores prediction inputs and results with timestamps, supporting pagination and advanced analytics.

- **Robust Validation & Authentication**  
  TypeScript-based front-end validations, JWT-based secured API endpoints, and rate limiting ensure data integrity and security.

---

## Technologies Used

- Kafka (Data Streaming)  
- Python FastAPI (ML Backend)  
- Express.js & Node.js (API Gateway)  
- PostgreSQL (Database)  
- React & Next.js (Frontend)  
- Chart.js & react-chartjs-2 (Visualization)  
- TypeScript (Frontend Type Safety)  
- Docker (Optional Deployment Containerization)  

---

## Getting Started

### Backend Setup

1. Ensure you have a running Kafka broker and topics configured.
2. Setup PostgreSQL database and configure `DATABASE_URL` environment variable.
3. Run the Python ML backend FastAPI service on port `3000`.
4. Run the Express API Gateway on port `4000` (or as configured).

### Frontend Setup

1. Install dependencies and run the Next.js React frontend on your preferred port (e.g., `3001`).
2. Login using the authentication system.
3. Use the form or JSON upload to submit block data for prediction.
4. View real-time prediction results and interactive charts.


---

## Usage

- **Prediction:** Enter blockchain features manually or upload multiple blocks via JSON file to get anomaly predictions.
- **Visualization:** Explore historical prediction trends with interactive charts and filter options.
- **Authentication:** Secure access with user login and session management.
- **Persistence:** Prediction history stored in PostgreSQL for audit and analytics.

---
