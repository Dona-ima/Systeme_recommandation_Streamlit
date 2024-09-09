import streamlit as st
import csv
import os


if 'page' not in st.session_state:
    st.session_state.page = 'select_preferences'

# Fonction pour enregistrer les préférences
def save_preferences(preferences):
    if 'username' not in st.session_state:
        st.error("Vous devez être connecté pour accéder à cette page.")
        st.session_state.page = 'login'
        return
    
    username = st.session_state.username
    preferences_file = 'preferences.csv'
    preferences_list = []

    # Lire les préférences existantes si le fichier existe
    if os.path.exists(preferences_file):
        try:
            with open(preferences_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                preferences_list = list(reader)
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier des préférences : {e}")
            return

        # Mettre à jour les préférences de l'utilisateur
        user_exists = False
        for row in preferences_list:
            if row['username'] == username:
                row.update(preferences)
                user_exists = True
                break

        if not user_exists:
            preferences_list.append({'username': username, **preferences})

    else:
        # Ajouter les préférences si le fichier n'existe pas encore
        preferences_list.append({'username': username, **preferences})

    # Sauvegarder les préférences dans le fichier CSV
    try:
        with open(preferences_file, mode='w', newline='') as file:
            fieldnames = ['username'] + list(preferences.keys())
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(preferences_list)
        st.success("Vos préférences ont été enregistrées avec succès!")
        st.session_state.page = 'accueil'
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement des préférences : {e}")

# Fonction pour afficher la page des préférences
def show_preferences_page():
    st.title("Sélectionnez vos préférences")
    if 'preferences' not in st.session_state:
        st.session_state['preferences'] = {option: False for option in ["Musique", "Technologie", "Sport", "Éducation", "Actualités", "Science", "Cuisine", "Voyage", "Mode", "Beauté", "Santé", "Films", "Séries", "Jeux Vidéo", "Documentaire", "Animation", "Comédie", "Politique", "Fitness", "Économie", "Développement Personnel", "Entrepreneuriat"]}
    
    # Afficher le formulaire de préférences
    for preference in st.session_state['preferences'].keys():
        st.session_state['preferences'][preference] = st.checkbox(preference, value=st.session_state['preferences'][preference])

    if st.button("Enregistrer mes préférences"):
        selected_preferences = sum(st.session_state['preferences'].values())
        if selected_preferences >= 5:  # Vérifier si au moins 5 préférences sont sélectionnées
            save_preferences(st.session_state['preferences'])
        else:
            st.warning("Veuillez sélectionner au moins 5 préférences.")


if st.session_state.page == 'select_preferences':
    show_preferences_page()
elif st.session_state.page == 'login':
    import app
    app.show_login()