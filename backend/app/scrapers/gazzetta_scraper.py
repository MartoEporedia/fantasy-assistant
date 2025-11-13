"""
Scraper for Gazzetta dello Sport Fantacalcio section
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)

class GazzettaScraper:
    """Scraper for Gazzetta dello Sport fantasy football data"""

    BASE_URL = "https://www.gazzetta.it"
    FANTACALCIO_URL = f"{BASE_URL}/calcio/fantanews"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/html',
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_player_ratings(self, matchday: Optional[int] = None) -> List[Dict]:
        """
        Get player ratings for current or specific matchday
        """
        players = []

        try:
            url = f"{self.FANTACALCIO_URL}/voti"
            if matchday:
                url += f"?giornata={matchday}"

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # Try to find JSON data in page
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tags = soup.find_all('script', type='application/json')

            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    if 'players' in data:
                        players.extend(self._parse_player_data(data['players']))
                except json.JSONDecodeError:
                    continue

            # Fallback to HTML parsing if no JSON found
            if not players:
                players = self._parse_html_ratings(soup)

            logger.info(f"Scraped {len(players)} player ratings from Gazzetta")

        except Exception as e:
            logger.error(f"Error fetching from Gazzetta: {e}")

        return players

    def _parse_player_data(self, players_data: List[Dict]) -> List[Dict]:
        """Parse player data from JSON"""
        parsed = []

        for player in players_data:
            try:
                parsed.append({
                    'name': player.get('name', ''),
                    'team': player.get('team', ''),
                    'role': self._normalize_role(player.get('role', '')),
                    'rating': float(player.get('vote', 0)),
                    'goals': int(player.get('goals', 0)),
                    'assists': int(player.get('assists', 0)),
                    'fantasy_points': float(player.get('fantavote', 0)),
                })
            except (ValueError, KeyError) as e:
                logger.error(f"Error parsing player: {e}")
                continue

        return parsed

    def _parse_html_ratings(self, soup) -> List[Dict]:
        """Parse player ratings from HTML table"""
        players = []

        table = soup.find('table', class_='ratings-table')
        if not table:
            return players

        rows = table.find_all('tr')[1:]  # Skip header

        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    players.append({
                        'name': cells[0].text.strip(),
                        'team': cells[1].text.strip(),
                        'role': self._normalize_role(cells[2].text.strip()),
                        'rating': float(cells[3].text.strip().replace(',', '.')),
                        'fantasy_points': float(cells[4].text.strip().replace(',', '.')),
                    })
            except (ValueError, IndexError) as e:
                logger.error(f"Error parsing row: {e}")
                continue

        return players

    def get_injury_updates(self) -> List[Dict]:
        """Get latest injury and suspension updates"""
        updates = []

        try:
            url = f"{self.FANTACALCIO_URL}/probabili-formazioni"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find injury/suspension notices
            notices = soup.find_all('div', class_='player-status')

            for notice in notices:
                try:
                    name_elem = notice.find('span', class_='player-name')
                    status_elem = notice.find('span', class_='status')

                    if name_elem and status_elem:
                        updates.append({
                            'name': name_elem.text.strip(),
                            'status': status_elem.text.strip(),
                            'is_injured': 'infortunato' in status_elem.text.lower(),
                            'is_suspended': 'squalificato' in status_elem.text.lower(),
                        })
                except Exception as e:
                    logger.error(f"Error parsing injury update: {e}")
                    continue

            logger.info(f"Found {len(updates)} injury/suspension updates")

        except Exception as e:
            logger.error(f"Error fetching injury updates: {e}")

        return updates

    def get_fixture_difficulty(self) -> Dict[str, Dict]:
        """Get fixture difficulty ratings for teams"""
        difficulties = {}

        try:
            url = f"{self.FANTACALCIO_URL}/calendario"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse fixture difficulty (1-5 scale)
            team_fixtures = soup.find_all('div', class_='team-fixtures')

            for team_elem in team_fixtures:
                team_name = team_elem.find('h3').text.strip()
                fixtures = []

                for fixture in team_elem.find_all('div', class_='fixture'):
                    difficulty_class = fixture.get('data-difficulty', '3')
                    fixtures.append({
                        'opponent': fixture.find('span', class_='opponent').text.strip(),
                        'difficulty': int(difficulty_class),
                        'home': 'casa' in fixture.get('class', []),
                    })

                difficulties[team_name] = {
                    'next_5': fixtures[:5],
                    'avg_difficulty': sum(f['difficulty'] for f in fixtures[:5]) / 5 if fixtures else 3,
                }

        except Exception as e:
            logger.error(f"Error fetching fixture difficulty: {e}")

        return difficulties

    def _normalize_role(self, role: str) -> str:
        """Normalize role to P, D, C, A format"""
        role_map = {
            'Por': 'P', 'P': 'P', 'Portiere': 'P',
            'Dif': 'D', 'D': 'D', 'Difensore': 'D',
            'Cen': 'C', 'C': 'C', 'Centrocampista': 'C',
            'Att': 'A', 'A': 'A', 'Attaccante': 'A',
        }
        return role_map.get(role, 'C')


def scrape_gazzetta() -> Dict:
    """Main function to scrape Gazzetta dello Sport"""
    scraper = GazzettaScraper()

    return {
        'players': scraper.get_player_ratings(),
        'injuries': scraper.get_injury_updates(),
        'fixture_difficulty': scraper.get_fixture_difficulty(),
    }
