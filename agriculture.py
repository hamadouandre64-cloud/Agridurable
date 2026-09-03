import datetime
import re
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AgriDurable - Système d'Aide à la Décision Agricole",
    page_icon="🌱",
    layout="wide",
)

# --- BASE DE DONNÉES GÉOGRAPHIQUE & PÉDOLOGIQUE ---
DONNEES_AGRI = {
    "Togo": {
        "Plateaux": {
            "Atakpamé": {
                "villages": ["Centre-Ville", "Adéta", "Kpèlè", "Agbonou", "Fagou"],
                "sols": ["Sols ferrallitiques profonds", "Limono-argileux", "Humifère"]
            },
            "Kpalimé": {
                "villages": ["Kpalimé Centre", "Agou Gadzépé", "Tové", "Kpadapé"],
                "sols": ["Sols forestiers riches", "Ferrallitiques", "Argilo-limoneux"]
            }
        },
        "Maritime": {
            "Lomé": {
                "villages": ["Bè", "Agoè", "Adidogomé", "Baguida"],
                "sols": ["Sols sablonneux", "Sablo-limoneux", "Hydromorphes"]
            },
            "Tsévié": {
                "villages": ["Tsévié Centre", "Gapé", "Badja"],
                "sols": ["Sols ferrugineux tropicaux", "Sablonneux"]
            }
        },
        "Kara": {
            "Kara": {
                "villages": ["Kara Centre", "Kozah", "Pya"],
                "sols": ["Sols ferrugineux tropicaux", "Argileux"]
            },
            "Niamtougou": {
                "villages": ["Niamtougou Centre", "Bassi", "Koka"],
                "sols": ["Sols peu évolués", "Sableux"]
            }
        }
    },
    "Bénin": {
        "Littoral": {
            "Cotonou": {
                "villages": ["Haie Vive", "Akpakpa", "Fidjrossè", "Cadjèhoun"],
                "sols": ["Sols sablonneux côtiers", "Hydromorphes"]
            },
            "Ouidah": {
                "villages": ["Ouidah Centre", "Pahou", "Zoungbodji"],
                "sols": ["Sols sablo-humifères"]
            }
        },
        "Atacora": {
            "Natitingou": {
                "villages": ["Natitingou Centre", "Perma", "Kotopouka"],
                "sols": ["Sols ferrugineux tropicaux", "Argilo-sableux"]
            },
            "Djougou": {
                "villages": ["Djougou Centre", "Bariénou", "Pélébina"],
                "sols": ["Sols minéraux bruts", "Limoneux"]
            }
        }
    },
    "Côte d'Ivoire": {
        "Lagunes": {
            "Abidjan": {
                "villages": ["Plateau", "Cocody", "Yopougon", "Marcory"],
                "sols": ["Sols ferrallitiques", "Sablo-argileux"]
            },
            "Grand-Bassam": {
                "villages": ["Bassam Centre", "Modeste", "Azuretti"],
                "sols": ["Sols sablonneux"]
            }
        },
        "Gbêkê": {
            "Bouaké": {
                "villages": ["Bouaké Centre", "Koko", "Dar-Es-Salam"],
                "sols": ["Sols ferrallitiques moyens", "Argilo-limoneux"]
            }
        }
    }
}

