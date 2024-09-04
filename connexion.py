import streamlit as st
import csv
import hashlib

def check_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

st.title('Connexion')
query_params = st.query_params
if 'page' not in query_params:
    st.query_params['page'] = 'connexion'
current_page = query_params.get('page', 'connexion')[0]  
username = st.text_input('Nom d\'utilisateur')
password = st.text_input('Mot de passe', type='password')

if st.button('Se connecter', key= "validation_connexion"):
    authenticated = False
    try:
        with open('users.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and check_password(row['hashed_password'], password):
                    authenticated = True
                    st.success(f'Bienvenue {row["name"]}')
                    st.title('Contenu de l\'application')
                    break
        if not authenticated:
            st.error('Nom d\'utilisateur ou mot de passe incorrect')
    except FileNotFoundError:
        st.error('Aucun utilisateur trouvé. Veuillez vous inscrire d\'abord.')

if st.button('Aller à la page d\'inscription'):
    current_page == "inscription"
if current_page== "inscription":
    import inscription