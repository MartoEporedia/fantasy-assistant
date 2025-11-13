import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Text, Button, Divider, List, Avatar } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';

export default function ProfileScreen() {
  const { user, signOut } = useAuth();

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content style={styles.profileHeader}>
          <Avatar.Text
            size={80}
            label={user?.username.substring(0, 2).toUpperCase() || 'U'}
            style={styles.avatar}
          />
          <Text variant="headlineMedium" style={styles.username}>
            {user?.username}
          </Text>
          <Text variant="bodyLarge" style={styles.email}>
            {user?.email}
          </Text>
          {user?.full_name && (
            <Text variant="bodyMedium" style={styles.fullName}>
              {user.full_name}
            </Text>
          )}
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">Account Settings</Text>
          <Divider style={styles.divider} />

          <List.Item
            title="Edit Profile"
            left={(props) => <List.Icon {...props} icon="account-edit" />}
            onPress={() => {}}
          />
          <List.Item
            title="Change Password"
            left={(props) => <List.Icon {...props} icon="lock-reset" />}
            onPress={() => {}}
          />
          <List.Item
            title="Notifications"
            left={(props) => <List.Icon {...props} icon="bell" />}
            onPress={() => {}}
          />
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">App Settings</Text>
          <Divider style={styles.divider} />

          <List.Item
            title="Theme"
            description="Light"
            left={(props) => <List.Icon {...props} icon="palette" />}
            onPress={() => {}}
          />
          <List.Item
            title="Language"
            description="English"
            left={(props) => <List.Icon {...props} icon="translate" />}
            onPress={() => {}}
          />
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">Support</Text>
          <Divider style={styles.divider} />

          <List.Item
            title="Help & FAQ"
            left={(props) => <List.Icon {...props} icon="help-circle" />}
            onPress={() => {}}
          />
          <List.Item
            title="About"
            left={(props) => <List.Icon {...props} icon="information" />}
            onPress={() => {}}
          />
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        onPress={signOut}
        style={styles.logoutButton}
        buttonColor="#ff5252"
      >
        Sign Out
      </Button>

      <Text variant="bodySmall" style={styles.version}>
        Fantasy Assistant v1.0.0
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    margin: 15,
    elevation: 3,
  },
  profileHeader: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  avatar: {
    backgroundColor: '#00a86b',
  },
  username: {
    marginTop: 15,
    fontWeight: 'bold',
  },
  email: {
    color: '#666',
    marginTop: 5,
  },
  fullName: {
    color: '#666',
    marginTop: 5,
  },
  divider: {
    marginVertical: 15,
  },
  logoutButton: {
    margin: 15,
    marginTop: 30,
  },
  version: {
    textAlign: 'center',
    color: '#999',
    marginVertical: 20,
  },
});
