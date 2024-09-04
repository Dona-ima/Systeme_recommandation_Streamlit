"""import streamlit as st
import csv
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

user_file = 'appusers.csv'

st.title('Inscription')

query_params = st.query_params
if 'page' not in query_params:
    st.query_params['page'] = 'inscription'
current_page = query_params.get('page', 'inscription')[0]   
name = st.text_input('Nom')
pseudo = st.text_input('Nom d\'utilisateur')
password = st.text_input('Mot de passe', type='password')

if st.button('S\'inscrire', key= "validation_inscription"):
    user_exists = False
    #vérification de l'existance de l'individu
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
        #conversion en format chiffré du password
        hashed_password = hash_password(password)
        with open(user_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                #ajout de l'individu dans le fichier csv
                writer.writerow(['username', 'name', 'hashed_password'])
            writer.writerow([pseudo, name, hashed_password])
        st.success('Inscription réussie. Vous pouvez maintenant vous connecter.')

if st.button('Passez à la connexion', key= "connexion_apres_inscription"):
    current_page = "connexion"
if current_page == "connexion":
    import connexion
"""
import streamlit as st

# Initialiser les variables de session pour stocker les valeurs du formulaire
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""
if "confirm_password" not in st.session_state:
    st.session_state["confirm_password"] = ""
if "registration_submitted" not in st.session_state:
    st.session_state["registration_submitted"] = False

# Simulation de la validation de l'inscription
def validate_registration():
    # Logique de validation
    st.success("Inscription réussie!")
    # Marquer le formulaire comme soumis
    st.session_state["registration_submitted"] = True
    # Rediriger vers la page de connexion
    st.experimental_set_query_params(page='connexion')

# Page d'inscription
def show_registration_page():
    st.title("Inscription")
    st.write("Veuillez remplir le formulaire d'inscription.")
    
    # Formulaire d'inscription avec valeurs persistantes
    st.session_state["username"] = st.text_input("Nom d'utilisateur", value=st.session_state["username"])
    st.session_state["password"] = st.text_input("Mot de passe", type="password", value=st.session_state["password"])
    st.session_state["confirm_password"] = st.text_input("Confirmez le mot de passe", type="password", value=st.session_state["confirm_password"])

    if st.button("S'inscrire"):
        if st.session_state["password"] == st.session_state["confirm_password"]:
            validate_registration()
        else:
            st.error("Les mots de passe ne correspondent pas.")

# Page de connexion
def show_login_page():
    st.title("Connexion")
    st.write("Veuillez vous connecter.")
    
    # Exemple de formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        st.success("Connexion réussie!")

# Gestion des pages en fonction des paramètres de requête
query_params = st.query_params
if 'page' not in query_params:
    st.query_params['page'] = 'inscription'
current_page = query_params.get('page', 'inscription')[0]   


if current_page == "connexion":
    show_login_page()
elif current_page == "inscription":
    show_registration_page()
