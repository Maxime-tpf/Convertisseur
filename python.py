if uploaded_file:
    # Sauvegarde sur disque temporaire
    temp_filename = "temp_audio_file"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Charge via pydub
    audio = AudioSegment.from_file(temp_filename)
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
    
    # Réinitialiser le pointer pour la lecture avec librosa
    # SOIT, en rechargeant depuis le fichier temporaire :
    y, sr = librosa.load(temp_filename)
    # OU, si vous souhaitez absolument utiliser uploaded_file, faites :
    # uploaded_file.seek(0)
    # y, sr = librosa.load(uploaded_file)
    
    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=sr, ax=ax)
    st.pyplot(fig)
