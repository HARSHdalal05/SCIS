const API_BASE =
  process.env.EXPO_PUBLIC_API_BASE ||
  process.env.REACT_APP_API_BASE ||
  'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const err = await response.text();
    throw new Error(err || 'API request failed');
  }
  return response.json();
}

export const api = {
  sendOtp: (mobile_number) => request('/auth/send-otp', { method: 'POST', body: JSON.stringify({ mobile_number }) }),
  verifyOtp: (mobile_number, otp) => request('/auth/verify-otp', { method: 'POST', body: JSON.stringify({ mobile_number, otp }) }),
  saveProfile: (userId, data) => request(`/user/profile?user_id=${userId}`, { method: 'POST', body: JSON.stringify(data) }),
  getDashboard: (userId) => request(`/dashboard/data?user_id=${userId}`),
  generateWorkout: (userId) => request(`/generate/workout?user_id=${userId}`, { method: 'POST' }),
  generateDiet: (userId) => request(`/generate/diet?user_id=${userId}`, { method: 'POST' }),
  updateProgress: (data) => request('/progress/update', { method: 'POST', body: JSON.stringify(data) }),
};
