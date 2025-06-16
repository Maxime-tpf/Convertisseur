import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment
import io
import tempfile  # Pour créer un fichier temporaire

st.title("Éditeur audio simple")

uploaded_file = st.file_uploader("Uploader un fichier audio", type=["mp3", "wav"])

if uploaded_file:
    # Créer un fichier temporaire et y écrire le contenu de l'upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_filename = tmp_file.name

    # Charger le fichier audio via pydub à partir du fichier temporaire
    try:
        audio = AudioSegment.from_file(temp_filename)
    except Exception as e:
        st.error(f"Erreur lors de la lecture de l'audio avec pydub: {e}")
    else:
        st.audio(uploaded_file)  # Vous pouvez toujours écouter le fichier original

        st.write("### Définir les points de découpe (en secondes)")
        start = st.number_input("Début", min_value=0.0, max_value=audio.duration_seconds, value=0.0)
        end = st.number_input("Fin", min_value=0.0, max_value=audio.duration_seconds, value=audio.duration_seconds)

        if st.button("Rogner l'audio"):
            trimmed_audio = audio[start * 1000 : end * 1000]
            buffer = io.BytesIO()
            trimmed_audio.export(buffer, format="mp3")
            st.success("Audio rogné avec succès")
            st.download_button(
                label="Télécharger", 
                data=buffer.getvalue(), 
                file_name="audio_rogné.mp3", 
                mime="audio/mp3"
            )

        st.write("### Spectrogramme")
        # Charger le fichier audio via librosa à partir du même fichier temporaire
        try:
            y, sr = librosa.load(temp_filename, sr=None)
        except Exception as e:
            st.error(f"Erreur lors de la lecture de l'audio avec librosa: {e}")
        else:
            fig, ax = plt.subplots()
            librosa.display.waveshow(y, sr=sr, ax=ax)
            st.pyplot(fig)
