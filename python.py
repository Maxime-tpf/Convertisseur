import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment
import io

st.title("Éditeur audio simple")

uploaded_file = st.file_uploader("Uploader un fichier audio", type=["mp3", "wav"])

if uploaded_file:
    audio = AudioSegment.from_file(uploaded_file)
    st.audio(uploaded_file)

    st.write("### Définir les points de découpe (en secondes)")
    start = st.number_input("Début", min_value=0.0, max_value=audio.duration_seconds, value=0.0)
    end = st.number_input("Fin", min_value=0.0, max_value=audio.duration_seconds, value=audio.duration_seconds)

    if st.button("Rogner l'audio"):
        trimmed_audio = audio[start*1000:end*1000]
        buffer = io.BytesIO()
        trimmed_audio.export(buffer, format="mp3")
        st.success("Audio rogné avec succès")
        st.download_button(label="Télécharger", data=buffer.getvalue(), file_name="audio_rogné.mp3", mime="audio/mp3")

    st.write("### Spectrogramme")
    y, sr = librosa.load(uploaded_file)
    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=sr, ax=ax)
    st.pyplot(fig)
