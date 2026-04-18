import React, { useState } from 'react';
import { Alert, Button, ScrollView, Text, TextInput } from 'react-native';
import { api } from '../api/client';

export default function ProgressScreen({ session }) {
  const [log, setLog] = useState({
    log_date: new Date().toISOString().slice(0, 10),
    workout_completed: 'true',
    calories_consumed: '2000',
    protein_intake_g: '120',
    weight_kg: '77',
    notes: 'Good day',
  });
  const [result, setResult] = useState(null);

  const submit = async () => {
    try {
      const payload = {
        user_id: session.userId,
        log_date: log.log_date,
        workout_completed: String(log.workout_completed).toLowerCase() === 'true',
        calories_consumed: Number(log.calories_consumed),
        protein_intake_g: Number(log.protein_intake_g),
        weight_kg: Number(log.weight_kg),
        notes: log.notes,
      };
      const res = await api.updateProgress(payload);
      setResult(res);
    } catch (e) {
      Alert.alert('Progress Error', e.message);
    }
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 8 }}>
      <Text>Daily Progress Tracker</Text>
      {Object.keys(log).map((k) => (
        <TextInput
          key={k}
          value={String(log[k])}
          onChangeText={(v) => setLog((p) => ({ ...p, [k]: v }))}
          placeholder={k}
          accessibilityLabel={`Progress field ${k}`}
          accessibilityHint={`Enter value for ${k}`}
          style={{ borderWidth: 1, padding: 10 }}
        />
      ))}
      <Button title="Update Progress" onPress={submit} />
      {result && <Text>{`Score: ${result.weekly_progress_score} | ${result.ai_feedback_summary}`}</Text>}
    </ScrollView>
  );
}
