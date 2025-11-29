import sys
import pandas as pd

from database import NBADatabase
from scraper import NBAStatsScraper
from utils import display_stats_summary, compare_players, calculate_efficiency

from visualizations import (plot_top_scorers, plot_player_comparison, plot_team_analysis, plot_efficiency_scatter, plot_shooting_percentages)


def print_menu():
    print("\n" + "=" * 60)
    print("NBA STATS MANAGER - Menu Principal")
    print("=" * 60)
    print("1. Récupérer les données depuis l'API NBA")
    print("2. Afficher le top 10 des scoreurs")
    print("3. Rechercher les stats d'une équipe")
    print("4. Exporter les données en CSV")
    print("5. Comparer deux joueurs")
    print("6. Calculer les scores d'efficacité")
    print("\n--- VISUALISATIONS ---")
    print("7. Graphique des top scoreurs")
    print("8. Comparer deux joueurs (graphique)")
    print("9. Analyser une équipe (graphique)")
    print("10. Nuage de points efficacité")
    print("11. Pourcentages de tir")
    print("0. Quitter")
    print("=" * 60)

def main():
    print("\n🏀 NBA STATS MANAGER 🏀")
    print("Système de gestion de statistiques NBA\n")

    # Initialisation de la base de données
    db = NBADatabase()
    db.connect()
    db.create_tables()

    while True:
        print_menu()
        choice = input("\nVotre choix: ")

        if choice == "1":
            # recup des données
            scraper = NBAStatsScraper(season="2024-25")
            players_data = scraper.fetch_league_leaders()
            if players_data:
                db.insert_players(players_data)

        elif choice == "2":
            # Top scoreurs
            df = db.get_top_scorers(10)
            display_stats_summary(df)

        elif choice == "3":
            # Stats d'équipe
            team = input("Nom de l'équipe: ")
            df = db.get_team_stats(team)
            if not df.empty:
                display_stats_summary(df)
            else:
                print("✗ Aucun résultat trouvé")

        elif choice == "4":
            # Export CSV
            filename = input("Nom du fichier (défaut: nba_stats_export.csv): ")
            if not filename:
                filename = "nba_stats_export.csv"
            db.export_to_csv(filename)

        elif choice == "5":
            # Comparaison de joueurs
            player1 = input("Premier joueur: ")
            player2 = input("Deuxième joueur: ")
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db.conn)
            compare_players(df, player1, player2)

        elif choice == "6":
            # Calcul d'efficacité
            query = "SELECT * FROM players WHERE games_played > 10"
            df = pd.read_sql_query(query, db.conn)
            df_efficiency = calculate_efficiency(df)
            print("\n🏆 TOP 10 JOUEURS LES PLUS EFFICACES")
            display_stats_summary(df_efficiency.head(10))

        elif choice == "0":
            print("\nAu revoir!")
            db.close()
            sys.exit(0)

        elif choice == "7":
            # Graphique top scoreurs
            df = db.get_top_scorers(10)
            plot_top_scorers(df, 10)

        elif choice == "8":
            # Comparaison graphique
            player1 = input("Premier joueur: ")
            player2 = input("Deuxième joueur: ")
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db.conn)
            plot_player_comparison(df, player1, player2)

        elif choice == "9":
            # Analyse d'équipe
            team = input("Nom de l'équipe: ")
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db.conn)
            plot_team_analysis(df, team)

        elif choice == "10":
            # Nuage de points
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db.conn)
            plot_efficiency_scatter(df)

        elif choice == "11":
            # Pourcentages de tir
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, db.conn)
            plot_shooting_percentages(df, 10)

        else:
            print("✗ Choix invalide")


if __name__ == "__main__":
    main()
