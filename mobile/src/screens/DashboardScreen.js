import React, { useCallback, useState } from 'react';
import { Alert, Button, ScrollView, Text, View } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import MuscleAvatar from '../components/MuscleAvatar';

export default function DashboardScreen({ navigation, session }) {
  const [data, setData] = useState(null);

  const load = useCallback(async () => {
    try {
      if (!session.userId) return;
      const d = await api.getDashboard(session.userId);
      setData(d);
    } catch (e) {
      Alert.alert('Dashboard Error', e.message);
    }
  }, [session.userId]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 10 }}>
      <Text>Dashboard</Text>
      <MuscleAvatar state={data?.avatar_state} />
      <Text>BMI: {data?.profile?.bmi ?? '-'}</Text>
      <Text>Calories: {data?.profile?.daily_calories ?? '-'}</Text>
      <Text>Progress Score: {data?.progress?.weekly_progress_score ?? '-'}</Text>
      <Text>Feedback: {data?.progress?.ai_feedback_summary ?? '-'}</Text>
      <View style={{ gap: 6 }}>
        {(data?.reminders || []).map((r, i) => (
          <Text key={i}>• {r}</Text>
        ))}
      </View>
      <Button title="Workout" onPress={() => navigation.navigate('Workout', { plan: data?.latest_workout })} />
      <Button title="Diet" onPress={() => navigation.navigate('Diet', { plan: data?.latest_diet })} />
      <Button title="Progress" onPress={() => navigation.navigate('Progress')} />
    </ScrollView>
  );
}
