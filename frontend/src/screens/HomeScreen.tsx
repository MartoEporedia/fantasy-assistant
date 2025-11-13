import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button } from 'react-native-paper';
import { useAuth } from '../contexts/AuthContext';

export default function HomeScreen({ navigation }: any) {
  const { user } = useAuth();

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text variant="headlineMedium" style={styles.title}>
          Welcome, {user?.username}! ⚽
        </Text>
        <Text variant="bodyLarge" style={styles.subtitle}>
          Your Fantasy Football Assistant
        </Text>
      </View>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">🏆 Quick Actions</Text>
        </Card.Content>
        <Card.Actions>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('Auctions')}
            style={styles.button}
          >
            Start Auction
          </Button>
          <Button
            mode="outlined"
            onPress={() => navigation.navigate('Players')}
            style={styles.button}
          >
            Browse Players
          </Button>
        </Card.Actions>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">📊 Statistics</Text>
          <View style={styles.statsContainer}>
            <View style={styles.stat}>
              <Text variant="displaySmall">0</Text>
              <Text variant="bodyMedium">Active Auctions</Text>
            </View>
            <View style={styles.stat}>
              <Text variant="displaySmall">0</Text>
              <Text variant="bodyMedium">Rosters</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">💡 Tips</Text>
          <Text variant="bodyMedium" style={styles.tip}>
            • Use AI suggestions during auctions for optimal bids
          </Text>
          <Text variant="bodyMedium" style={styles.tip}>
            • Check player stats and trends before bidding
          </Text>
          <Text variant="bodyMedium" style={styles.tip}>
            • Balance your roster across all positions
          </Text>
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#00a86b',
  },
  title: {
    color: 'white',
    fontWeight: 'bold',
  },
  subtitle: {
    color: 'white',
    marginTop: 5,
  },
  card: {
    margin: 15,
    elevation: 3,
  },
  button: {
    marginHorizontal: 5,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 15,
  },
  stat: {
    alignItems: 'center',
  },
  tip: {
    marginTop: 8,
  },
});
