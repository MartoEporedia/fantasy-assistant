import React, { useState } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import {
  Card,
  Text,
  FAB,
  Portal,
  Modal,
  TextInput,
  Button,
  ActivityIndicator,
  ProgressBar,
} from 'react-native-paper';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../config/api';

export default function RostersScreen({ navigation }: any) {
  const [modalVisible, setModalVisible] = useState(false);
  const [rosterName, setRosterName] = useState('');
  const queryClient = useQueryClient();

  const { data: rosters, isLoading } = useQuery({
    queryKey: ['rosters'],
    queryFn: async () => {
      const response = await api.get('/rosters');
      return response.data;
    },
  });

  const createRosterMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/rosters', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['rosters'] });
      setModalVisible(false);
      setRosterName('');
    },
  });

  const handleCreateRoster = () => {
    if (!rosterName) return;
    createRosterMutation.mutate({ name: rosterName });
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return '#00a86b';
    if (score >= 50) return '#ffa500';
    return '#ff5252';
  };

  const renderRoster = ({ item }: any) => (
    <Card
      style={styles.card}
      onPress={() => navigation.navigate('RosterDetail', { rosterId: item.id })}
    >
      <Card.Content>
        <Text variant="titleLarge">{item.name}</Text>

        <View style={styles.rosterInfo}>
          <Text variant="bodyMedium">
            Players: {item.players?.length || 0}
          </Text>
          <Text variant="bodyMedium">
            Budget Spent: ${item.total_spent || 0}
          </Text>
        </View>

        {item.balance_score !== null && (
          <View style={styles.scoreContainer}>
            <View style={styles.scoreHeader}>
              <Text variant="bodyMedium">Balance Score</Text>
              <Text
                variant="titleMedium"
                style={{ color: getScoreColor(item.balance_score) }}
              >
                {item.balance_score}/100
              </Text>
            </View>
            <ProgressBar
              progress={item.balance_score / 100}
              color={getScoreColor(item.balance_score)}
              style={styles.progressBar}
            />
          </View>
        )}

        <Text variant="bodySmall" style={styles.date}>
          Created: {new Date(item.created_at).toLocaleDateString()}
        </Text>
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      {isLoading ? (
        <ActivityIndicator size="large" style={styles.loader} />
      ) : rosters?.length === 0 ? (
        <View style={styles.emptyState}>
          <Text variant="headlineSmall" style={styles.emptyText}>
            No rosters yet
          </Text>
          <Text variant="bodyLarge" style={styles.emptySubtext}>
            Create your first roster to get started!
          </Text>
        </View>
      ) : (
        <FlatList
          data={rosters}
          renderItem={renderRoster}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.list}
        />
      )}

      <FAB
        icon="plus"
        style={styles.fab}
        onPress={() => setModalVisible(true)}
      />

      <Portal>
        <Modal
          visible={modalVisible}
          onDismiss={() => setModalVisible(false)}
          contentContainerStyle={styles.modal}
        >
          <Text variant="headlineSmall" style={styles.modalTitle}>
            Create New Roster
          </Text>

          <TextInput
            label="Roster Name"
            value={rosterName}
            onChangeText={setRosterName}
            mode="outlined"
            style={styles.input}
          />

          <View style={styles.modalButtons}>
            <Button mode="outlined" onPress={() => setModalVisible(false)}>
              Cancel
            </Button>
            <Button
              mode="contained"
              onPress={handleCreateRoster}
              loading={createRosterMutation.isPending}
            >
              Create
            </Button>
          </View>
        </Modal>
      </Portal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loader: {
    marginTop: 50,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  emptyText: {
    marginBottom: 10,
  },
  emptySubtext: {
    color: '#666',
    textAlign: 'center',
  },
  list: {
    padding: 10,
  },
  card: {
    marginBottom: 10,
  },
  rosterInfo: {
    marginVertical: 15,
  },
  scoreContainer: {
    marginVertical: 10,
  },
  scoreHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
  },
  date: {
    color: '#666',
    marginTop: 10,
  },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    backgroundColor: '#00a86b',
  },
  modal: {
    backgroundColor: 'white',
    padding: 20,
    margin: 20,
    borderRadius: 10,
  },
  modalTitle: {
    marginBottom: 20,
  },
  input: {
    marginBottom: 15,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 20,
  },
});
