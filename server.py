from fastapi import FastAPI, HTTPException, Query
import requests
import os
from typing import Any, List

app = FastAPI()

FILLOUT_API_KEY = os.getenv("FILLOUT_API_KEY")
FORM_ID = "wdUPwWRKVius"

if not FILLOUT_API_KEY:
    raise ValueError("FILLOUT_API_KEY environment variable is required")

def get_value(qs: List[dict], field_id: str) -> Any:
    """Get a specific question value by ID."""
    for q in qs:
        if q.get("id") == field_id:
            value = q.get("value")
            return None if value is None else value
    return None

def to_array(v: Any) -> List:
    """Convert value to array."""
    if isinstance(v, list):
        return v
    if v is None:
        return []
    return [v]

@app.get("/submission")
async def handle_submission(submissionId: str = Query(...)):
    try:
        if not FORM_ID or not submissionId:
            raise HTTPException(status_code=400, detail="Missing formId or submissionId")

        response = requests.get(
            f"https://api.fillout.com/v1/api/forms/{FORM_ID}/submissions/{submissionId}",
            headers={
                "Authorization": f"Bearer {FILLOUT_API_KEY}",
                "Content-Type": "application/json",
            }
        )
        response.raise_for_status()

        data = response.json()
        sub = data.get("submission", {})
        qs = sub.get("questions", []) if isinstance(sub.get("questions"), list) else []

        answers = {
            "submissionId": data.get("submissionId") or sub.get("submissionId") or submissionId,
            "submissionTime": data.get("submissionTime") or sub.get("submissionTime"),
            "lastUpdatedAt": data.get("lastUpdatedAt") or sub.get("lastUpdatedAt"),
            "startedAt": data.get("startedAt") or sub.get("startedAt"),

            "first_name": get_value(qs, "bRU5"),
            "surname": get_value(qs, "5Jej"),
            "email": get_value(qs, "5Tzw"),
            "phone": get_value(qs, "kAZP"),

            "dob": get_value(qs, "vdKq"),
            "gender": get_value(qs, "v1MV"),

            "skin_type": get_value(qs, "6nhN"),
            "skin_condition_awareness": get_value(qs, "92kP"),
            "sensitivity_score_1_to_5": get_value(qs, "5vKS"),

            "primary_concerns": to_array(get_value(qs, "d91n")),
            "additional_concerns": to_array(get_value(qs, "jiuG")),
            "other_concern_text": get_value(qs, "am5K"),

            "routine_selection": to_array(get_value(qs, "4CUf")),
            "medications_current": get_value(qs, "nihF"),
            "medications_names": get_value(qs, "4fhi"),
            "allergies_any": get_value(qs, "qMfk"),
            "allergies_list": get_value(qs, "9Hdy"),

            "source": get_value(qs, "qekf"),
            "pregnant_or_breastfeeding": get_value(qs, "cuog"),
        }

        return answers

    except requests.exceptions.RequestException as err:
        error_msg = "Internal server error"
        if err.response is not None:
            try:
                error_msg = err.response.json()
            except:
                error_msg = err.response.text

        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
