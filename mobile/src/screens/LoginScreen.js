import React, { useState } from 'react';
import { Alert, Button, Text, TextInput, View } from 'react-native';
import { api } from '../api/client';

export default function LoginScreen({ navigation, setSession }) {
  const [mobile, setMobile] = useState('');
  const [otp, setOtp] = useState('123456');

  const handleLogin = async () => {
    try {
      await api.sendOtp(mobile);
      const verified = await api.verifyOtp(mobile, otp);
      setSession({ token: verified.token, userId: verified.user_id });
      navigation.navigate('ProfileSetup');
    } catch (e) {
      Alert.alert('Auth Error', e.message);
    }
  };

  return (
    <View style={{ padding: 16, gap: 10 }}>
      <Text>FitMorph AI Login (OTP)</Text>
      <TextInput
        placeholder="Mobile number"
        value={mobile}
        onChangeText={setMobile}
        keyboardType="phone-pad"
        accessibilityLabel="Mobile number"
        accessibilityHint="Enter your mobile number"
        style={{ borderWidth: 1, padding: 10 }}
      />
      <TextInput
        placeholder="OTP"
        value={otp}
        onChangeText={setOtp}
        keyboardType="number-pad"
        secureTextEntry
        accessibilityLabel="OTP code"
        accessibilityHint="Enter the one-time password sent to your phone"
        style={{ borderWidth: 1, padding: 10 }}
      />
      <Button title="Login" onPress={handleLogin} />
      <Text>Use OTP: 123456 (MVP mock)</Text>
    </View>
  );
}
