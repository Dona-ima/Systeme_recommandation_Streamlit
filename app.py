import streamlit as st
import csv
import hashlib

st.sidebar.title("Youtube 2.0")
st.sidebar.markdown("Cette application vous propose du contenu vidéos en fonction de vos "
                    " préférences et de vos historisques de lectures et de like. Passez un "
                    " bon moment 👌🙌")
st.sidebar.subheader("AGBOTON Ariane,"
                     " AHOUANDJINOU Carmelle,"
                     " GBODO Emmanuella")

# Initialiser l'état de la page si non défini
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Définir les différentes pages
def show_home():
    st.title("Bienvenue sur Youtube2.0")
    st.write("Veuiller choisir une option: ")
    if st.button("S'inscrire"):
        st.session_state.page = 'signup'
    if st.button("Se connecter"):
        st.session_state.page = 'login'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def show_signup():
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
                st.success('Inscription réussie. Vous pouvez maintenant vous connecter.')
                st.session_state.page = 'login'
    
    if st.button("J'ai déjà un compte", key="retour_connexion"):
        st.session_state.page = 'login'

def show_login():
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
                        st.session_state.page = 'dashboard'  # Rediriger vers une autre page après connexion réussie
                        break
            if not authenticated:
                st.error('Nom d\'utilisateur ou mot de passe incorrect')
        except FileNotFoundError:
            st.error('Aucun utilisateur trouvé. Veuillez vous inscrire d\'abord.')
    
    if st.button("Retour à l'accueil"):
        st.session_state.page = 'home'

# Initialisation de l'état de la page
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Afficher la page selon l'état actuel
if st.session_state.page == 'home':
    show_home()  # Assurez-vous que cette fonction existe
elif st.session_state.page == 'signup':
    show_signup()
elif st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'dashboard':  # Exemple de redirection après connexion réussie
    st.title('Contenu de l\'application')