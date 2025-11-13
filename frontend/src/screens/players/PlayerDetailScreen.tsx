import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Text, Chip, ActivityIndicator, Divider } from 'react-native-paper';
import { useQuery } from '@tanstack/react-query';
import api from '../../config/api';

export default function PlayerDetailScreen({ route }: any) {
  const { playerId } = route.params;

  const { data: player, isLoading } = useQuery({
    queryKey: ['player', playerId],
    queryFn: async () => {
      const response = await api.get(`/players/${playerId}`);
      return response.data;
    },
  });

  const { data: stats } = useQuery({
    queryKey: ['playerStats', playerId],
    queryFn: async () => {
      const response = await api.get(`/players/${playerId}/stats`);
      return response.data;
    },
  });

  if (isLoading) {
    return <ActivityIndicator size="large" style={styles.loader} />;
  }

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.header}>
            <View>
              <Text variant="headlineMedium">{player.name}</Text>
              <Text variant="titleMedium" style={styles.team}>{player.team}</Text>
            </View>
            <Chip mode="outlined" style={styles.roleChip}>{player.role}</Chip>
          </View>

          <View style={styles.info}>
            <Text variant="bodyMedium">Age: {player.age}</Text>
            <Text variant="bodyMedium">Nationality: {player.nationality}</Text>
          </View>

          {player.is_injured && (
            <Chip icon="alert" mode="flat" style={styles.alertChip}>
              Injured: {player.injury_info}
            </Chip>
          )}
          {player.is_suspended && (
            <Chip icon="alert" mode="flat" style={styles.alertChip}>
              Suspended
            </Chip>
          )}
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">Current Season Stats</Text>
          <Divider style={styles.divider} />

          <View style={styles.statsGrid}>
            <View style={styles.statBox}>
              <Text variant="displaySmall">{stats?.current_season.matches_played || 0}</Text>
              <Text variant="bodyMedium">Matches</Text>
            </View>
            <View style={styles.statBox}>
              <Text variant="displaySmall">{stats?.current_season.goals || 0}</Text>
              <Text variant="bodyMedium">Goals</Text>
            </View>
            <View style={styles.statBox}>
              <Text variant="displaySmall">{stats?.current_season.assists || 0}</Text>
              <Text variant="bodyMedium">Assists</Text>
            </View>
            <View style={styles.statBox}>
              <Text variant="displaySmall">
                {stats?.current_season.avg_rating?.toFixed(1) || 'N/A'}
              </Text>
              <Text variant="bodyMedium">Avg Rating</Text>
            </View>
            <View style={styles.statBox}>
              <Text variant="displaySmall">{stats?.current_season.fantasy_points || 0}</Text>
              <Text variant="bodyMedium">Fantasy Pts</Text>
            </View>
            <View style={styles.statBox}>
              <Text variant="displaySmall">{stats?.current_season.yellow_cards || 0}</Text>
              <Text variant="bodyMedium">Yellow Cards</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">Market Value</Text>
          <Divider style={styles.divider} />

          <View style={styles.valueRow}>
            <Text variant="bodyLarge">Estimated Value:</Text>
            <Text variant="titleLarge" style={styles.value}>
              ${stats?.market_value || 'N/A'}
            </Text>
          </View>

          {stats?.avg_auction_price && (
            <View style={styles.valueRow}>
              <Text variant="bodyLarge">Avg Auction Price:</Text>
              <Text variant="titleLarge" style={styles.value}>
                ${stats.avg_auction_price}
              </Text>
            </View>
          )}
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
  loader: {
    flex: 1,
    justifyContent: 'center',
  },
  card: {
    margin: 15,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 15,
  },
  team: {
    color: '#666',
    marginTop: 5,
  },
  roleChip: {
    marginTop: 5,
  },
  info: {
    marginVertical: 10,
  },
  alertChip: {
    marginTop: 10,
    backgroundColor: '#ffebee',
  },
  divider: {
    marginVertical: 15,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
  },
  statBox: {
    alignItems: 'center',
    width: '33%',
    marginBottom: 20,
  },
  valueRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 10,
  },
  value: {
    color: '#00a86b',
    fontWeight: 'bold',
  },
});
