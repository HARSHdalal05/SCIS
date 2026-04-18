CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  mobile_number VARCHAR(20) UNIQUE NOT NULL,
  is_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fitness_profile (
  id SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  age INTEGER NOT NULL,
  gender VARCHAR(20) NOT NULL,
  height_cm FLOAT NOT NULL,
  weight_kg FLOAT NOT NULL,
  body_fat_percent FLOAT,
  activity_level VARCHAR(40) NOT NULL,
  fitness_goal VARCHAR(40) NOT NULL,
  diet_type VARCHAR(40) NOT NULL,
  whey_protein BOOLEAN DEFAULT FALSE,
  workout_days_per_week INTEGER NOT NULL,
  training_level VARCHAR(20) DEFAULT 'beginner',
  bmi FLOAT,
  bmr FLOAT,
  daily_calories FLOAT,
  macro_protein_g FLOAT,
  macro_carbs_g FLOAT,
  macro_fats_g FLOAT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workout_plan (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  week_label VARCHAR(20) DEFAULT 'week-1',
  plan_json JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diet_plan (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  day_label VARCHAR(20) DEFAULT 'day-1',
  calories FLOAT NOT NULL,
  plan_json JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS progress_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  log_date DATE NOT NULL,
  workout_completed BOOLEAN DEFAULT FALSE,
  calories_consumed FLOAT DEFAULT 0,
  protein_intake_g FLOAT DEFAULT 0,
  weight_kg FLOAT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS avatar_state (
  id SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  muscle_visibility_index FLOAT DEFAULT 0.3,
  body_fat_estimate FLOAT DEFAULT 25,
  consistency_score FLOAT DEFAULT 0,
  muscle_group_visibility JSONB NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
