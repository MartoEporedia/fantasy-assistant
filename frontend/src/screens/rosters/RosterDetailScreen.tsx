import React from 'react';
import { View, StyleSheet, ScrollView, FlatList } from 'react-native';
import {
  Card,
  Text,
  Divider,
  Chip,
  ActivityIndicator,
  ProgressBar,
  Button,
} from 'react-native-paper';
import { useQuery } from '@tanstack/react-query';
import api from '../../config/api';

export default function RosterDetailScreen({ route }: any) {
  const { rosterId } = route.params;

  const { data: roster, isLoading } = useQuery({
    queryKey: ['roster', rosterId],
    queryFn: async () => {
      const response = await api.get(`/rosters/${rosterId}/details`);
      return response.data;
    },
  });

  const { data: analysis } = useQuery({
    queryKey: ['rosterAnalysis', rosterId],
    queryFn: async () => {
      const response = await api.get(`/advice/roster/${rosterId}`);
      return response.data;
    },
  });

  const getScoreColor = (score: number) => {
    if (score >= 70) return '#00a86b';
    if (score >= 50) return '#ffa500';
    return '#ff5252';
  };

  const roleColors: any = {
    P: '#3399ff',
    D: '#00a86b',
    C: '#ffa500',
    A: '#ff5252',
  };

  if (isLoading) {
    return <ActivityIndicator size="large" style={styles.loader} />;
  }

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="headlineMedium">{roster?.roster.name}</Text>

          <View style={styles.budgetInfo}>
            <View style={styles.budgetItem}>
              <Text variant="bodyMedium">Total Spent</Text>
              <Text variant="titleLarge" style={styles.amount}>
                ${roster?.roster.total_spent || 0}
              </Text>
            </View>
            {roster?.roster.remaining_budget !== null && (
              <View style={styles.budgetItem}>
                <Text variant="bodyMedium">Remaining</Text>
                <Text variant="titleLarge" style={styles.amount}>
                  ${roster?.roster.remaining_budget}
                </Text>
              </View>
            )}
          </View>
        </Card.Content>
      </Card>

      {analysis && (
        <>
          <Card style={styles.card}>
            <Card.Content>
              <Text variant="titleLarge">Roster Analysis</Text>
              <Divider style={styles.divider} />

              <View style={styles.scoresGrid}>
                <View style={styles.scoreBox}>
                  <Text variant="titleMedium" style={{ color: getScoreColor(analysis.balance_score) }}>
                    {analysis.balance_score}/100
                  </Text>
                  <Text variant="bodySmall">Balance</Text>
                </View>
                <View style={styles.scoreBox}>
                  <Text variant="titleMedium" style={{ color: getScoreColor(analysis.quality_score) }}>
                    {analysis.quality_score}/100
                  </Text>
                  <Text variant="bodySmall">Quality</Text>
                </View>
                <View style={styles.scoreBox}>
                  <Text variant="titleMedium" style={{ color: getScoreColor(analysis.depth_score) }}>
                    {analysis.depth_score}/100
                  </Text>
                  <Text variant="bodySmall">Depth</Text>
                </View>
              </View>

              <Text variant="titleMedium" style={styles.sectionTitle}>
                Role Distribution
              </Text>
              {Object.entries(analysis.role_distribution).map(([role, count]: any) => (
                <View key={role} style={styles.roleRow}>
                  <View style={styles.roleLabel}>
                    <Chip
                      mode="flat"
                      style={{ backgroundColor: roleColors[role] }}
                      textStyle={{ color: 'white' }}
                    >
                      {role}
                    </Chip>
                    <Text variant="bodyMedium" style={styles.roleCount}>
                      {count} players
                    </Text>
                  </View>
                </View>
              ))}
            </Card.Content>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text variant="titleLarge">Strengths</Text>
              <Divider style={styles.divider} />
              {analysis.strengths.map((strength: string, index: number) => (
                <Text key={index} variant="bodyMedium" style={styles.listItem}>
                  ✓ {strength}
                </Text>
              ))}
            </Card.Content>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text variant="titleLarge">Weaknesses</Text>
              <Divider style={styles.divider} />
              {analysis.weaknesses.map((weakness: string, index: number) => (
                <Text key={index} variant="bodyMedium" style={styles.listItem}>
                  ⚠ {weakness}
                </Text>
              ))}
            </Card.Content>
          </Card>

          <Card style={styles.card}>
            <Card.Content>
              <Text variant="titleLarge">Suggestions</Text>
              <Divider style={styles.divider} />
              {analysis.suggested_improvements.map((suggestion: string, index: number) => (
                <Text key={index} variant="bodyMedium" style={styles.listItem}>
                  💡 {suggestion}
                </Text>
              ))}
            </Card.Content>
          </Card>
        </>
      )}

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">Players ({roster?.players.length || 0})</Text>
          <Divider style={styles.divider} />

          {roster?.players.length === 0 ? (
            <Text variant="bodyMedium" style={styles.emptyText}>
              No players in roster yet
            </Text>
          ) : (
            roster?.players.map((player: any) => (
              <View key={player.id} style={styles.playerRow}>
                <View style={styles.playerInfo}>
                  <Text variant="titleSmall">{player.name}</Text>
                  <Text variant="bodySmall" style={styles.playerTeam}>
                    {player.team}
                  </Text>
                </View>
                <View style={styles.playerMeta}>
                  <Chip
                    mode="outlined"
                    style={{ backgroundColor: roleColors[player.role] }}
                    textStyle={{ color: 'white' }}
                  >
                    {player.role}
                  </Chip>
                  <Text variant="titleSmall" style={styles.price}>
                    ${player.purchase_price}
                  </Text>
                </View>
              </View>
            ))
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
  budgetInfo: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 20,
  },
  budgetItem: {
    alignItems: 'center',
  },
  amount: {
    color: '#00a86b',
    fontWeight: 'bold',
  },
  divider: {
    marginVertical: 15,
  },
  scoresGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  scoreBox: {
    alignItems: 'center',
  },
  sectionTitle: {
    marginTop: 15,
    marginBottom: 10,
  },
  roleRow: {
    marginBottom: 10,
  },
  roleLabel: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  roleCount: {
    marginLeft: 10,
  },
  listItem: {
    marginBottom: 8,
    paddingLeft: 5,
  },
  emptyText: {
    textAlign: 'center',
    color: '#666',
    marginVertical: 20,
  },
  playerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  playerInfo: {
    flex: 1,
  },
  playerTeam: {
    color: '#666',
    marginTop: 4,
  },
  playerMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  price: {
    marginLeft: 10,
    color: '#00a86b',
    fontWeight: 'bold',
  },
});
