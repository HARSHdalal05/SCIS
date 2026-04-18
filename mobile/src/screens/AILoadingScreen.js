import React from 'react';
import { ActivityIndicator, Text, View } from 'react-native';

export default function AILoadingScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', gap: 8 }}>
      <ActivityIndicator size="large" />
      <Text>Generating adaptive AI workout & diet plans...</Text>
    </View>
  );
}
