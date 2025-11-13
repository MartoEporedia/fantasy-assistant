import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, FlatList } from 'react-native';
import {
  Card,
  Text,
  Button,
  Divider,
  Portal,
  Modal,
  TextInput,
  ActivityIndicator,
  Chip,
} from 'react-native-paper';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../config/api';

export default function AuctionDetailScreen({ route }: any) {
  const { auctionId } = route.params;
  const [bidModalVisible, setBidModalVisible] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState<any>(null);
  const [bidAmount, setBidAmount] = useState('');
  const queryClient = useQueryClient();

  const { data: auction, isLoading } = useQuery({
    queryKey: ['auction', auctionId],
    queryFn: async () => {
      const response = await api.get(`/auctions/${auctionId}`);
      return response.data;
    },
  });

  const { data: bids } = useQuery({
    queryKey: ['auctionBids', auctionId],
    queryFn: async () => {
      const response = await api.get(`/auctions/${auctionId}/bids`);
      return response.data;
    },
  });

  const { data: players } = useQuery({
    queryKey: ['players'],
    queryFn: async () => {
      const response = await api.get('/players');
      return response.data;
    },
  });

  const placeBidMutation = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post(`/auctions/${auctionId}/bids`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auctionBids', auctionId] });
      setBidModalVisible(false);
      setBidAmount('');
      setSelectedPlayer(null);
    },
  });

  const startAuctionMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post(`/auctions/${auctionId}/start`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auction', auctionId] });
    },
  });

  const handlePlaceBid = () => {
    if (!bidAmount || !selectedPlayer) return;

    placeBidMutation.mutate({
      player_id: selectedPlayer.id,
      amount: parseInt(bidAmount),
      is_sealed: auction?.auction_type === 'sealed',
    });
  };

  const openBidModal = (player: any) => {
    setSelectedPlayer(player);
    setBidModalVisible(true);
  };

  if (isLoading) {
    return <ActivityIndicator size="large" style={styles.loader} />;
  }

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="headlineMedium">{auction?.name}</Text>
          <Chip mode="outlined" style={styles.statusChip}>
            {auction?.status.toUpperCase()}
          </Chip>

          <Divider style={styles.divider} />

          <View style={styles.infoGrid}>
            <View style={styles.infoItem}>
              <Text variant="bodyMedium">Type</Text>
              <Text variant="titleMedium">{auction?.auction_type}</Text>
            </View>
            <View style={styles.infoItem}>
              <Text variant="bodyMedium">Budget</Text>
              <Text variant="titleMedium">${auction?.total_budget}</Text>
            </View>
            <View style={styles.infoItem}>
              <Text variant="bodyMedium">Teams</Text>
              <Text variant="titleMedium">{auction?.num_teams}</Text>
            </View>
            <View style={styles.infoItem}>
              <Text variant="bodyMedium">Roster Size</Text>
              <Text variant="titleMedium">{auction?.roster_size}</Text>
            </View>
          </View>

          {auction?.status === 'pending' && (
            <Button
              mode="contained"
              onPress={() => startAuctionMutation.mutate()}
              loading={startAuctionMutation.isPending}
              style={styles.startButton}
            >
              Start Auction
            </Button>
          )}
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge">Recent Bids</Text>
          <Divider style={styles.divider} />

          {bids?.length === 0 ? (
            <Text variant="bodyMedium" style={styles.noBids}>
              No bids yet
            </Text>
          ) : (
            bids?.slice(0, 10).map((bid: any) => (
              <View key={bid.id} style={styles.bidItem}>
                <View>
                  <Text variant="titleSmall">Player ID: {bid.player_id}</Text>
                  <Text variant="bodySmall" style={styles.bidTime}>
                    {new Date(bid.created_at).toLocaleString()}
                  </Text>
                </View>
                <Text variant="titleMedium" style={styles.bidAmount}>
                  ${bid.amount}
                </Text>
              </View>
            ))
          )}
        </Card.Content>
      </Card>

      {auction?.status === 'active' && (
        <Card style={styles.card}>
          <Card.Content>
            <Text variant="titleLarge">Available Players</Text>
            <Divider style={styles.divider} />

            {players?.slice(0, 10).map((player: any) => (
              <View key={player.id} style={styles.playerItem}>
                <View style={styles.playerInfo}>
                  <Text variant="titleSmall">{player.name}</Text>
                  <Text variant="bodySmall">{player.team} - {player.role}</Text>
                </View>
                <Button
                  mode="outlined"
                  onPress={() => openBidModal(player)}
                  compact
                >
                  Bid
                </Button>
              </View>
            ))}
          </Card.Content>
        </Card>
      )}

      <Portal>
        <Modal
          visible={bidModalVisible}
          onDismiss={() => setBidModalVisible(false)}
          contentContainerStyle={styles.modal}
        >
          <Text variant="headlineSmall" style={styles.modalTitle}>
            Place Bid
          </Text>

          {selectedPlayer && (
            <View style={styles.playerCard}>
              <Text variant="titleMedium">{selectedPlayer.name}</Text>
              <Text variant="bodyMedium">{selectedPlayer.team}</Text>
              <Text variant="bodySmall">Role: {selectedPlayer.role}</Text>
            </View>
          )}

          <TextInput
            label="Bid Amount ($)"
            value={bidAmount}
            onChangeText={setBidAmount}
            mode="outlined"
            keyboardType="numeric"
            style={styles.input}
          />

          <View style={styles.modalButtons}>
            <Button mode="outlined" onPress={() => setBidModalVisible(false)}>
              Cancel
            </Button>
            <Button
              mode="contained"
              onPress={handlePlaceBid}
              loading={placeBidMutation.isPending}
            >
              Place Bid
            </Button>
          </View>
        </Modal>
      </Portal>
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
  statusChip: {
    marginTop: 10,
    alignSelf: 'flex-start',
  },
  divider: {
    marginVertical: 15,
  },
  infoGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  infoItem: {
    width: '48%',
    marginBottom: 15,
  },
  startButton: {
    marginTop: 15,
  },
  noBids: {
    textAlign: 'center',
    color: '#666',
    marginVertical: 20,
  },
  bidItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  bidTime: {
    color: '#666',
    marginTop: 4,
  },
  bidAmount: {
    color: '#00a86b',
    fontWeight: 'bold',
  },
  playerItem: {
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
  modal: {
    backgroundColor: 'white',
    padding: 20,
    margin: 20,
    borderRadius: 10,
  },
  modalTitle: {
    marginBottom: 15,
  },
  playerCard: {
    backgroundColor: '#f5f5f5',
    padding: 15,
    borderRadius: 8,
    marginBottom: 15,
  },
  input: {
    marginBottom: 15,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
});
