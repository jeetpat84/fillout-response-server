# Fillout Submission API

FastAPI server that fetches form submissions from the Fillout API and returns parsed form answers.

## Local Setup

1. Clone the repository and navigate to this directory
2. Create a `.env` file with your API key:
   ```
   FILLOUT_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python server.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoint

### GET `/submission`

Query parameter:
- `submissionId` (required): The submission ID from Fillout

**Example:**
```
GET http://localhost:8000/submission?submissionId=YOUR_SUBMISSION_ID
```

**Response:**
```json
{
  "submissionId": "...",
  "submissionTime": "...",
  "first_name": "...",
  "email": "...",
  "skin_type": "...",
  ...
}
```

## Deployment on Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect the `render.yaml` configuration
6. Add the `FILLOUT_API_KEY` environment variable in the Render dashboard
7. Deploy!

The service will automatically rebuild and redeploy when you push changes to the main branch.

## Docker

Build and run locally with Docker:

```bash
docker build -t fillout-api .
docker run -p 8000:8000 -e FILLOUT_API_KEY=your_key_here fillout-api
```

## Documentation

Once running, visit `/docs` for interactive API documentation (Swagger UI).
# fillout-response-server
