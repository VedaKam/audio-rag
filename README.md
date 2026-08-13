# Audio RAG with Voice Synthesis Pipeline

A retrieval-augmented generation pipeline that answers questions about spoken audio content and speaks the answer back.

Given an audio clip (e.g. a lecture or podcast segment), this app transcribes it, embeds and indexes the transcript, retrieves relevant context for a user's question, generates a grounded answer with an LLM, and converts that answer to natural-sounding speech.

Most chunk embedding models embed each chunk independently, losing document-level context. `voyage-context-3` embeds all chunks of a document together, so each chunk's embedding retains awareness of the full transcript, thereby improving retrieval quality for content where meaning depends on surrounding context (similar to spoken dialogue).


## Pipeline

```
Audio file
   │
   ▼
1. Transcription (Speechmatics)
   │   speaker-attributed transcript
   ▼
2. Embedding + Storage (Voyage voyage-context-3 → MongoDB Atlas Vector Search)
   │   contextualized chunk embeddings, indexed for vector search
   ▼
3. Retrieval (MongoDB $vectorSearch)
   │   top-k relevant transcript chunks for a query
   ▼
4. Generation (DeepSeek V3.2 via OpenRouter)
   │   text answer grounded in retrieved context
   ▼
5. Speech synthesis (Fish Audio TTS)
   │   spoken answer as audio
   ▼
Streamlit UI — question in, spoken + text answer out
```

## Stack

- **Transcription:** Speechmatics (batch API, speaker diarization)
- **Embeddings:** Voyage AI `voyage-context-3`
- **Vector store:** MongoDB Atlas Vector Search (free M0 tier)
- **Orchestration:** Python (LlamaIndex-compatible retrieval pattern)
- **LLM:** DeepSeek V3.2 via OpenRouter
- **Text-to-speech:** Fish Audio API (`s2.1-pro-free`)
- **UI:** Streamlit

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add API keys to `.env`:
   ```
   SPEECHMATICS_API_KEY=
   VOYAGE_API_KEY=
   MONGODB_URI=
   OPENROUTER_API_KEY=
   FISHAUDIO_API_KEY=
   ```

3. Create a MongoDB Atlas Vector Search index named `autoembed_index` on the `transcript_chunks` collection (`embedding` field, cosine similarity, "Bring your own embeddings" — see `index_config.json`).

4. Place an audio file as `input_audio.mp3` and run:
   ```bash
   python transcribe.py      # step 1: transcription
   python embed_store.py     # step 2: embedding + storage
   streamlit run app.py      # steps 3-5: retrieval, generation, speech synthesis + UI
   ```

   Individual pipeline stages can also be run standalone for testing:
   ```bash
   python retrieve.py   # step 3: retrieval only
   python generate.py   # steps 3-4: retrieval + generation
   python speak.py       # steps 3-5: full pipeline, no UI
   ```

## Notes

- Built as an extension of a Daily Dose of DS tutorial on audio RAG, with an added text-to-speech step using Fish Audio's API to close the loop from audio question to spoken answer.
- Free-tier friendly: MongoDB M0, Fish Audio's free `s2.1-pro-free` model, and Voyage's free embedding tier keep this runnable at no cost for demo purposes.