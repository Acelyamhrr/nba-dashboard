import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from database import NBADatabase  # Enlève "src."
from scraper import NBAStatsScraper
from visualizations import (plot_top_scorers, plot_player_comparison,
                            plot_team_analysis, plot_efficiency_scatter,
                            plot_shooting_percentages)


class NBAStatsGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NBA Stats Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#000000')

        # Connexion à la base de données
        self.db = NBADatabase()
        self.db.connect()
        self.db.create_tables()

        self.setup_ui()

    def setup_ui(self):
        """Met en place tous les éléments de l'interface"""

        # Configuration du style général
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#000000')
        style.configure('TButton', background='#FFFFFF', foreground='#000000',
                        padding=10, font=('Arial', 10, 'bold'))
        style.map('TButton', background=[('active', '#CCCCCC')])
        style.configure('TLabel', background='#000000', foreground='#FFFFFF',
                        font=('Arial', 11))
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'),
                        foreground='#FFFFFF')

        # Bandeau du haut avec le titre
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20, padx=20, fill=tk.X)

        title = ttk.Label(header_frame, text="🏀 NBA STATS MANAGER 🏀",
                          style='Title.TLabel')
        title.pack()

        subtitle = ttk.Label(header_frame,
                             text="Gestionnaire de statistiques NBA 2024-25",
                             font=('Arial', 10))
        subtitle.pack()

        # Zone principale divisée en deux parties
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Partie gauche avec les boutons d'action
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        actions_label = ttk.Label(left_frame, text="ACTIONS",
                                  font=('Arial', 14, 'bold'))
        actions_label.pack(pady=(0, 10))

        # Bouton pour récupérer les données de l'API
        btn_fetch = tk.Button(left_frame, text="Récupérer les données NBA",
                              command=self.fetch_data, bg='#FFFFFF', fg='#000000',
                              font=('Arial', 10, 'bold'), cursor='hand2',
                              relief=tk.FLAT, padx=20, pady=10)
        btn_fetch.pack(fill=tk.X, pady=5)

        # Afficher les meilleurs scoreurs
        btn_top = tk.Button(left_frame, text="Top 10 Scoreurs",
                            command=self.show_top_scorers, bg='#FFFFFF', fg='#000000',
                            font=('Arial', 10, 'bold'), cursor='hand2',
                            relief=tk.FLAT, padx=20, pady=10)
        btn_top.pack(fill=tk.X, pady=5)

        # Chercher les stats d'une équipe
        btn_team = tk.Button(left_frame, text="Rechercher une équipe",
                             command=self.search_team, bg='#FFFFFF', fg='#000000',
                             font=('Arial', 10, 'bold'), cursor='hand2',
                             relief=tk.FLAT, padx=20, pady=10)
        btn_team.pack(fill=tk.X, pady=5)

        # Comparer deux joueurs
        btn_compare = tk.Button(left_frame, text="Comparer deux joueurs",
                                command=self.compare_players, bg='#FFFFFF', fg='#000000',
                                font=('Arial', 10, 'bold'), cursor='hand2',
                                relief=tk.FLAT, padx=20, pady=10)
        btn_compare.pack(fill=tk.X, pady=5)

        # Exporter toute la base en CSV
        btn_export = tk.Button(left_frame, text="Exporter en CSV",
                               command=self.export_csv, bg='#FFFFFF', fg='#000000',
                               font=('Arial', 10, 'bold'), cursor='hand2',
                               relief=tk.FLAT, padx=20, pady=10)
        btn_export.pack(fill=tk.X, pady=5)

        # Section pour les graphiques
        separator = ttk.Label(left_frame, text="VISUALISATIONS",
                              font=('Arial', 14, 'bold'))
        separator.pack(pady=(20, 10))

        # Graphique des top scoreurs
        btn_plot1 = tk.Button(left_frame, text="Graphique top scoreurs",
                              command=self.plot_top, bg='#000000', fg='#FFFFFF',
                              font=('Arial', 10, 'bold'), cursor='hand2',
                              relief=tk.FLAT, padx=20, pady=10,
                              highlightbackground='#FFFFFF', highlightthickness=1)
        btn_plot1.pack(fill=tk.X, pady=5)

        # Graphique de comparaison entre deux joueurs
        btn_plot2 = tk.Button(left_frame, text="Comparer joueurs (graphique)",
                              command=self.plot_compare, bg='#000000', fg='#FFFFFF',
                              font=('Arial', 10, 'bold'), cursor='hand2',
                              relief=tk.FLAT, padx=20, pady=10,
                              highlightbackground='#FFFFFF', highlightthickness=1)
        btn_plot2.pack(fill=tk.X, pady=5)

        # Graphique d'analyse d'équipe
        btn_plot3 = tk.Button(left_frame, text="Analyser une équipe",
                              command=self.plot_team, bg='#000000', fg='#FFFFFF',
                              font=('Arial', 10, 'bold'), cursor='hand2',
                              relief=tk.FLAT, padx=20, pady=10,
                              highlightbackground='#FFFFFF', highlightthickness=1)
        btn_plot3.pack(fill=tk.X, pady=5)

        # Nuage de points pour l'efficacité
        btn_plot4 = tk.Button(left_frame, text="Nuage de points efficacité",
                              command=self.plot_scatter, bg='#000000', fg='#FFFFFF',
                              font=('Arial', 10, 'bold'), cursor='hand2',
                              relief=tk.FLAT, padx=20, pady=10,
                              highlightbackground='#FFFFFF', highlightthickness=1)
        btn_plot4.pack(fill=tk.X, pady=5)

        # Partie droite pour afficher les résultats
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        results_label = ttk.Label(right_frame, text="RÉSULTATS",
                                  font=('Arial', 14, 'bold'))
        results_label.pack(pady=(0, 10))

        # Zone de texte avec barre de défilement
        text_frame = ttk.Frame(right_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_output = tk.Text(text_frame, wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set,
                                   bg='#000000', fg='#FFFFFF',
                                   font=('Courier', 10), padx=10, pady=10,
                                   relief=tk.FLAT, insertbackground='#FFFFFF')
        self.text_output.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_output.yview)

        # Message au démarrage
        self.print_output("Bienvenue dans NBA Stats Manager !\n\n"
                          "Cliquez sur '📥 Récupérer les données NBA' pour commencer.\n")

    def print_output(self, text):
        """Ajoute du texte dans la zone de résultats"""
        self.text_output.insert(tk.END, text + "\n")
        self.text_output.see(tk.END)

    def clear_output(self):
        """Vide complètement la zone de résultats"""
        self.text_output.delete(1.0, tk.END)

    def fetch_data(self):
        """Récupère les stats depuis l'API NBA"""
        self.clear_output()
        self.print_output("📥 Récupération des données NBA en cours...")
        self.root.update()

        try:
            scraper = NBAStatsScraper(season="2024-25")
            players_data = scraper.fetch_league_leaders()
            if players_data:
                self.db.insert_players(players_data)
                self.print_output(f"✓ {len(players_data)} joueurs récupérés et stockés")
                messagebox.showinfo("Succès", "Données récupérées avec succès !")
            else:
                self.print_output("✗ Erreur lors de la récupération")
                messagebox.showerror("Erreur", "Impossible de récupérer les données")
        except Exception as e:
            self.print_output(f"✗ Erreur: {str(e)}")
            messagebox.showerror("Erreur", str(e))

    def show_top_scorers(self):
        """Affiche le classement des 10 meilleurs scoreurs"""
        self.clear_output()
        try:
            df = self.db.get_top_scorers(10)
            if df.empty:
                self.print_output("⚠ Aucune donnée. Récupérez d'abord les données NBA.")
                return

            self.print_output("🏆 TOP 10 SCOREURS NBA 2024-25\n")
            self.print_output("=" * 70)
            for idx, row in df.iterrows():
                self.print_output(f"{idx + 1}. {row['player_name']:25} - {row['team_name']:4} "
                                  f"| {row['points_per_game']:.1f} PPG  "
                                  f"{row['rebounds_per_game']:.1f} RPG  "
                                  f"{row['assists_per_game']:.1f} APG")
            self.print_output("=" * 70)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def search_team(self):
        """Cherche tous les joueurs d'une équipe donnée"""
        team = self.ask_input("Nom de l'équipe", "Entrez le nom de l'équipe:")
        if not team:
            return

        self.clear_output()
        try:
            df = self.db.get_team_stats(team)
            if df.empty:
                self.print_output(f"✗ Aucun résultat pour '{team}'")
                return

            self.print_output(f"👥 STATISTIQUES DE L'ÉQUIPE : {team.upper()}\n")
            self.print_output("=" * 70)
            for idx, row in df.iterrows():
                self.print_output(f"{row['player_name']:25} - {row['position']:3} "
                                  f"| {row['points_per_game']:.1f} PPG  "
                                  f"{row['rebounds_per_game']:.1f} RPG  "
                                  f"{row['assists_per_game']:.1f} APG")
            self.print_output("=" * 70)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def compare_players(self):
        """Compare les stats de deux joueurs côte à côte"""
        player1 = self.ask_input("Premier joueur", "Nom du premier joueur:")
        if not player1:
            return
        player2 = self.ask_input("Deuxième joueur", "Nom du deuxième joueur:")
        if not player2:
            return

        self.clear_output()
        try:
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, self.db.conn)

            p1 = df[df['player_name'].str.contains(player1, case=False)]
            p2 = df[df['player_name'].str.contains(player2, case=False)]

            if p1.empty or p2.empty:
                self.print_output("✗ Un ou plusieurs joueurs non trouvés")
                return

            p1 = p1.iloc[0]
            p2 = p2.iloc[0]

            self.print_output(f"🆚 COMPARAISON : {p1['player_name']} vs {p2['player_name']}\n")
            self.print_output("=" * 70)
            self.print_output(f"{'Statistique':<20} {p1['player_name']:<20} {p2['player_name']:<20}")
            self.print_output("-" * 70)
            self.print_output(f"{'Points/match':<20} {p1['points_per_game']:<20.1f} {p2['points_per_game']:<20.1f}")
            self.print_output(
                f"{'Rebonds/match':<20} {p1['rebounds_per_game']:<20.1f} {p2['rebounds_per_game']:<20.1f}")
            self.print_output(f"{'Passes/match':<20} {p1['assists_per_game']:<20.1f} {p2['assists_per_game']:<20.1f}")
            self.print_output(
                f"{'Interceptions/match':<20} {p1['steals_per_game']:<20.1f} {p2['steals_per_game']:<20.1f}")
            self.print_output(f"{'Contres/match':<20} {p1['blocks_per_game']:<20.1f} {p2['blocks_per_game']:<20.1f}")
            self.print_output("=" * 70)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def export_csv(self):
        """Exporte toute la base de données dans un fichier CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.db.export_to_csv(filename)
                self.print_output(f"✓ Données exportées vers {filename}")
                messagebox.showinfo("Succès", f"Fichier exporté : {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def plot_top(self):
        """Génère un graphique des top scoreurs"""
        try:
            df = self.db.get_top_scorers(10)
            if df.empty:
                messagebox.showwarning("Attention", "Aucune donnée disponible")
                return
            plot_top_scorers(df, 10)
            self.print_output("✓ Graphique généré : top_scorers.png")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def plot_compare(self):
        """Génère un graphique comparant deux joueurs"""
        player1 = self.ask_input("Premier joueur", "Nom du premier joueur:")
        if not player1:
            return
        player2 = self.ask_input("Deuxième joueur", "Nom du deuxième joueur:")
        if not player2:
            return

        try:
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, self.db.conn)
            plot_player_comparison(df, player1, player2)
            self.print_output(f"✓ Graphique généré : player_comparison.png")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def plot_team(self):
        """Génère un graphique analysant une équipe"""
        team = self.ask_input("Nom de l'équipe", "Entrez le nom de l'équipe:")
        if not team:
            return

        try:
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, self.db.conn)
            plot_team_analysis(df, team)
            self.print_output(f"✓ Graphique généré : team_analysis.png")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def plot_scatter(self):
        """Génère un nuage de points pour l'efficacité"""
        try:
            query = "SELECT * FROM players"
            df = pd.read_sql_query(query, self.db.conn)
            plot_efficiency_scatter(df)
            self.print_output("✓ Graphique généré : efficiency_scatter.png")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def ask_input(self, title, prompt):
        """Ouvre une petite fenêtre pour demander une info à l'utilisateur"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.configure(bg='#000000')
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text=prompt, font=('Arial', 11)).pack(pady=20)

        entry = tk.Entry(dialog, font=('Arial', 11), width=30, bg='#FFFFFF', fg='#000000')
        entry.pack(pady=10)
        entry.focus()

        result = [None]

        def on_ok():
            result[0] = entry.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        # Bouton OK
        tk.Button(btn_frame, text="OK", command=on_ok, bg='#FFFFFF',
                  fg='#000000', font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        # Bouton Annuler
        tk.Button(btn_frame, text="Annuler", command=on_cancel, bg='#000000',
                  fg='#FFFFFF', font=('Arial', 10, 'bold'), padx=20, pady=5,
                  highlightbackground='#FFFFFF', highlightthickness=1).pack(side=tk.LEFT, padx=5)

        # Raccourcis clavier
        entry.bind('<Return>', lambda e: on_ok())
        entry.bind('<Escape>', lambda e: on_cancel())

        dialog.wait_window()
        return result[0]

    def run(self):
        """Lance l'application"""
        self.root.mainloop()
        self.db.close()


if __name__ == "__main__":
    app = NBAStatsGUI()
    app.run()