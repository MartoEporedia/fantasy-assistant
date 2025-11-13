import { MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

export const theme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: '#00a86b',
    secondary: '#0066cc',
    background: '#f5f5f5',
    surface: '#ffffff',
    error: '#d32f2f',
    success: '#00a86b',
  },
};

export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: '#00d68f',
    secondary: '#3399ff',
    background: '#121212',
    surface: '#1e1e1e',
    error: '#ff5252',
    success: '#00d68f',
  },
};
