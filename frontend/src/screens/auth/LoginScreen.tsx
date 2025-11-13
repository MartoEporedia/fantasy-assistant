import React, { useState } from 'react';
import { View, StyleSheet, Image } from 'react-native';
import { TextInput, Button, Text, Snackbar } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';

export default function LoginScreen({ navigation }: any) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { signIn } = useAuth();

  const handleLogin = async () => {
    if (!username || !password) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await signIn(username, password);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text variant="displaySmall" style={styles.title}>⚽ Fantasy Assistant</Text>
        <Text variant="bodyLarge" style={styles.subtitle}>Sign in to your account</Text>

        <TextInput
          label="Username"
          value={username}
          onChangeText={setUsername}
          mode="outlined"
          style={styles.input}
          autoCapitalize="none"
        />

        <TextInput
          label="Password"
          value={password}
          onChangeText={setPassword}
          mode="outlined"
          secureTextEntry
          style={styles.input}
        />

        <Button
          mode="contained"
          onPress={handleLogin}
          loading={loading}
          disabled={loading}
          style={styles.button}
        >
          Sign In
        </Button>

        <Button
          mode="text"
          onPress={() => navigation.navigate('Register')}
          style={styles.linkButton}
        >
          Don't have an account? Sign Up
        </Button>
      </View>

      <Snackbar
        visible={!!error}
        onDismiss={() => setError('')}
        duration={3000}
      >
        {error}
      </Snackbar>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#00a86b',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: 'white',
    marginTop: 100,
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
  },
  title: {
    textAlign: 'center',
    marginBottom: 10,
    fontWeight: 'bold',
  },
  subtitle: {
    textAlign: 'center',
    marginBottom: 30,
    color: '#666',
  },
  input: {
    marginBottom: 15,
  },
  button: {
    marginTop: 10,
    paddingVertical: 5,
  },
  linkButton: {
    marginTop: 10,
  },
});
