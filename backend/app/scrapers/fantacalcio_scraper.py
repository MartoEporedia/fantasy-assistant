"""
Web scraper for Fantacalcio.it - Get real player data and statistics
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import logging

logger = logging.getLogger(__name__)

class FantacalcioScraper:
    """Scraper for Fantacalcio.it website"""

    BASE_URL = "https://www.fantacalcio.it"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_all_players(self, serie_a_only: bool = True) -> List[Dict]:
        """
        Fetch all Serie A players with current season statistics
        """
        players = []

        try:
            # Fantacalcio.it quotazioni page
            url = f"{self.BASE_URL}/quotazioni-fantacalcio"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find player rows (adjust selectors based on actual HTML)
            player_rows = soup.find_all('tr', class_='player-row')

            for row in player_rows:
                try:
                    player_data = self._parse_player_row(row)
                    if player_data:
                        players.append(player_data)
                except Exception as e:
                    logger.error(f"Error parsing player row: {e}")
                    continue

                # Be respectful with rate limiting
                time.sleep(0.1)

            logger.info(f"Scraped {len(players)} players from Fantacalcio.it")

        except requests.RequestException as e:
            logger.error(f"Error fetching from Fantacalcio.it: {e}")

        return players

    def _parse_player_row(self, row) -> Optional[Dict]:
        """Parse a single player row from the table"""
        try:
            # Adjust selectors based on actual HTML structure
            name_elem = row.find('td', class_='name')
            team_elem = row.find('td', class_='team')
            role_elem = row.find('td', class_='role')

            if not all([name_elem, team_elem, role_elem]):
                return None

            player = {
                'name': name_elem.text.strip(),
                'team': team_elem.text.strip(),
                'role': self._normalize_role(role_elem.text.strip()),
                'age': self._extract_number(row, 'age'),
                'nationality': row.find('td', class_='nationality').text.strip() if row.find('td', class_='nationality') else 'Italy',
                'matches_played': self._extract_number(row, 'matches'),
                'goals': self._extract_number(row, 'goals'),
                'assists': self._extract_number(row, 'assists'),
                'yellow_cards': self._extract_number(row, 'yellow-cards'),
                'red_cards': self._extract_number(row, 'red-cards'),
                'avg_rating': self._extract_float(row, 'avg-rating'),
                'fantasy_points': self._extract_float(row, 'fantasy-points'),
                'market_value': self._extract_float(row, 'value'),
            }

            return player

        except Exception as e:
            logger.error(f"Error in _parse_player_row: {e}")
            return None

    def _normalize_role(self, role: str) -> str:
        """Normalize role to P, D, C, A format"""
        role_map = {
            'Por': 'P', 'P': 'P', 'Portiere': 'P',
            'Dif': 'D', 'D': 'D', 'Difensore': 'D',
            'Cen': 'C', 'C': 'C', 'Centrocampista': 'C',
            'Att': 'A', 'A': 'A', 'Attaccante': 'A',
        }
        return role_map.get(role, 'C')

    def _extract_number(self, row, class_name: str) -> int:
        """Extract integer from table cell"""
        try:
            elem = row.find('td', class_=class_name)
            if elem:
                return int(elem.text.strip())
        except (ValueError, AttributeError):
            pass
        return 0

    def _extract_float(self, row, class_name: str) -> Optional[float]:
        """Extract float from table cell"""
        try:
            elem = row.find('td', class_=class_name)
            if elem:
                return float(elem.text.strip().replace(',', '.'))
        except (ValueError, AttributeError):
            pass
        return None

    def get_player_details(self, player_id: int) -> Optional[Dict]:
        """Get detailed statistics for a specific player"""
        try:
            url = f"{self.BASE_URL}/giocatore/{player_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract detailed stats
            details = {
                'injury_info': self._extract_injury_info(soup),
                'is_injured': self._check_injury_status(soup),
                'is_suspended': self._check_suspension_status(soup),
                'stats_history': self._extract_historical_stats(soup),
            }

            return details

        except Exception as e:
            logger.error(f"Error fetching player details: {e}")
            return None

    def _extract_injury_info(self, soup) -> Optional[str]:
        """Extract injury information if available"""
        injury_elem = soup.find('div', class_='injury-info')
        if injury_elem:
            return injury_elem.text.strip()
        return None

    def _check_injury_status(self, soup) -> bool:
        """Check if player is currently injured"""
        return bool(soup.find('span', class_='status-injured'))

    def _check_suspension_status(self, soup) -> bool:
        """Check if player is suspended"""
        return bool(soup.find('span', class_='status-suspended'))

    def _extract_historical_stats(self, soup) -> Dict:
        """Extract historical season statistics"""
        history = {}

        season_table = soup.find('table', class_='season-stats')
        if season_table:
            rows = season_table.find_all('tr')[1:]  # Skip header

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    season = cells[0].text.strip()
                    stats = {
                        'goals': self._extract_number(row, 'goals'),
                        'assists': self._extract_number(row, 'assists'),
                        'matches': self._extract_number(row, 'matches'),
                    }
                    history[season] = stats

        return history


def scrape_fantacalcio() -> List[Dict]:
    """Main function to scrape Fantacalcio.it"""
    scraper = FantacalcioScraper()
    return scraper.get_all_players()
