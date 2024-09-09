import hashlib
import streamlit as st
import csv
import pandas as pd
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import os

def info_app():
    st.sidebar.title("Youtube 2.0")
    st.sidebar.markdown("Cette application vous propose du contenu vidéos en fonction de vos "
                        "préférences et de vos historiques de lectures et de likes. Passez un "
                        "bon moment 👌🙌")
    st.sidebar.subheader("AGBOTON Ariane,"
                        " AHOUANDJINOU Carmelle,"
                        " GBODO Emmanuella")

# Initialiser l'état de la page si non défini
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Définir les différentes pages
def show_home():
    info_app()
    st.title("Bienvenue sur Youtube2.0")
    st.write("Veuillez choisir une option : ")
    if st.button("S'inscrire", key="option_signup"):
        st.session_state.page = 'signup'
    if st.button("Se connecter", key="option_login"):
        st.session_state.page = 'login'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def show_signup():
    info_app()
    if st.button("Retour à l'accueil", key="retour_accueil"):
        st.session_state.page = 'home'
    
    st.title("Inscription")

    user_file = 'appuser.csv'
    name = st.text_input('Nom')
    pseudo = st.text_input('Nom d\'utilisateur')
    password = st.text_input('Mot de passe', type='password')

    if st.button('S\'inscrire', key="validation_inscription"):
        if not name or not pseudo or not password:
            st.error("Veuillez remplir tous les champs.")
        else:
            user_exists = False
            try:
                with open(user_file, mode='r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['username'] == pseudo:
                            user_exists = True
                            break
            except FileNotFoundError:
                pass

            if user_exists:
                st.warning('Ce nom d\'utilisateur est déjà pris.')
            else:
                hashed_password = hash_password(password)
                with open(user_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:
                        writer.writerow(['username', 'name', 'hashed_password'])
                    writer.writerow([pseudo, name, hashed_password])
                st.success('Inscription réussie. Vous pouvez maintenant configurer vos préférences.')
                st.session_state.page = 'login'

    if st.button("J'ai déjà un compte", key="retour_connexion"):
        st.session_state.page = 'login'

def show_login():
    info_app()
    st.title('Connexion')  

    pseudo = st.text_input('Nom d\'utilisateur')
    password = st.text_input('Mot de passe', type='password')

    if st.button('Se connecter', key="validation_connexion"):
        authenticated = False
        try:
            with open('appuser.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == pseudo and check_password(row['hashed_password'], password):
                        authenticated = True
                        st.success(f'Bienvenue {row["name"]}')
                        preferences_file = 'preferences.csv'
                        preferences_exists = False
                        if os.path.exists(preferences_file):
                            with open(preferences_file, mode='r', newline='') as file:
                                reader = csv.DictReader(file)
                                for pref_row in reader:
                                    if pref_row['username'] == pseudo:
                                        preferences_exists = True
                                        break
                        
                        # Afficher la page des préférences seulement si elles ne sont pas encore enregistrées
                        if not preferences_exists:
                            st.session_state.username = pseudo
                            st.session_state.page = 'preferences'
                        else:
                            
                            st.session_state.username = pseudo
                            st.session_state.page = 'accueil'
                        
                        break
                    
            if not authenticated:
                st.error('Nom d\'utilisateur ou mot de passe incorrect')
        except FileNotFoundError:
            st.error('Aucun utilisateur trouvé. Veuillez vous inscrire d\'abord.')
    
    if st.button("Retour à l'accueil"):
        st.session_state.page = 'home'




#chargement des fichiers et de l'API
API_KEY = 'AIzaSyB7zqyRPYYtQVlABHqjF7V17a6P8uMAKKA'
youtube = build('youtube', 'v3', developerKey=API_KEY)
fichier_interaction = 'user_interactions.csv'
fichier_preference = 'preferences.csv'

# si le fichier interaction n'existe pas il faut le créer
if not os.path.exists(fichier_interaction):
    with open(fichier_interaction, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'video_id', 'info_video'])

def get_username():
    if 'username' not in st.session_state:
        st.session_state.username = None
    return st.session_state.username

#récupération du username
def pseudonyme():
    username = get_username()
    if username is None:
        st.error("Vous devez être connecté pour accéder à cette fonctionnalité.")
        show_login()
    return username

#Menu dans le sidebar
def menu():
    st.sidebar.title(pseudonyme())  
    st.sidebar.write("Bienvenue dans le menu personnalisé")
    if st.sidebar.button("Se déconnecter", key="deconnexion"):
        st.session_state.username = None
        st.session_state.page = 'login'
        st.success("Vous avez été déconnecté.")

def chargement_preferences(username):
    user_preferences = []
    try:
        with open(fichier_preference, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    user_preferences = [pref for pref, selected in row.items() if selected.lower() == 'true']
                    break
    except FileNotFoundError:
        st.error('Fichier des préférences non trouvé.')
    return user_preferences

#Fonction pour le chargement des interractions de l'utilisateur pour le similary cosine
def chargement_interactions(username):
    interactions = []
    try:
        with open(fichier_interaction, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    interactions.append(row)
    except FileNotFoundError:
        st.error('Fichier des interactions non trouvé.')
    return interactions

#Fonction pour l'enregistrement des interactions dans user_interactions.csv

def save_interaction(username, video_id, video_data):
    interactions = []
    
    # Charger les interactions existantes
    try:
        with open(fichier_interaction, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                interactions.append(row)
    except FileNotFoundError:
        pass
    
    # Filtrer les interactions de l'utilisateur
    user_interactions = [row for row in interactions if row['username'] == username]
    
    # Limiter à 10 vidéos par utilisateur
    if len(user_interactions) >= 10:
        # Supprimer la vidéo la plus ancienne
        user_interactions.pop(0)

    # Ajouter la nouvelle interaction
    new_interaction = {
        'username': username,
        'video_id': video_id,
        'info_video': video_data
    }
    print(new_interaction)
    user_interactions.append(new_interaction)
    
    # Réécrire toutes les interactions dans le fichier CSV
    with open(fichier_interaction, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['username', 'video_id', 'info_video']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Réécrire les interactions restantes et celles des autres utilisateurs
        for row in interactions:
            if row['username'] != username:
                writer.writerow(row)
        
        # Réécrire les interactions mises à jour de l'utilisateur
        for interaction in user_interactions:
            writer.writerow(interaction)

# Fonction pour aller chercher les vidéos sur youtube
def search_youtube_videos(query, max_results=10):
    videos = []
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            video_data = {
                'title': item['snippet']['title'],
                'video_id': video_id,
                'tags': ", ".join(item['snippet'].get('tags', [])),
                'description': item['snippet']['description'],
                'full_text': item['snippet']['title'] + " " + ", ".join(item['snippet'].get('tags', [])) + " " + item['snippet']['description'],
            }
            videos.append(video_data)
        random.shuffle(videos)
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return []
    return videos



def accueil():
    menu()
    user_interactions = chargement_interactions(pseudonyme()) 
    if not user_interactions:
        user_preferences = chargement_preferences(pseudonyme())
        some_user_preferences = random.sample(user_preferences, 3)
        if some_user_preferences:
            videos_trouves = search_youtube_videos(" ".join(some_user_preferences))
            if videos_trouves:
                videos_df = pd.DataFrame(videos_trouves)
                st.markdown(f"""
                    <h4 style='color: fc9880;'>Suggestion de vidéos</h4>
                    """, unsafe_allow_html=True)
                for index, row in videos_df.iterrows():
                    st.markdown(f"""
                    <h3 style='color: #1E90FF; margin-top: 10px;'>{row['title']}</h3>
                    """, unsafe_allow_html=True)
                    video_url = f'https://www.youtube.com/embed/{row["video_id"]}'
                    st.markdown(f"""
                    <iframe width="560" height="315" border-radius="10" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    """, unsafe_allow_html=True)
                    st.write(f"Description: {row['description']}")
                    st.write(f"Tags: {row['tags']}")
                    col1, col2 = st.columns([1, 2])
                    like= False
                    with col1:
                        like_key = f"like_button_{row['video_id']}"
                        
                        if st.button("Liker 👍 ", key=like_key):
                            save_interaction(pseudonyme(), row['video_id'], row['full_text'])
                            like = True
                            

                    # Champ de texte pour les commentaires
                    with col2:
                        comment_key = f"comment_input_{row['video_id']}"
                        comment = st.text_input(f"Commentaire pour {row['title']}", key=comment_key)
                        
                        send_comment_key = f"send_comment_button_{row['video_id']}"
                        if st.button(f"Envoyer commentaire 💬 ", key=send_comment_key):
                            if comment:
                                if not like:
                                    save_interaction(pseudonyme(), row['video_id'], row['full_text'])
                            else:
                                st.warning("Le champ commentaire est vide.")
            else:
                st.write("Aucune vidéo trouvée pour les préférences sélectionnées.")


    else:
        # Charger les vidéos précédemment likées/commentées
        previous_videos = []
        for interaction in user_interactions:
            video_data = {
                'video_id': interaction['video_id'],
                'full_text': interaction['info_video']
            }
            previous_videos.append(video_data)
        
        if previous_videos:
            
            some_user_preferences = [video['full_text'] for video in previous_videos]
            while True:
                search_query = " ".join(some_user_preferences)
                videos_trouves = search_youtube_videos(search_query, max_results=4)
            
                if videos_trouves:
                    for i in previous_videos:
                        for j in videos_trouves:
                            if i['full_text'] == j['full_text']:
                                videos_trouves.remove(j)
                    # Calculer la similarité entre les vidéos trouvées et les vidéos précédemment regardées
                    videos_df = pd.DataFrame(videos_trouves)
                    previous_texts = [video['full_text'] for video in previous_videos]
                    tfidf_vectorizer = TfidfVectorizer()
                    tfidf_model = tfidf_vectorizer.fit_transform(previous_texts + videos_df['full_text'].tolist())
                    
                    similarity_scores = cosine_similarity(tfidf_model[:len(previous_texts)], tfidf_model[len(previous_texts):])
                    scores = similarity_scores.mean(axis=0)
                    
                    # Ajouter les scores de similarité aux vidéos trouvées
                    videos_df['similarity_score'] = scores
                    low_score_count = (videos_df['similarity_score'] < 0.30).sum()
                    total_videos = len(videos_df)
                    if low_score_count / total_videos < 0.50:
                        break
                    some_user_preferences.append("plus d'options")
                    
            videos_df = videos_df.sort_values(by='similarity_score', ascending=False)
            print(videos_df['similarity_score'])
            user_preferences = chargement_preferences(pseudonyme())
            some_user_preferences = random.sample(user_preferences, 3)
            if some_user_preferences:
                videos_trouves = search_youtube_videos(" ".join(some_user_preferences))
                if videos_trouves:
                    videos_df2 = pd.DataFrame(videos_trouves)
            videos_total= pd.concat([videos_df.drop("similarity_score"), videos_df2], axis=1)
                
            st.markdown(f"""
                <h4 style='color: fc9880;'>Suggestion de vidéos basées sur vos interactions passées</h4>
                """, unsafe_allow_html=True)
                    
            for index, row in videos_total.iterrows():
                st.markdown(f"""
                <h3 style='color: #1E90FF; margin-top: 10px;'>{row['title']}</h3>
                """, unsafe_allow_html=True)
                video_url = f'https://www.youtube.com/embed/{row["video_id"]}'
                st.markdown(f"""
                <iframe width="560" height="315" border-radius="10" src="{video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                """, unsafe_allow_html=True)
                st.write(f"Description: {row['description']}")
                st.write(f"Tags: {row['tags']}")
                col1, col2 = st.columns([1, 2])
                like = False
                with col1:
                    like_key = f"like_button_{row['video_id']}"
                    if st.button("Liker 👍 ", key=like_key):
                        save_interaction(pseudonyme(), row['video_id'], row['full_text'])
                        like = True

                # Champ de texte pour les commentaires
                with col2:
                    comment_key = f"comment_input_{row['video_id']}"
                    comment = st.text_input(f"Commentaire pour {row['title']}", key=comment_key) 
                    send_comment_key = f"send_comment_button_{row['video_id']}"
                    if st.button(f"Envoyer commentaire 💬 ", key=send_comment_key):
                        if comment:
                            if not like:
                                save_interaction(pseudonyme(), row['video_id'], row['full_text'])
                        else:
                            st.warning("Le champ commentaire est vide.")
                
            else:
                st.write("Aucune vidéo trouvée pour les préférences basées sur vos interactions passées.")
 
   






# Afficher la page selon l'état actuel
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'signup':
    show_signup()
elif st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'preferences':
    import preferences
    preferences.show_preferences_page()
elif st.session_state.page == 'accueil':
    accueil()


    