CULTURES_BASE = {
    "mil": {"nom": "Mil", "sol": "Sols sableux ou sablo-limoneux", "eau": "300 - 500 mm", "ph_min": 5.5, "ph_max": 7.0, "azote": "Faible"},
    "sorgho": {"nom": "Sorgho", "sol": "Sols profonds, argileux ou limoneux", "eau": "450 - 650 mm", "ph_min": 6.0, "ph_max": 7.5, "azote": "Moyen"},
    "manioc": {"nom": "Manioc", "sol": "Sols légers, meubles et bien drainés", "eau": "500 - 1000 mm", "ph_min": 5.0, "ph_max": 6.5, "azote": "Faible"},
    "riz": {"nom": "Riz", "sol": "Sols hydromorphes, argileux", "eau": "1200+ mm", "ph_min": 5.5, "ph_max": 7.0, "azote": "Élevé"},
    "maïs": {"nom": "Maïs", "sol": "Sols limoneux riches en matière organique", "eau": "500 - 800 mm", "ph_min": 6.0, "ph_max": 7.2, "azote": "Élevé"},
    "mais": {"nom": "Maïs", "sol": "Sols limoneux riches en matière organique", "eau": "500 - 800 mm", "ph_min": 6.0, "ph_max": 7.2, "azote": "Élevé"},
    "tomate": {"nom": "Tomate", "sol": "Sols riches en humus, sablo-limoneux", "eau": "400 - 600 mm", "ph_min": 6.0, "ph_max": 6.8, "azote": "Élevé"},
    "igname": {"nom": "Igname", "sol": "Sols meubles, profonds et riches en humus", "eau": "800 - 1200 mm", "ph_min": 5.5, "ph_max": 6.8, "azote": "Moyen"}
}

# --- GESTION DE L'ÉTAT ET DES PALETTES DE COULEURS ---
if "theme" not in st.session_state:
    st.session_state.theme = "Clair"

if st.session_state.theme == "Sombre":
    bg_main = "#101622"
    bg_sidebar = "#182232"
    text_color = "#e2e8f0"
    card_bg = "#1e293b"
    primary_color = "#38bdf8"
    accent_color = "#0ea5e9"
    border_color = "#334155"
    input_bg = "#0f172a"
    input_text = "#f8fafc"
