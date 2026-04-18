import React from 'react';
import { ScrollView, Text } from 'react-native';

export default function WorkoutScreen({ route }) {
  const plan = route.params?.plan;
  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 8 }}>
      <Text>Workout Plan</Text>
      {(plan?.weekly_plan || []).map((d) => (
        <Text key={d.day}>{`Day ${d.day} (${d.focus}): ${d.exercises.map((e) => e.exercise).join(', ')}`}</Text>
      ))}
    </ScrollView>
  );
}
