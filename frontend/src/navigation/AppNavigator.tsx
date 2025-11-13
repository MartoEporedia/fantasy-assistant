import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Screens
import HomeScreen from '../screens/HomeScreen';
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import PlayersScreen from '../screens/players/PlayersScreen';
import PlayerDetailScreen from '../screens/players/PlayerDetailScreen';
import AuctionsScreen from '../screens/auctions/AuctionsScreen';
import AuctionDetailScreen from '../screens/auctions/AuctionDetailScreen';
import RostersScreen from '../screens/rosters/RostersScreen';
import RosterDetailScreen from '../screens/rosters/RosterDetailScreen';
import ProfileScreen from '../screens/profile/ProfileScreen';

import { useAuth } from '../contexts/AuthContext';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const PlayersStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="PlayersList"
      component={PlayersScreen}
      options={{ title: 'Players' }}
    />
    <Stack.Screen
      name="PlayerDetail"
      component={PlayerDetailScreen}
      options={{ title: 'Player Details' }}
    />
  </Stack.Navigator>
);

const AuctionsStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="AuctionsList"
      component={AuctionsScreen}
      options={{ title: 'Auctions' }}
    />
    <Stack.Screen
      name="AuctionDetail"
      component={AuctionDetailScreen}
      options={{ title: 'Auction' }}
    />
  </Stack.Navigator>
);

const RostersStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="RostersList"
      component={RostersScreen}
      options={{ title: 'My Rosters' }}
    />
    <Stack.Screen
      name="RosterDetail"
      component={RosterDetailScreen}
      options={{ title: 'Roster Details' }}
    />
  </Stack.Navigator>
);

const AuthStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Register" component={RegisterScreen} />
  </Stack.Navigator>
);

const MainTabs = () => (
  <Tab.Navigator
    screenOptions={{
      tabBarActiveTintColor: '#00a86b',
      tabBarInactiveTintColor: 'gray',
    }}
  >
    <Tab.Screen
      name="Home"
      component={HomeScreen}
      options={{
        tabBarIcon: ({ color, size }) => (
          <Icon name="home" size={size} color={color} />
        ),
      }}
    />
    <Tab.Screen
      name="Players"
      component={PlayersStack}
      options={{
        headerShown: false,
        tabBarIcon: ({ color, size }) => (
          <Icon name="account-group" size={size} color={color} />
        ),
      }}
    />
    <Tab.Screen
      name="Auctions"
      component={AuctionsStack}
      options={{
        headerShown: false,
        tabBarIcon: ({ color, size }) => (
          <Icon name="gavel" size={size} color={color} />
        ),
      }}
    />
    <Tab.Screen
      name="Rosters"
      component={RostersStack}
      options={{
        headerShown: false,
        tabBarIcon: ({ color, size }) => (
          <Icon name="clipboard-list" size={size} color={color} />
        ),
      }}
    />
    <Tab.Screen
      name="Profile"
      component={ProfileScreen}
      options={{
        tabBarIcon: ({ color, size }) => (
          <Icon name="account" size={size} color={color} />
        ),
      }}
    />
  </Tab.Navigator>
);

export default function AppNavigator() {
  const { user, loading } = useAuth();

  if (loading) {
    return null; // TODO: Add loading screen
  }

  return user ? <MainTabs /> : <AuthStack />;
}
