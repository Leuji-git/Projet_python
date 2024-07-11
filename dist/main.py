import tkinter as tk
from app import TMDB, RandomMovieApp

# Authentification TMDB
api_key = '5dfe8c36ac41234cb5200209235f1b5a'

def main():
    root = tk.Tk()
    tmdb_client = TMDB(api_key)  # Fais la requête
    app = RandomMovieApp(root, tmdb_client)  # Lance les différentes fonctions de l'application
    root.mainloop()

if __name__ == "__main__":
    main()
