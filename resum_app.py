# libraries
import streamlit as st
from PyPDF2 import PdfReader
import json
# resum model
import resum_model

# Chargement et lecture des fichiers
def load_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.type == "application/json":
        data = json.load(uploaded_file)
        return json.dumps(data, indent=4)
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return None

# Fonction pour télécharger le résumé et exporter en base de données

# Fonctionnalité application
def main():
    st.title("Application de Résumé de Texte NLP")

    st.sidebar.title("Options")
    uploaded_file = st.sidebar.file_uploader("Choisissez un fichier", type=["json", "txt", "pdf"])

    text_input = st.sidebar.text_area("Ou écrivez le texte ici")

    if uploaded_file:
        text = load_text_from_file(uploaded_file)
    elif text_input:
        text = text_input
    else:
        text = "Aucun texte n'a été entré ou téléchargé."

    st.write("### Texte d'entrée")
    st.write(
        f'<div style="border:2px solid #4CAF50; padding: 10px; border-radius: 10px; background-color:#f9f9f9; height:300px; overflow:auto;">'
        f'{text}</div>',
        unsafe_allow_html=True)

    summary = "Aucun résumé disponible."
    if text != "Aucun texte n'a été entré ou téléchargé." and st.sidebar.button("Résumer le texte"):
        summary = resum_model.summarize_test(text)

    st.write("### Résumé")
    st.write(
        f'<div style="border:2px solid #2196F3; padding: 10px; border-radius: 10px; background-color:#f0f0f0;height:300px; overflow:auto;">'
        f'{summary}</div>',
        unsafe_allow_html=True)

if __name__ == "__main__":
    main()
