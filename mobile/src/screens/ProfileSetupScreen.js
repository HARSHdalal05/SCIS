import React, { useState } from 'react';
import { Alert, Button, ScrollView, Text, TextInput } from 'react-native';
import { api } from '../api/client';

export default function ProfileSetupScreen({ navigation, session }) {
  const [form, setForm] = useState({
    age: '28',
    gender: 'male',
    height_cm: '175',
    weight_kg: '78',
    body_fat_percent: '22',
    activity_level: 'moderate',
    fitness_goal: 'fat loss',
    diet_type: 'veg',
    whey_protein: 'false',
    workout_days_per_week: '5',
    training_level: 'beginner',
  });

  const onSave = async () => {
    try {
      if (!session.userId) return Alert.alert('Missing user session');
      const payload = {
        ...form,
        age: Number(form.age),
        height_cm: Number(form.height_cm),
        weight_kg: Number(form.weight_kg),
        body_fat_percent: Number(form.body_fat_percent),
        whey_protein: String(form.whey_protein).toLowerCase() === 'true',
        workout_days_per_week: Number(form.workout_days_per_week),
      };
      await api.saveProfile(session.userId, payload);
      navigation.replace('AILoading', { userId: session.userId });
    } catch (e) {
      Alert.alert('Profile Error', e.message);
    }
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 8 }}>
      <Text>Profile Setup</Text>
      {Object.keys(form).map((k) => (
        <TextInput
          key={k}
          value={String(form[k])}
          onChangeText={(v) => setForm((p) => ({ ...p, [k]: v }))}
          placeholder={k}
          accessibilityLabel={`Profile field ${k}`}
          accessibilityHint={`Enter value for ${k}`}
          style={{ borderWidth: 1, padding: 10 }}
        />
      ))}
      <Button title="Generate AI Plans" onPress={onSave} />
    </ScrollView>
  );
}
