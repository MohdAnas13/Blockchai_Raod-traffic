# Blockchain Event Tracker

This project consists of a FastAPI backend and a Streamlit frontend for tracking blockchain events.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Streamlit
- Requests

Install the dependencies using:

```bash
pip install -r requirements.txt
```

## Running the application

1.  Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

2.  Start the Streamlit frontend:

```bash
streamlit run streamlit_app.py
```

Open your browser and navigate to `http://localhost:8501` to view the Streamlit app.

## API Endpoints

### Add Event

-   Endpoint: `/add_event`
-   Method: POST
-   Request Body:

```json
{
    "vehicle_id": "string",
    "location": "string",
    "speed": float,
    "incident": "string (optional)"
}
```

### Get Chain

-   Endpoint: `/get_chain`
-   Method: GET

### Is Valid

-   Endpoint: `/is_valid`
-   Method: GET
