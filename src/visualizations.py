import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_top_scorers(df: pd.DataFrame, limit: int = 10):

    # Préparer les données
    data = df.head(limit).sort_values('points_per_game', ascending=True)

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(data['player_name'], data['points_per_game'],
                   color='#1f77b4', edgecolor='black', linewidth=0.5)

    # Labels et titre
    ax.set_xlabel('Points par match', fontsize=11, fontweight='bold')
    ax.set_title(f'Top {limit} Scoreurs NBA 2024-25',
                 fontsize=14, fontweight='bold', pad=20)

    # Ajouter les valeurs sur les barres
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{width:.1f}',
                ha='left', va='center', fontsize=9)

    # Grille discrète
    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig('top_scorers.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique sauvegardé: top_scorers.png")
    plt.show()


def plot_player_comparison(df: pd.DataFrame, player1: str, player2: str):

    # Récupérer les données
    p1 = df[df['player_name'].str.contains(player1, case=False)]
    p2 = df[df['player_name'].str.contains(player2, case=False)]

    if p1.empty or p2.empty:
        print("✗ Un ou plusieurs joueurs non trouvés")
        return

    p1 = p1.iloc[0]
    p2 = p2.iloc[0]

    # Catégories à comparer
    categories = ['PPG', 'RPG', 'APG', 'SPG', 'BPG']
    p1_values = [p1['points_per_game'], p1['rebounds_per_game'],
                 p1['assists_per_game'], p1['steals_per_game'],
                 p1['blocks_per_game']]
    p2_values = [p2['points_per_game'], p2['rebounds_per_game'],
                 p2['assists_per_game'], p2['steals_per_game'],
                 p2['blocks_per_game']]

    # Créer le graphique
    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width / 2, p1_values, width, label=p1['player_name'],
                   color='#1f77b4', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width / 2, p2_values, width, label=p2['player_name'],
                   color='#ff7f0e', edgecolor='black', linewidth=0.5)

    # Labels
    ax.set_xlabel('Statistiques', fontsize=11, fontweight='bold')
    ax.set_ylabel('Valeur', fontsize=11, fontweight='bold')
    ax.set_title('Comparaison de joueurs', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig('player_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique sauvegardé: player_comparison.png")
    plt.show()


def plot_team_analysis(df: pd.DataFrame, team_name: str):

    team_data = df[df['team_name'].str.contains(team_name, case=False)]

    if team_data.empty:
        print("✗ Équipe non trouvée")
        return

    team_data = team_data.sort_values('points_per_game', ascending=False).head(8)

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))

    x = range(len(team_data))
    width = 0.25

    bars1 = ax.bar([i - width for i in x], team_data['points_per_game'],
                   width, label='PPG', color='#1f77b4', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar([i for i in x], team_data['rebounds_per_game'],
                   width, label='RPG', color='#2ca02c', edgecolor='black', linewidth=0.5)
    bars3 = ax.bar([i + width for i in x], team_data['assists_per_game'],
                   width, label='APG', color='#ff7f0e', edgecolor='black', linewidth=0.5)

    # Labels
    ax.set_xlabel('Joueurs', fontsize=11, fontweight='bold')
    ax.set_ylabel('Statistiques', fontsize=11, fontweight='bold')
    ax.set_title(f'Analyse de l\'équipe - {team_name}',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(team_data['player_name'], rotation=45, ha='right')
    ax.legend(frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig('team_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique sauvegardé: team_analysis.png")
    plt.show()


def plot_efficiency_scatter(df: pd.DataFrame):

    # Calculer l'efficacité
    df = df.copy()
    df['efficiency'] = df['points_per_game'] + df['rebounds_per_game'] + df['assists_per_game']

    # Filtrer les joueurs avec au moins 15 matchs
    df = df[df['games_played'] >= 15]

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(df['points_per_game'], df['efficiency'],
                         s=df['games_played'] * 3, alpha=0.6,
                         c=df['assists_per_game'], cmap='viridis',
                         edgecolors='black', linewidth=0.5)

    # Ajouter les noms des meilleurs joueurs
    top_players = df.nlargest(8, 'efficiency')
    for _, player in top_players.iterrows():
        ax.annotate(player['player_name'],
                    (player['points_per_game'], player['efficiency']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=8, alpha=0.8)

    # Labels
    ax.set_xlabel('Points par match', fontsize=11, fontweight='bold')
    ax.set_ylabel('Score d\'efficacité', fontsize=11, fontweight='bold')
    ax.set_title('Points vs Efficacité globale', fontsize=14, fontweight='bold', pad=20)

    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Passes par match', fontsize=10)

    # Grille
    ax.grid(alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig('efficiency_scatter.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique sauvegardé: efficiency_scatter.png")
    plt.show()


def plot_shooting_percentages(df: pd.DataFrame, limit: int = 10):

    # Filtrer et trier
    data = df[df['games_played'] >= 15].nlargest(limit, 'points_per_game')

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))

    x = range(len(data))
    width = 0.25

    bars1 = ax.bar([i - width for i in x], data['field_goal_pct'],
                   width, label='FG%', color='#1f77b4', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar([i for i in x], data['three_point_pct'],
                   width, label='3P%', color='#ff7f0e', edgecolor='black', linewidth=0.5)
    bars3 = ax.bar([i + width for i in x], data['free_throw_pct'],
                   width, label='FT%', color='#2ca02c', edgecolor='black', linewidth=0.5)

    # Labels
    ax.set_xlabel('Joueurs', fontsize=11, fontweight='bold')
    ax.set_ylabel('Pourcentage (%)', fontsize=11, fontweight='bold')
    ax.set_title('Pourcentages de tir des meilleurs scoreurs',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(data['player_name'], rotation=45, ha='right')
    ax.legend(frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig('shooting_percentages.png', dpi=300, bbox_inches='tight')
    print("✓ Graphique sauvegardé: shooting_percentages.png")
    plt.show()