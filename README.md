# FitMorph AI – Adaptive Fitness, Diet & Body Transformation MVP

Production-style MVP with FastAPI backend, PostgreSQL schema, rule-based AI engine, and React Native (Expo) mobile UI.

## Project Structure

```
SCIS/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── generate.py
│   │   │   ├── progress.py
│   │   │   └── dashboard.py
│   │   ├── services/
│   │   │   ├── ai_engine.py
│   │   │   └── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── schema.sql
│   └── .env.example
├── mobile/
│   ├── App.js
│   ├── package.json
│   └── src/
│       ├── api/client.js
│       ├── components/MuscleAvatar.js
│       └── screens/
│           ├── LoginScreen.js
│           ├── ProfileSetupScreen.js
│           ├── AILoadingScreen.js
│           ├── DashboardScreen.js
│           ├── WorkoutScreen.js
│           ├── DietScreen.js
│           └── ProgressScreen.js
└── docker-compose.yml
```

## Core Capabilities Implemented

- OTP mobile auth (mock OTP for MVP)
- User profile setup with body + fitness data
- BMI/BMR/calorie/macro calculation engine
- Rule-based workout generator (fat loss / muscle gain / beginner/advanced)
- Rule-based diet generator (veg/non-veg/vegan + whey support)
- Daily progress logging + weekly score + AI feedback
- Adaptive muscle-based avatar state (gradual visibility updates)
- Dashboard insights + reminders (workout/diet/missed-day alerts)

## Backend Setup (FastAPI + PostgreSQL)

1. Start PostgreSQL:

```bash
docker compose up -d
```

2. Setup backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# keep APP_ENV=development for local runs
uvicorn app.main:app --reload
```

3. Open docs: `http://localhost:8000/docs`

## Mobile Setup (React Native / Expo)

```bash
cd mobile
npm install
export EXPO_PUBLIC_API_BASE=http://localhost:8000
npm run start
```

> For emulator/device testing, change `API_BASE` in `mobile/src/api/client.js` from `localhost` to your machine LAN IP if needed.

## Required APIs

- `POST /auth/send-otp`
- `POST /auth/verify-otp`
- `POST /user/create`
- `POST /user/profile`
- `GET /user/profile`
- `POST /generate/workout`
- `POST /generate/diet`
- `POST /progress/update`
- `GET /dashboard/data`

## Example API Responses

### `POST /auth/verify-otp`

```json
{
  "token": "<jwt>",
  "user_id": 1,
  "is_new_user": true
}
```

### `POST /generate/workout?user_id=1`

```json
{
  "user_id": 1,
  "plan": {
    "weekly_plan": [
      {
        "day": 1,
        "focus": "Full Body + Cardio",
        "exercises": [
          {"exercise": "Goblet Squat", "sets": 2, "reps": "12-15", "rest_seconds": 60}
        ]
      }
    ]
  }
}
```

### `POST /generate/diet?user_id=1`

```json
{
  "user_id": 1,
  "plan": {
    "daily_calories": 2100,
    "macro_targets": {"protein_g": 156, "carbs_g": 220, "fats_g": 58},
    "meals": {
      "breakfast": {"calories": 525, "options": ["Oats + milk + nuts"]}
    }
  }
}
```

### `GET /dashboard/data?user_id=1`

```json
{
  "user_id": 1,
  "profile": {"bmi": 24.5, "daily_calories": 2100},
  "progress": {"weekly_progress_score": 71.4, "ai_feedback_summary": "Good progress"},
  "avatar_state": {
    "muscle_visibility_index": 0.42,
    "muscle_group_visibility": {"chest": 0.42, "abs": 0.32}
  },
  "reminders": ["Workout reminder...", "Diet reminder..."]
}
```

## Notes

- AI is intentionally lightweight and rule-based for MVP reliability.
- Avatar model is simplified SVG-based muscle visibility mapping (no heavy 3D dependency).
- Transformations are gradual and clamped for realistic progression.
