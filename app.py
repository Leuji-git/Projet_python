import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import webbrowser
import tkinter.font as tkFont



class TMDB:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3/'  # Url de Base



    # Fonction avec les parametres de recherche
    def get_movie(self, sort_by, page ):
        endpoint = f'{self.base_url}discover/movie'  # Endpoint populaire
        params = {  # Query parameters de la requete API
            'api_key': self.api_key,  # Api Key
            'sort_by': sort_by,  # Filtre
            'language': 'fr-FR',  # langue choisi
            'page': page # nombre de page parcouru dans la recherche
        }
        response = requests.get(endpoint, params=params)
        data = response.json()  # Conversion en json

        movies = data['results']
        random_movie = random.choice(movies)
        return random_movie



class RandomMovieApp:
    def __init__(self, master, tmdb_client):
        #Initialisation de la page
        self.master = master
        self.tmdb_client = tmdb_client
        master.title("Random Movies Finder")
        master.geometry()
        master.configure(bg='#212F3D')

        # logo de l'application
        icon = ImageTk.PhotoImage(file='app_icon.png')
        master.iconphoto(False, icon)

        #Initialisation Font perso
        bellerose = tkFont.Font(family="bellerose.ttf", size=12)
        bellerose_bold = tkFont.Font(family="bellerose.ttf", size=12, weight="bold")
        bellerose_title = tkFont.Font(family="bellerose.ttf", size=20, weight="bold")
        bellerose_link = tkFont.Font(family="bellerose.ttf", size=12, underline=1)

        # canvas des filtres
        self.filters_frame = tk.Frame(master, bg='#212F3D')
        self.filters_frame.pack(pady=10)

        # Filtre Sort
        tk.Label(self.filters_frame, text="Trier par:", font=bellerose_bold, fg="#FFFFFF", bg='#212F3D').grid(row=0, column=0, padx=5)
        self.sort_by_var = tk.StringVar(value="popularity.desc")
        sort_by_options = ["popularity.desc", "release_date.desc", "release_date.asc","popularity.desc" ]
        self.sort_by_menu = ttk.OptionMenu(self.filters_frame, self.sort_by_var, *sort_by_options)
        self.sort_by_menu.grid(row=0, column=1, padx=5)

        # Filtre Page
        tk.Label(self.filters_frame, text="Page:", font=bellerose_bold, fg="#FFFFFF", bg='#212F3D').grid(row=0, column=2, padx=5)
        self.page_entry = tk.Entry(self.filters_frame, width=5, font=bellerose)
        self.page_entry.grid(row=0, column=3, padx=5)
        self.page_entry.insert(0, "20")

        # Canvas pour affiche et detail
        self.result_frame = ttk.Frame(master)
        self.result_frame.pack(pady=20)

        #DETAIL FILM 
        self.details_frame = tk.Frame(self.result_frame, bg='#FFFFFF', bd=0, highlightthickness=0)
        self.details_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # Label Affiche du Film
        self.poster_label = tk.Label(self.result_frame, bg='#212F3D',fg="#212F3D", bd=0, highlightthickness=0)
        self.poster_label.grid(row=0, column=0, rowspan=5, padx=10, pady=10)
        self.load_default_logo()

        # Label Titre du film
        self.title_label = tk.Label(self.details_frame, text="", font=bellerose_title, fg="#212F3D", bg='#FFFFFF', bd=0, highlightthickness=0)
        self.title_label.grid(row=0, column=0, sticky='w')

        # Label Date du film
        self.release_date_label = tk.Label(self.details_frame, text="", font=bellerose_bold, fg="#212F3D", bg='#FFFFFF', bd=0, highlightthickness=0)
        self.release_date_label.grid(row=1, column=0, sticky='w')

        # Label note TMDB
        self.vote_average_label = tk.Label(self.details_frame, text="", font=bellerose_bold, fg="#212F3D", bg='#FFFFFF', bd=0, highlightthickness=0)
        self.vote_average_label.grid(row=2, column=0, sticky='w')

        # URL du Film
        self.movie_url_label = tk.Label(self.details_frame, text="", font=bellerose_link, fg="#212F3D", bg='#FFFFFF', cursor="hand2")
        self.movie_url_label.grid(row=3, column=0, sticky='w')
        self.movie_url_label.bind("<Button-1>", self.open_url)

        # Description du film
        self.overview_label = tk.Label(self.result_frame, text="", font=bellerose, fg="#212F3D", bg='#FFFFFF', wraplength=400, justify="left", bd=0, highlightthickness=0)
        self.overview_label.grid(row=0, column=2, padx=10, pady=10, sticky='n')
        
        # Find
        self.find_button = tk.Button(master, text="Find Movie", command=self.find_random_movie, font=bellerose_bold, bg="#FFFFFF", fg="#212F3D")
        self.find_button.pack(pady=10)

        # Logo information
        info_logo = Image.open("info_icon.png")
        info_logo = info_logo.resize((20, 20), Image.LANCZOS)
        self.info_logo_photo = ImageTk.PhotoImage(info_logo)
        self.info_button = tk.Button(master, image=self.info_logo_photo, command=self.show_info_window, bg='#212F3D', borderwidth=0)
        self.info_button.pack(anchor='ne', padx=10, pady=10)

        # Enleve les champs Detail et Overview à initation de l'application
        self.details_frame.grid_remove()
        self.overview_label.grid_remove()



    # Precharge les logos et le redimensionne
    def load_default_logo(self):
        logo = Image.open("app_icon.png")
        logo = logo.resize((100, 100), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo)
        self.poster_label.config(image=logo_photo)
        self.poster_label.image = logo_photo



    # Affiche la boite de help
    def show_info_window(self):
        info_window = tk.Toplevel(self.master)
        info_window.title("Information")
        info_window.geometry("350x250")
        info_window.configure(bg='#212F3D')
        help_text = ("Random Movie Finder est une application pour trouver des films aléatoires.\n\n"
                     "Bienvenue dans le centre d'informations:\n\n"
                     "1 - Ajuster vos filtres pour une recherche personnalisé\n"
                     "2 - Le filtre 'Page' permet de plus ou moins élargir son champs actions (20 par defaut)\n"
                     "4 -  Cliquer sur 'Find Movie'\n")
        tk.Label(info_window, text=help_text, font=("Calibri", 12), fg="#FFFFFF", bg='#212F3D', wraplength=350, justify="left").pack(pady=10)



    # Fonction redirection internet
    def open_url(self, event):
        webbrowser.open_new(event.widget.cget("text"))




    # Fonction resultat
    def find_random_movie(self):
        sort_by = self.sort_by_var.get()
        page = int(self.page_entry.get())
        movie = self.tmdb_client.get_movie(sort_by, page)
        title = movie['title']
        release_date = movie['release_date']
        vote_average = movie['vote_average']
        overview = movie['overview']
        poster_path = movie['poster_path']
        movie_url = f"https://www.themoviedb.org/movie/{movie['id']}"

        # Afficher les informations sur le film
        self.title_label.config(text=f"{title}")
        self.release_date_label.config(text=f"({release_date})")
        self.vote_average_label.config(text=f"Indice TMDB: {vote_average}")
        self.movie_url_label.config(text=movie_url)
        self.overview_label.config(text=f"{overview}")

        # Afficher l'affiche du film
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            response = requests.get(poster_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((200, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.poster_label.config(image=photo)
            self.poster_label.image = photo
        else:
                self.load_default_logo()

        #Affiche les champs detail et overview apres la recherche
        self.details_frame.grid()
        self.overview_label.grid()