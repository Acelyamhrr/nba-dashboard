import sqlite3
import pandas as pd
from typing import List, Dict, Optional


class NBADatabase:

    # inti la connexion a la bdd
    def __init__(self, db_name: str = "nba_stats.db"):

        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ Connexion à {self.db_name} établie")
        except sqlite3.Error as e:
            print(f"✗ Erreur de connexion: {e}")

    def create_tables(self):

        # Table des joueurs
        players_table = """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            team_name TEXT,
            position TEXT,
            games_played INTEGER,
            points_per_game REAL,
            rebounds_per_game REAL,
            assists_per_game REAL,
            steals_per_game REAL,
            blocks_per_game REAL,
            field_goal_pct REAL,
            three_point_pct REAL,
            free_throw_pct REAL,
            season TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        # Table des équipes
        teams_table = """
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL,
            wins INTEGER,
            losses INTEGER,
            win_pct REAL,
            season TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        try:
            self.cursor.execute(players_table)
            self.cursor.execute(teams_table)
            self.conn.commit()
            print("✓ Tables créées avec succès")
        except sqlite3.Error as e:
            print(f"✗ Erreur création tables: {e}")

    def insert_players(self, players_data: List[Dict]):
        insert_query = """
        INSERT OR REPLACE INTO players (
            player_id, player_name, team_name, position, games_played,
            points_per_game, rebounds_per_game, assists_per_game,
            steals_per_game, blocks_per_game, field_goal_pct,
            three_point_pct, free_throw_pct, season
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            for player in players_data:
                self.cursor.execute(insert_query, (
                    player.get('player_id'),
                    player.get('player_name'),
                    player.get('team_name'),
                    player.get('position'),
                    player.get('games_played'),
                    player.get('ppg'),
                    player.get('rpg'),
                    player.get('apg'),
                    player.get('spg'),
                    player.get('bpg'),
                    player.get('fg_pct'),
                    player.get('three_pct'),
                    player.get('ft_pct'),
                    player.get('season')
                ))
            self.conn.commit()
            print(f"✓ {len(players_data)} joueurs insérés/mis à jour")
        except sqlite3.Error as e:
            print(f"✗ Erreur insertion: {e}")

    def get_top_scorers(self, limit: int = 10) -> pd.DataFrame:

        query = """
        SELECT player_name, team_name, games_played, points_per_game, 
               rebounds_per_game, assists_per_game
        FROM players
        WHERE games_played > 10
        ORDER BY points_per_game DESC
        LIMIT ?
        """
        return pd.read_sql_query(query, self.conn, params=(limit,))

    def get_team_stats(self, team_name: str) -> pd.DataFrame:

        query = """
        SELECT player_name, position, games_played, points_per_game,
               rebounds_per_game, assists_per_game
        FROM players
        WHERE team_name LIKE ?
        ORDER BY points_per_game DESC
        """
        return pd.read_sql_query(query, self.conn, params=(f"%{team_name}%",))

    def export_to_csv(self, filename: str = "nba_stats_export.csv"):

        query = "SELECT * FROM players"
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(filename, index=False)
        print(f"✓ Données exportées vers {filename}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("✓ Connexion fermée")

