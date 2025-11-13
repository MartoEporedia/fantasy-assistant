import React, { useState } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Card, Text, Button, FAB, Portal, Modal, TextInput, Chip, ActivityIndicator } from 'react-native-paper';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../config/api';

export default function AuctionsScreen({ navigation }: any) {
  const [modalVisible, setModalVisible] = useState(false);
  const [auctionName, setAuctionName] = useState('');
  const [auctionType, setAuctionType] = useState('classic');
  const queryClient = useQueryClient();

  const { data: auctions, isLoading } = useQuery({
    queryKey: ['auctions'],
    queryFn: async () => {
      const response = await api.get('/auctions');
      return response.data;
    },
  });

  const createAuctionMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/auctions', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auctions'] });
      setModalVisible(false);
      setAuctionName('');
      setAuctionType('classic');
    },
  });

  const handleCreateAuction = () => {
    if (!auctionName) return;

    createAuctionMutation.mutate({
      name: auctionName,
      auction_type: auctionType,
      total_budget: 500,
      num_teams: 10,
      roster_size: 25,
      roles_required: { P: 3, D: 8, C: 8, A: 6 },
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return '#00a86b';
      case 'completed':
        return '#666';
      default:
        return '#0066cc';
    }
  };

  const renderAuction = ({ item }: any) => (
    <Card
      style={styles.card}
      onPress={() => navigation.navigate('AuctionDetail', { auctionId: item.id })}
    >
      <Card.Content>
        <View style={styles.auctionHeader}>
          <Text variant="titleLarge">{item.name}</Text>
          <Chip
            mode="flat"
            style={{ backgroundColor: getStatusColor(item.status) }}
            textStyle={{ color: 'white' }}
          >
            {item.status.toUpperCase()}
          </Chip>
        </View>

        <View style={styles.auctionInfo}>
          <Text variant="bodyMedium">Type: {item.auction_type}</Text>
          <Text variant="bodyMedium">Budget: ${item.total_budget}</Text>
          <Text variant="bodyMedium">Teams: {item.num_teams}</Text>
          <Text variant="bodyMedium">Roster Size: {item.roster_size}</Text>
        </View>

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
      ) : auctions?.length === 0 ? (
        <View style={styles.emptyState}>
          <Text variant="headlineSmall" style={styles.emptyText}>
            No auctions yet
          </Text>
          <Text variant="bodyLarge" style={styles.emptySubtext}>
            Create your first auction to get started!
          </Text>
        </View>
      ) : (
        <FlatList
          data={auctions}
          renderItem={renderAuction}
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
            Create New Auction
          </Text>

          <TextInput
            label="Auction Name"
            value={auctionName}
            onChangeText={setAuctionName}
            mode="outlined"
            style={styles.input}
          />

          <Text variant="titleMedium" style={styles.label}>
            Auction Type
          </Text>
          <View style={styles.typeChips}>
            {['classic', 'snake', 'sealed', 'hybrid'].map((type) => (
              <Chip
                key={type}
                selected={auctionType === type}
                onPress={() => setAuctionType(type)}
                style={styles.typeChip}
              >
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </Chip>
            ))}
          </View>

          <View style={styles.modalButtons}>
            <Button mode="outlined" onPress={() => setModalVisible(false)}>
              Cancel
            </Button>
            <Button
              mode="contained"
              onPress={handleCreateAuction}
              loading={createAuctionMutation.isPending}
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
  auctionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  auctionInfo: {
    marginBottom: 10,
  },
  date: {
    color: '#666',
    marginTop: 5,
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
  label: {
    marginBottom: 10,
  },
  typeChips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 20,
  },
  typeChip: {
    marginRight: 8,
    marginBottom: 8,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 20,
  },
});
