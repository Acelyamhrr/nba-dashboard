from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import teams
import time
from typing import List, Dict

# pour recup les stats nba
class NBAStatsScraper:

    def __init__(self, season: str = "2024-25"):

        self.season = season

    # recup les plus fort de la ligue et retourne un sdico avc les stats des joeuurs
    def fetch_league_leaders(self) -> List[Dict]:

        print(f"Récupération des stats de la saison {self.season}...")

        try:
            # Appel à l'API NBA
            leaders = leagueleaders.LeagueLeaders(
                season=self.season,
                stat_category_abbreviation='PTS',
                per_mode48='PerGame'
            )

            # Conversion en DataFrame
            df = leaders.get_data_frames()[0]

            # Transformation des données
            players_data = []
            for _, row in df.iterrows():
                player = {
                    'player_id': row.get('PLAYER_ID'),
                    'player_name': row.get('PLAYER'),
                    'team_name': row.get('TEAM'),
                    'position': row.get('POSITION', 'N/A'),
                    'games_played': row.get('GP'),
                    'ppg': round(row.get('PTS', 0), 1),
                    'rpg': round(row.get('REB', 0), 1),
                    'apg': round(row.get('AST', 0), 1),
                    'spg': round(row.get('STL', 0), 1),
                    'bpg': round(row.get('BLK', 0), 1),
                    'fg_pct': round(row.get('FG_PCT', 0) * 100, 1),
                    'three_pct': round(row.get('FG3_PCT', 0) * 100, 1),
                    'ft_pct': round(row.get('FT_PCT', 0) * 100, 1),
                    'season': self.season
                }
                players_data.append(player)

            print(f"✓ {len(players_data)} joueurs récupérés")
            return players_data

        except Exception as e:
            print(f"✗ Erreur lors de la récupération: {e}")
            return []

