import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from './src/screens/LoginScreen';
import ProfileSetupScreen from './src/screens/ProfileSetupScreen';
import AILoadingScreen from './src/screens/AILoadingScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import WorkoutScreen from './src/screens/WorkoutScreen';
import DietScreen from './src/screens/DietScreen';
import ProgressScreen from './src/screens/ProgressScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  const [session, setSession] = useState({ token: null, userId: null });

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login">
          {(props) => <LoginScreen {...props} setSession={setSession} />}
        </Stack.Screen>
        <Stack.Screen name="ProfileSetup">
          {(props) => <ProfileSetupScreen {...props} session={session} />}
        </Stack.Screen>
        <Stack.Screen name="AILoading">
          {(props) => <AILoadingScreen {...props} session={session} />}
        </Stack.Screen>
        <Stack.Screen name="Dashboard">
          {(props) => <DashboardScreen {...props} session={session} />}
        </Stack.Screen>
        <Stack.Screen name="Workout">
          {(props) => <WorkoutScreen {...props} session={session} />}
        </Stack.Screen>
        <Stack.Screen name="Diet">
          {(props) => <DietScreen {...props} session={session} />}
        </Stack.Screen>
        <Stack.Screen name="Progress">
          {(props) => <ProgressScreen {...props} session={session} />}
        </Stack.Screen>
      </Stack.Navigator>
    </NavigationContainer>
  );
}
