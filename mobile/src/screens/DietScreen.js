import React from 'react';
import { ScrollView, Text } from 'react-native';

export default function DietScreen({ route }) {
  const plan = route.params?.plan;
  return (
    <ScrollView contentContainerStyle={{ padding: 16, gap: 8 }}>
      <Text>Diet Plan</Text>
      <Text>Daily Calories: {plan?.daily_calories ?? '-'}</Text>
      {Object.entries(plan?.meals || {}).map(([meal, details]) => (
        <Text key={meal}>{`${meal}: ${details.calories} kcal | ${details.options.join(' / ')}`}</Text>
      ))}
    </ScrollView>
  );
}