else:
    bg_main = "#faf9f5"
    bg_sidebar = "#1c3829"
    text_color = "#2b2d42"
    card_bg = "#ffffff"
    primary_color = "#2d6a4f"
    accent_color = "#40916c"
    border_color = "#e9ecef"
    input_bg = "#ffffff"
    input_text = "#2b2d42"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_main}; color: {text_color}; }}
    .main {{ background-color: {bg_main}; color: {text_color}; font-family: 'Inter', sans-serif; }}
    .stSidebar {{ background-color: {bg_sidebar}; color: #ffffff; }}
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar label, .stSidebar .stMarkdown, .stSidebar p {{ color: #ffffff !important; }}
    input, textarea, select {{ background-color: {input_bg} !important; color: {input_text} !important; }}
    div.stButton > button {{
        background-color: {primary_color}; color: #ffffff; border-radius: 8px; border: none;
        padding: 0.6rem 1.2rem; font-weight: 600; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: 0.3s;
    }}
    div.stButton > button:hover {{ background-color: {accent_color}; color: #ffffff; }}
    h1 {{ color: {primary_color}; font-weight: 800; border-bottom: 3px solid {accent_color}; padding-bottom: 10px; }}
    h2, h3 {{ color: {primary_color}; font-weight: 700; }}
    div[data-testid="stMetric"] {{
        background-color: {card_bg}; color: {text_color}; padding: 15px; border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); border-top: 4px solid {accent_color};
    }}
    div[data-testid="stMetricValue"] {{ color: {text_color} !important; }}
    hr {{ margin: 2rem 0; border: none; border-top: 2px solid {border_color}; }}
    .logo-container {{ display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }}
    .logo-badge {{ background-color: {primary_color}; color: white; padding: 8px 12px; border-radius: 10px; font-size: 24px; font-weight: bold; }}
    .pro-card {{ background-color: {card_bg}; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); border: 1px solid {border_color}; margin-bottom: 15px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- BASE DE DONNÉES SQLite ---
conn = sqlite3.connect("agridurable_v3.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cultures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_culture TEXT, type_sol TEXT, date_semis DATE, etat TEXT, pays TEXT, ville TEXT, village TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS activites (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_activite DATE, description TEXT, type TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS communaute (
        id INTEGER PRIMARY KEY AUTOINCREMENT, auteur TEXT, message TEXT, date_post DATETIME
    )
""")
conn.commit()

# --- BARRE LATÉRALE ---
st.sidebar.markdown(
    """
    <div class="logo-container">
        <div class="logo-badge">🌱</div>
        <div>
            <h2 style="margin: 0; font-size: 20px; color: white;">AgriDurable</h2>
            <p style="margin: 0; font-size: 11px; color: #a3cef1;">Intelligence Agricole</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.radio("Navigation", [
    "Tableau de bord", 
    "Planificateur & Moteur", 
    "Calendrier & Suivi", 
    "Diagnostic Phytosanitaire 🔬", 
    "Communauté", 
    "Paramètres"
])

st.sidebar.markdown("---")
st.sidebar.subheader("Profil & Localisation")
nom_utilisateur = st.sidebar.text_input("Nom", "Agriculteur Expert")

pays_list = list(DONNEES_AGRI.keys())
pays = st.sidebar.selectbox("Pays", pays_list)

regions_list = list(DONNEES_AGRI[pays].keys())
region_loc = st.sidebar.selectbox("Région", regions_list)

villes_dict = DONNEES_AGRI[pays][region_loc]
ville = st.sidebar.selectbox("Ville", list(villes_dict.keys()))

villages_dispo = villes_dict[ville]["villages"]
choix_village = st.sidebar.selectbox("Village / Localité", villages_dispo + ["Autre (Personnalisé)"])
village = st.sidebar.text_input("Préciser le village", "Centre") if choix_village == "Autre (Personnalisé)" else choix_village

sols_disponibles = villes_dict[ville]["sols"]
sol_local_choisi = st.sidebar.selectbox("Type de sol de votre terre locale", sols_disponibles)

st.sidebar.markdown("---")
st.sidebar.subheader("Configuration Système")
alerte_eau = st.sidebar.checkbox("Alertes d'irrigation auto", value=True)
seuil_humidite = st.sidebar.slider("Seuil critique d'humidité (%)", 10, 80, 35)

nouveau_theme = st.sidebar.radio("Thème de l'application", ["Clair", "Sombre"], index=0 if st.session_state.theme == "Clair" else 1)
if nouveau_theme != st.session_state.theme:
    st.session_state.theme = nouveau_theme
    st.rerun()

# --- MODULE 1 : TABLEAU DE BORD ---
if menu == "Tableau de bord":
    st.title("Tableau de bord Analytique")
    st.markdown("Vue d'ensemble des indicateurs agronomiques et environnementaux de votre exploitation.")
    
    st.info(f"📍 **Localisation Active :** Village de {village}, Ville de {ville}, Région {region_loc} ({pays}) | **Sol :** {sol_local_choisi}")

    df_cult = pd.read_sql("SELECT * FROM cultures", conn)
    nb_cultures = len(df_cult)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cultures Actives", f"{nb_cultures} parcelles", "+1 ce mois")
    with col2:
        st.metric("Indice de Stress Hydrique", "Optimal", "Humidité > 45%")
    with col3:
        st.metric("Économie d'eau potentielle", "18.5 %", "+3.2%")
    with col4:
        st.metric("Sols Référencés", len(sols_disponibles), "Zone locale")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("État des parcelles enregistrées")
    if not df_cult.empty:
        st.dataframe(df_cult[['nom_culture', 'type_sol', 'date_semis', 'etat', 'ville']], use_container_width=True)
    else:
        st.warning("Aucune culture enregistrée pour le moment. Rendez-vous dans le Planificateur pour ajouter vos parcelles.")

# --- MODULE 2 : PLANIFICATEUR & MOTEUR AGRONOMIQUE ---
elif menu == "Planificateur & Moteur":
    st.title("Moteur d'Aide à la Décision Agronomique")
    st.markdown("Testez une culture pour vérifier si elle est favorable sur votre terre à **" + village + ", " + ville + " (" + pays + ")**.")

    culture_saisie = st.text_input("Entrez le nom d'une culture (ex: Maïs, Sorgho, Manioc, Riz...)")

    if culture_saisie:
        is_valid_format = bool(re.match(r"^[a-zA-ZÀ-ÿ\s]+$", culture_saisie.strip()))
        culture_lower = culture_saisie.strip().lower()

        if not is_valid_format:
            st.error("❌ Erreur : Le nom de la culture ne doit contenir ni chiffres ni symboles.")
        elif culture_lower not in CULTURES_BASE:
            st.warning(f"⚠️ La culture '{culture_saisie}' n'est pas répertoriée dans notre base de données générale, mais elle respecte le format alphabétique.")
        else:
            infos = CULTURES_BASE[culture_lower]
            st.success(f"Analyse agronomique réussie pour : **{infos['nom']}**")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Sol Idéal Recommandé", infos["sol"])
            with c2:
                st.metric("Besoin en Eau (Cycle)", infos["eau"])
            with c3:
                st.metric("Besoin en Azote", infos["azote"])

            st.markdown("---")
            st.subheader("🌍 Évaluation de la favorabilité de votre terre")
            
            sol_cible = sol_local_choisi.lower()
            sol_ref = infos["sol"].lower()
            
            if any(mot in sol_cible for mot in sol_ref.split() if len(mot) > 3):
                st.success(f"✅ **Favorable :** Votre terre à **{village} ({ville})** composée de *{sol_local_choisi}* est **favorable** à la culture du **{infos['nom']}**.")
            else:
                st.info(f"💡 **Moderément favorable / Attention :** Votre terre (*{sol_local_choisi}*) diffère du sol idéal requis (*{infos['sol']}*). Des amendements organiques ou des apports d'engrais adaptés seront nécessaires pour optimiser le rendement du {infos['nom']}.")

    st.markdown("---")
    st.subheader("Enregistrement d'une nouvelle parcelle de culture")
    with st.form("form_planificateur"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nom_culture_form = st.text_input("Nom de la culture à semer")
            type_sol = st.selectbox("Type de sol de la parcelle", sols_disponibles + ["Argileux", "Sableux", "Limoneux", "Humifère"])
        with col_f2:
            date_semis = st.date_input("Date de semis prévisionnelle / effective")
            etat = st.selectbox("État de la culture", ["Semis", "Croissance", "Floraison", "Récolte"])
        
        submit_culture = st.form_submit_button("Valider et Enregistrer la Culture")

        if submit_culture:
            form_lower = nom_culture_form.strip().lower()
            if not nom_culture_form.strip() or not bool(re.match(r"^[a-zA-ZÀ-ÿ\s]+$", nom_culture_form)):
                st.error("❌ Erreur : Le nom de la culture contient des caractères interdits (chiffres/symboles) ou est vide.")
            elif form_lower not in CULTURES_BASE:
                st.error("⚠️ Cette culture n'existe pas dans la base de référence pour l'enregistrement.")
            else:
                cursor.execute(
                    "INSERT INTO cultures (nom_culture, type_sol, date_semis, etat, pays, ville, village) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nom_culture_form, type_sol, str(date_semis), etat, pays, ville, village),
                )
                cursor.execute(
                    "INSERT INTO activites (date_activite, description, type) VALUES (?, ?, ?)",
                    (str(date_semis), f"Semis de {nom_culture_form} à {village}, {ville} ({pays}) - Statut : {etat}", etat),
                )
                conn.commit()
                st.success(f"Parcelle de {nom_culture_form} enregistrée avec succès pour {ville} ({village}) !")

# --- MODULE 3 : CALENDRIER & SUIVI ---
elif menu == "Calendrier & Suivi":
    st.title("Calendrier et Traçabilité des Interventions")
    st.markdown("Historique complet de toutes vos actions agronomiques, semis, alertes et récoltes.")
    st.markdown("---")

    df_activites = pd.read_sql("SELECT * FROM activites ORDER BY date_activite DESC", conn)
    if not df_activites.empty:
        st.dataframe(df_activites, use_container_width=True)
    else:
        st.info("Aucune intervention enregistrée dans l'historique.")

# --- MODULE 4 : DIAGNOSTIC PHYTOSANITAIRE ---
elif menu == "Diagnostic Phytosanitaire 🔬":
    st.title("Assistant de Diagnostic Phytosanitaire")
    st.markdown("Identifiez rapidement les maladies ou carences de vos cultures en sélectionnant les symptômes observés.")
    st.markdown("---")

    culture_concernee = st.selectbox("Culture concernée", ["Maïs", "Riz", "Manioc", "Tomate", "Sorgho", "Igname"])
    symptome_principal = st.selectbox("Symptôme observé", [
        "Feuilles jaunissantes (partiel ou total)",
        "Taches brunes ou noires sur les feuilles",
        "Présence d'insectes ou chenilles dévoreuses",
        "Tubercules pourris ou ramollis",
        "Flétrissement soudain de la plante"
    ])

    if st.button("Lancer le Diagnostic"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Résultat de l'analyse experte")
        
        if "jaunissantes" in symptome_principal:
            st.warning("⚠️ **Suspicion de carence en azote ou attaque de cicadelles.**")
            st.write("- **Recommandation :** Apporter un engrais riche en azote (urée) ou du compost organique bien décomposé. Inspecter le revers des feuilles pour éliminer les nuisibles.")
        elif "Taches brunes" in symptome_principal:
            st.error("🚨 **Suspicion de maladie fongique (Helminthosporiose ou Blast).**")
            st.write("- **Recommandation :** Éviter les excès d'irrigation par aspersion. Traiter de manière préventive avec un fongicide homologué à base de cuivre.")
        elif "insectes" in symptome_principal:
            st.error("🚨 **Attaque de ravageurs détectée (chenilles légionnaires ou foreurs).**")
            st.write("- **Recommandation :** Utiliser des bio-pesticides à base de Neem ou un traitement insecticide sélectif recommandé par la station locale.")
        else:
            st.info("💡 **Alerte hydrique ou pourriture racinaire possible.**")
            st.write("- **Recommandation :** Vérifier le drainage du sol. Réduire les apports d'eau si le sol retient trop l'humidité.")

# --- MODULE 5 : COMMUNAUTÉ ---
elif menu == "Communauté":
    st.title("Réseau d'Échange Agricole")
    st.markdown(f"Partagez vos astuces, posez vos questions aux producteurs de **{ville}** et des régions voisines.")
    st.markdown("---")

    with st.form("form_commu"):
        message = st.text_area("Votre message, observation ou alerte phytosanitaire :")
        btn_publier = st.form_submit_button("Diffuser dans le réseau")
        if btn_publier and message:
            cursor.execute(
                "INSERT INTO communaute (auteur, message, date_post) VALUES (?, ?, ?)",
                (f"{nom_utilisateur} ({village}, {ville}, {pays})", message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
            )
            conn.commit()
            st.success("Message publié avec succès !")

    st.markdown("### Fil d'actualité des producteurs")
    df_commu = pd.read_sql("SELECT auteur, message, date_post FROM communaute ORDER BY id DESC", conn)
    for _, row in df_commu.iterrows():
        st.markdown(f"**{row['auteur']}** — *({row['date_post']})*\n\n> {row['message']}")
        st.markdown("---")

# --- MODULE 6 : PARAMÈTRES ---
elif menu == "Paramètres":
    st.title("Paramètres et Maintenance du Système")
    st.markdown("Gérez vos informations de compte et l'état de la base de données locale.")
    st.markdown("---")

    st.subheader("Résumé de votre profil technique")
    st.write(f"- **Utilisateur :** {nom_utilisateur}")
    st.write(f"- **Localisation :** Village {village}, Ville {ville}, Région {region_loc}, {pays}")
    st.write(f"- **Sol local sélectionné :** {sol_local_choisi}")
    st.write(f"- **Thème actif :** {st.session_state.theme}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Réinitialiser toutes les données de l'application"):
        cursor.execute("DELETE FROM cultures")
        cursor.execute("DELETE FROM activites")
        cursor.execute("DELETE FROM communaute")
        conn.commit()
        st.warning("Toutes les bases de données ont été remises à zéro.")
