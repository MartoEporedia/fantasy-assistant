import React, { useState } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Searchbar, Card, Text, Chip, ActivityIndicator } from 'react-native-paper';
import { useQuery } from '@tanstack/react-query';
import api from '../../config/api';

export default function PlayersScreen({ navigation }: any) {
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState<string | null>(null);

  const { data: players, isLoading } = useQuery({
    queryKey: ['players', roleFilter, search],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (roleFilter) params.append('role', roleFilter);
      if (search) params.append('search', search);

      const response = await api.get(`/players?${params.toString()}`);
      return response.data;
    },
  });

  const roles = ['P', 'D', 'C', 'A'];

  const renderPlayer = ({ item }: any) => (
    <Card
      style={styles.card}
      onPress={() => navigation.navigate('PlayerDetail', { playerId: item.id })}
    >
      <Card.Content>
        <View style={styles.playerHeader}>
          <View style={styles.playerInfo}>
            <Text variant="titleMedium">{item.name}</Text>
            <Text variant="bodyMedium" style={styles.team}>{item.team}</Text>
          </View>
          <Chip mode="outlined">{item.role}</Chip>
        </View>

        <View style={styles.stats}>
          <View style={styles.stat}>
            <Text variant="bodySmall">Goals</Text>
            <Text variant="titleSmall">{item.goals}</Text>
          </View>
          <View style={styles.stat}>
            <Text variant="bodySmall">Assists</Text>
            <Text variant="titleSmall">{item.assists}</Text>
          </View>
          <View style={styles.stat}>
            <Text variant="bodySmall">Avg Rating</Text>
            <Text variant="titleSmall">{item.avg_rating?.toFixed(1) || 'N/A'}</Text>
          </View>
          <View style={styles.stat}>
            <Text variant="bodySmall">Value</Text>
            <Text variant="titleSmall">${item.market_value || 'N/A'}</Text>
          </View>
        </View>
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      <Searchbar
        placeholder="Search players..."
        onChangeText={setSearch}
        value={search}
        style={styles.searchbar}
      />

      <View style={styles.filters}>
        <Chip
          selected={roleFilter === null}
          onPress={() => setRoleFilter(null)}
          style={styles.chip}
        >
          All
        </Chip>
        {roles.map((role) => (
          <Chip
            key={role}
            selected={roleFilter === role}
            onPress={() => setRoleFilter(role)}
            style={styles.chip}
          >
            {role}
          </Chip>
        ))}
      </View>

      {isLoading ? (
        <ActivityIndicator size="large" style={styles.loader} />
      ) : (
        <FlatList
          data={players}
          renderItem={renderPlayer}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.list}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  searchbar: {
    margin: 10,
  },
  filters: {
    flexDirection: 'row',
    paddingHorizontal: 10,
    paddingBottom: 10,
  },
  chip: {
    marginRight: 8,
  },
  list: {
    padding: 10,
  },
  card: {
    marginBottom: 10,
  },
  playerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  playerInfo: {
    flex: 1,
  },
  team: {
    color: '#666',
    marginTop: 4,
  },
  stats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  stat: {
    alignItems: 'center',
  },
  loader: {
    marginTop: 50,
  },
});
