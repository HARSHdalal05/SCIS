import React, { useEffect } from 'react';
import { ActivityIndicator, Text, View } from 'react-native';
import { api } from '../api/client';

export default function AILoadingScreen({ navigation, route, session }) {
  useEffect(() => {
    const run = async () => {
      const userId = route?.params?.userId || session?.userId;
      if (!userId) {
        navigation.replace('Login');
        return;
      }
      try {
        await Promise.all([api.generateWorkout(userId), api.generateDiet(userId)]);
      } finally {
        navigation.replace('Dashboard');
      }
    };
    run();
  }, [navigation, route?.params?.userId, session?.userId]);

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', gap: 8 }}>
      <ActivityIndicator size="large" />
      <Text>Generating adaptive AI workout & diet plans...</Text>
    </View>
  );
}
