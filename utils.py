import pandas as pd


def display_stats_summary(df: pd.DataFrame):

    print("\n" + "=" * 60)
    print("RÉSUMÉ DES STATISTIQUES NBA")
    print("=" * 60)
    print(df.to_string(index=False))
    print("=" * 60 + "\n")


def calculate_efficiency(df: pd.DataFrame) -> pd.DataFrame:

    df['efficiency'] = (
            df['points_per_game'] +
            df['rebounds_per_game'] +
            df['assists_per_game']
    )
    return df.sort_values('efficiency', ascending=False)


def compare_players(df: pd.DataFrame, player1: str, player2: str):

    p1_data = df[df['player_name'].str.contains(player1, case=False)]
    p2_data = df[df['player_name'].str.contains(player2, case=False)]

    if not p1_data.empty and not p2_data.empty:
        print(f"\n🆚 Comparaison: {player1} vs {player2}")
        print("-" * 60)
        comparison = pd.concat([p1_data, p2_data])
        print(comparison.to_string(index=False))
    else:
        print("✗ Joueur(s) non trouvé(s)")

