import streamlit as st
from speak import speak_answer

st.title("Audio RAG")
st.write("Ask a question about the audio clip and get a spoken answer back.")

query = st.text_input("Your !uestion")

if st.button("Ask") and query:
    with st.spinner("Retrieving context and generating answer..."):
        answer, audio_path = speak_answer(query)

    st.subheader("Answer")
    st.write(answer)
    st.audio(audio_path)