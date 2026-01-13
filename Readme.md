# Data Cleaning Backend API

Django backend for the data cleaning application that normalizes inconsistent document data from an unreliable API.

## Features

- **Robust API Client**: Handles 30% error rate, slow responses with exponential backoff retry logic
- **Data Normalization**: Converts inconsistent field names, dates, and amounts to standard schema
- **Duplicate Removal**: Identifies and removes duplicate records
- **Validation**: Validates all required fields before submission
- **Batch Processing**: Full pipeline from fetch → normalize → submit

## API Endpoints

- `GET /api/fetch/` - Fetch raw data from external API
- `POST /api/normalize/` - Normalize raw data
- `POST /api/submit/` - Submit cleaned data
- `POST /api/process/` - Complete processing pipeline
- `GET /api/status/<task_id>/` - Check processing status

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
