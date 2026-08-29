import tkinter as tk
from tkinter import ttk, messagebox

class AgriDurable:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 AgriDurable")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.dark_mode = False
        self.current_page = None

        self.colors = {
            "light": {
                "bg": "#F4F7F4",
                "card": "#FFFFFF",
                "text": "#1F2937",
                "muted": "#6B7280",
                "green": "#35A853",
                "green_dark": "#218739",
                "border": "#E5E7EB"
            },
            "dark": {
                "bg": "#111827",
                "card": "#1F2937",
                "text": "#F9FAFB",
                "muted": "#9CA3AF",
                "green": "#6EDB45",
                "green_dark": "#35A853",
                "border": "#374151"
            }
        }

        self.create_layout()
        self.show_page("Accueil")
        self.apply_theme()

    # =====================================================
    # COULEURS
    # =====================================================

    def theme(self):
        return self.colors["dark" if self.dark_mode else "light"]

    # =====================================================
    # STRUCTURE PRINCIPALE
    # =====================================================

    def create_layout(self):

        # Barre supérieure
        self.header = tk.Frame(self.root, height=70)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.logo = tk.Label(
            self.header,
            text="🌱  AgriDurable",
            font=("Arial", 21, "bold")
        )
        self.logo.pack(side="left", padx=25)

        self.theme_button = tk.Button(
            self.header,
            text="☀️",
            font=("Arial", 16),
            width=4,
            relief="flat",
            command=self.toggle_theme,
            cursor="hand2"
        )
        self.theme_button.pack(side="right", padx=20)

        # Zone principale
        self.main = tk.Frame(self.root)
        self.main.pack(fill="both", expand=True)

        # Menu gauche
        self.sidebar = tk.Frame(self.main, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.menu_title = tk.Label(
            self.sidebar,
            text="MENU",
            font=("Arial", 10, "bold")
        )
        self.menu_title.pack(anchor="w", padx=25, pady=(25, 15))

        pages = [
            ("🏠", "Accueil"),
            ("🌾", "Cultures"),
            ("💧", "Eau"),
            ("🌱", "Sol"),
            ("📊", "Statistiques"),
            ("♻️", "Conseils"),
            ("👤", "Profil")
        ]

        self.menu_buttons = []

        for icon, name in pages:
            button = tk.Button(
                self.sidebar,
                text=f"{icon}   {name}",
                font=("Arial", 12),
                anchor="w",
                relief="flat",
                bd=0,
                padx=20,
                pady=13,
                cursor="hand2",
                command=lambda page=name: self.show_page(page)
            )

            button.pack(fill="x", padx=12, pady=3)
            self.menu_buttons.append(button)

        # Zone de contenu
        self.content = tk.Frame(self.main)
        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

    # =====================================================
    # NAVIGATION
    # =====================================================

    def show_page(self, page):

        self.current_page = page

        for widget in self.content.winfo_children():
            widget.destroy()

        if page == "Accueil":
            self.page_accueil()

        elif page == "Cultures":
            self.page_cultures()

        elif page == "Eau":
            self.page_eau()

        elif page == "Sol":
            self.page_sol()

        elif page == "Statistiques":
            self.page_statistiques()

        elif page == "Conseils":
            self.page_conseils()

        elif page == "Profil":
            self.page_profil()

        self.update_menu()

    # =====================================================
    # MENU ACTIF
    # =====================================================

    def update_menu(self):

        c = self.theme()

        for button in self.menu_buttons:

            if self.current_page in button.cget("text"):
                button.config(
                    bg=c["green"],
                    fg="white"
                )
            else:
                button.config(
                    bg=c["card"],
                    fg=c["text"]
                )

    # =====================================================
    # PAGE ACCUEIL
    # =====================================================

    def page_accueil(self):

        c = self.theme()

        title = tk.Label(
            self.content,
            text="Bonjour 👋",
            font=("Arial", 28, "bold"),
            bg=c["bg"],
            fg=c["text"]
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            self.content,
            text="Bienvenue sur votre tableau de bord agricole.",
            font=("Arial", 12),
            bg=c["bg"],
            fg=c["muted"]
        )
        subtitle.pack(anchor="w", pady=(5, 25))

        # Cartes statistiques
        cards = tk.Frame(self.content, bg=c["bg"])
        cards.pack(fill="x")

        data = [
            ("🌾", "Cultures", "5"),
            ("💧", "Eau utilisée", "12 450 L"),
            ("📊", "Production", "3 200 kg"),
            ("🌱", "État du sol", "Bon")
        ]

        for icon, title, value in data:

            card = tk.Frame(
                cards,
                bg=c["card"],
                padx=20,
                pady=18
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=7
            )

            tk.Label(
                card,
                text=icon,
                font=("Arial", 24),
                bg=c["card"]
            ).pack(anchor="w")

            tk.Label(
                card,
                text=title,
                font=("Arial", 11),
                bg=c["card"],
                fg=c["muted"]
            ).pack(anchor="w", pady=(8, 2))

            tk.Label(
                card,
                text=value,
                font=("Arial", 19, "bold"),
                bg=c["card"],
                fg=c["text"]
            ).pack(anchor="w")

        # Conseil
        conseil = tk.Frame(
            self.content,
            bg=c["card"],
            padx=25,
            pady=25
        )
        conseil.pack(fill="x", pady=30)

        tk.Label(
            conseil,
            text="♻️ Conseil du jour",
            font=("Arial", 18, "bold"),
            bg=c["card"],
            fg=c["green"]
        ).pack(anchor="w")

        tk.Label(
            conseil,
            text="Utilisez l'irrigation goutte-à-goutte pour réduire\n"
                 "la consommation d'eau et protéger vos cultures.",
            font=("Arial", 12),
            bg=c["card"],
            fg=c["text"],
            justify="left"
        ).pack(anchor="w", pady=10)

    # =====================================================
    # PAGE CULTURES
    # =====================================================

    def page_cultures(self):

        c = self.theme()

        self.page_title("🌾 Mes cultures")

        add_button = tk.Button(
            self.content,
            text="+ Ajouter une culture",
            font=("Arial", 11, "bold"),
            bg=c["green"],
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.add_culture
        )
        add_button.pack(anchor="e", pady=(0, 20))

        cultures = [
            ("🌽", "Maïs", "2 hectares", "Bon"),
            ("🍅", "Tomates", "1 hectare", "Excellent"),
            ("🥕", "Carottes", "0.5 hectare", "Bon"),
            ("🥬", "Laitue", "0.3 hectare", "Excellent")
        ]

        for icon, name, surface, status in cultures:

            card = tk.Frame(
                self.content,
                bg=c["card"],
                padx=20,
                pady=15
            )
            card.pack(fill="x", pady=5)

            tk.Label(
                card,
                text=icon,
                font=("Arial", 25),
                bg=c["card"]
            ).pack(side="left")

            info = tk.Frame(card, bg=c["card"])
            info.pack(side="left", padx=20)

            tk.Label(
                info,
                text=name,
                font=("Arial", 14, "bold"),
                bg=c["card"],
                fg=c["text"]
            ).pack(anchor="w")

            tk.Label(
                info,
                text=surface,
                font=("Arial", 10),
                bg=c["card"],
                fg=c["muted"]
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"● {status}",
                font=("Arial", 11, "bold"),
                bg=c["card"],
                fg=c["green"]
            ).pack(side="right")

    # =====================================================
    # AJOUT CULTURE
    # =====================================================

    def add_culture(self):

        c = self.theme()

        window = tk.Toplevel(self.root)
        window.title("Ajouter une culture")
        window.geometry("400x400")
        window.config(bg=c["bg"])

        tk.Label(
            window,
            text="🌾 Nouvelle culture",
            font=("Arial", 20, "bold"),
            bg=c["bg"],
            fg=c["text"]
        ).pack(pady=25)

        entries = []

        for label in ["Nom de la culture", "Surface", "Date de plantation"]:

            tk.Label(
                window,
                text=label,
                bg=c["bg"],
                fg=c["text"],
                font=("Arial", 11)
            ).pack(anchor="w", padx=40)

            entry = tk.Entry(
                window,
                font=("Arial", 12)
            )
            entry.pack(fill="x", padx=40, pady=(5, 15))

            entries.append(entry)

        tk.Button(
            window,
            text="Enregistrer",
            bg=c["green"],
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: messagebox.showinfo(
                "AgriDurable",
                "Culture enregistrée avec succès !"
            )
        ).pack(pady=15)

    # =====================================================
    # PAGE EAU
    # =====================================================

    def page_eau(self):

        c = self.theme()

        self.page_title("💧 Gestion de l'eau")

        card = tk.Frame(
            self.content,
            bg=c["card"],
            padx=30,
            pady=30
        )
        card.pack(fill="x")

        tk.Label(
            card,
            text="Consommation actuelle",
            font=("Arial", 13),
            bg=c["card"],
            fg=c["muted"]
        ).pack(anchor="w")

        tk.Label(
            card,
            text="12 450 L",
            font=("Arial", 32, "bold"),
            bg=c["card"],
            fg=c["green"]
        ).pack(anchor="w", pady=10)

        tk.Label(
            card,
            text="Objectif mensuel : 15 000 L",
            font=("Arial", 11),
            bg=c["card"],
            fg=c["text"]
        ).pack(anchor="w")

        progress = ttk.Progressbar(
            card,
            length=500,
            value=83,
            mode="determinate"
        )
        progress.pack(fill="x", pady=20)

        tk.Label(
            card,
            text="💡 Vous êtes dans la limite recommandée.",
            font=("Arial", 11),
            bg=c["card"],
            fg=c["green"]
        ).pack(anchor="w")

    # =====================================================
    # PAGE SOL
    # =====================================================

    def page_sol(self):

        c = self.theme()

        self.page_title("🌱 État du sol")

        data = [
            ("Humidité", "68 %"),
            ("Fertilité", "Bonne"),
            ("pH", "6.7"),
            ("Matière organique", "Élevée")
        ]

        for name, value in data:

            card = tk.Frame(
                self.content,
                bg=c["card"],
                padx=25,
                pady=18
            )
            card.pack(fill="x", pady=5)

            tk.Label(
                card,
                text=name,
                font=("Arial", 13),
                bg=c["card"],
                fg=c["text"]
            ).pack(side="left")

            tk.Label(
                card,
                text=value,
                font=("Arial", 13, "bold"),
                bg=c["card"],
                fg=c["green"]
            ).pack(side="right")

    # =====================================================
    # PAGE STATISTIQUES
    # =====================================================

    def page_statistiques(self):

        c = self.theme()

        self.page_title("📊 Statistiques")

        card = tk.Frame(
            self.content,
            bg=c["card"],
            padx=25,
            pady=25
        )
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="Production des derniers mois",
            font=("Arial", 16, "bold"),
            bg=c["card"],
            fg=c["text"]
        ).pack(anchor="w")

        # Graphique simple
        graph = tk.Canvas(
            card,
            bg=c["card"],
            highlightthickness=0
        )
        graph.pack(fill="both", expand=True, pady=20)

        values = [40, 55, 45, 70, 85, 95]

        width = 600
        height = 300

        for i, value in enumerate(values):

            x = 60 + i * 90
            y = height - value * 2

            graph.create_rectangle(
                x,
                y,
                x + 45,
                height,
                fill=c["green"],
                outline=""
            )

            graph.create_text(
                x + 22,
                height + 15,
                text=f"M{i + 1}",
                fill=c["text"]
            )

    # =====================================================
    # PAGE CONSEILS
    # =====================================================

    def page_conseils(self):

        c = self.theme()

        self.page_title("♻️ Conseils écologiques")

        conseils = [
            ("💧", "Économisez l'eau",
             "Utilisez une irrigation adaptée aux besoins des cultures."),

            ("🌱", "Protégez le sol",
             "Utilisez du compost et pratiquez la rotation des cultures."),

            ("🐝", "Protégez la biodiversité",
             "Préservez les insectes utiles et plantez des haies."),

            ("♻️", "Réduisez les déchets",
             "Valorisez les déchets agricoles grâce au compostage.")
        ]

        for icon, title, text in conseils:

            card = tk.Frame(
                self.content,
                bg=c["card"],
                padx=25,
                pady=20
            )
            card.pack(fill="x", pady=7)

            tk.Label(
                card,
                text=icon,
                font=("Arial", 25),
                bg=c["card"]
            ).pack(side="left")

            info = tk.Frame(card, bg=c["card"])
            info.pack(side="left", padx=20)

            tk.Label(
                info,
                text=title,
                font=("Arial", 14, "bold"),
                bg=c["card"],
                fg=c["text"]
            ).pack(anchor="w")

            tk.Label(
                info,
                text=text,
                font=("Arial", 11),
                bg=c["card"],
                fg=c["muted"]
            ).pack(anchor="w", pady=5)

    # =====================================================
    # PAGE PROFIL
    # =====================================================

    def page_profil(self):

        c = self.theme()

        self.page_title("👤 Mon profil")

        card = tk.Frame(
            self.content,
            bg=c["card"],
            padx=30,
            pady=30
        )
        card.pack(fill="x")

        tk.Label(
            card,
            text="👨‍🌾",
            font=("Arial", 50),
            bg=c["card"]
        ).pack()

        tk.Label(
            card,
            text="Agriculteur",
            font=("Arial", 20, "bold"),
            bg=c["card"],
            fg=c["text"]
        ).pack(pady=10)

        tk.Label(
            card,
            text="Gestionnaire de l'exploitation",
            font=("Arial", 11),
            bg=c["card"],
            fg=c["muted"]
        ).pack()

        tk.Button(
            card,
            text="Modifier le profil",
            bg=c["green"],
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(pady=20)

    # =====================================================
    # TITRE DES PAGES
    # =====================================================

    def page_title(self, title):

        c = self.theme()

        tk.Label(
            self.content,
            text=title,
            font=("Arial", 27, "bold"),
            bg=c["bg"],
            fg=c["text"]
        ).pack(anchor="w", pady=(0, 25))

    # =====================================================
    # MODE SOMBRE / CLAIR
    # =====================================================

    def toggle_theme(self):

        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.theme_button.config(text="🌙")
        else:
            self.theme_button.config(text="☀️")

        self.apply_theme()

        # Recharge la page actuelle
        self.show_page(self.current_page)

    # =====================================================
    # APPLICATION DU THÈME
    # =====================================================

    def apply_theme(self):

        c = self.theme()

        self.root.config(bg=c["bg"])
        self.header.config(bg=c["card"])
        self.main.config(bg=c["bg"])
        self.sidebar.config(bg=c["card"])
        self.content.config(bg=c["bg"])

        self.logo.config(
            bg=c["card"],
            fg=c["green"]
        )

        self.theme_button.config(
            bg=c["card"],
            fg=c["text"],
            activebackground=c["border"]
        )

        self.menu_title.config(
            bg=c["card"],
            fg=c["muted"]
        )

        self.update_menu()


# =========================================================
# LANCEMENT
# =========================================================

root = tk.Tk()

app = AgriDurable(root)

root.mainloop()
