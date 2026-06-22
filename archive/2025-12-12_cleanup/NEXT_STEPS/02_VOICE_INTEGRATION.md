# Voice System Integration Research

## Current State
The existing system has TTS implementations in `docs/amalgam/observability/utils/tts/`:
- `elevenlabs_tts.py` - ElevenLabs Turbo v2.5
- `openai_tts.py` - OpenAI TTS model
- `pyttsx3_tts.py` - Offline pyttsx3

Whisper mentioned in SwarmForge docs for voice input.

---

## Target State

### Text-to-Speech: Microsoft VibeVoice

**Overview:**
- Multi-speaker, long-form conversational TTS
- Synthesizes up to 90 minutes with up to 4 speakers
- Uses LLM-powered next-token diffusion framework

**Variants:**
| Model | Speakers | Latency | Use Case |
|:------|:---------|:--------|:---------|
| VibeVoice Full | 4 | Higher | Multi-speaker, long-form |
| VibeVoice-Realtime-0.5B | 1 | ~300ms | Streaming, real-time |

**Integration Options:**

1. **Replicate API** (Recommended for ease)
   ```python
   import replicate
   
   output = replicate.run(
       "microsoft/vibe-voice:latest",
       input={
           "text": "Hello from Super Agent Monitor",
           "speakers": 1
       }
   )
   ```

2. **Fal.ai API**
   ```python
   import fal_client
   
   result = fal_client.subscribe(
       "fal-ai/vibe-voice",
       arguments={"text": "Agent status update"}
   )
   ```

3. **Local (via HuggingFace)**
   - Model: `microsoft/VibeVoice-Realtime-0.5B`
   - Requires: GPU with CUDA
   - Note: Main repo temporarily disabled for responsible AI concerns

**Current Status:**
- Official GitHub repo temporarily disabled
- Available via: Replicate, Fal.ai, AI/ML API
- Has audible disclaimer + watermark for safety

**Security Notes:**
- Designed for research, not production without testing
- Includes deepfake mitigation watermarks

---

### Speech-to-Text: NVIDIA Parakeet v3

**Overview:**
- Model: `parakeet-tdt-0.6b-v3`
- Multilingual: 25 European languages
- Based on TDT (Token-and-Duration Transducer) architecture

**Integration Options:**

1. **NVIDIA NeMo Framework** (Recommended for local)
   ```python
   import nemo.collections.asr as nemo_asr
   
   # Load model
   asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(
       model_name="nvidia/parakeet-tdt-0.6b-v3"
   )
   
   # Transcribe
   transcription = asr_model.transcribe(["audio.wav"])
   ```

2. **NVIDIA Riva** (Production API)
   - Enterprise-grade ASR service
   - Streaming support
   - Multi-model pipelines

3. **HuggingFace Transformers**
   ```python
   from transformers import pipeline
   
   pipe = pipeline("automatic-speech-recognition", 
                   model="nvidia/parakeet-tdt-0.6b-v3")
   result = pipe("audio.wav")
   ```

**Requirements:**
- Python 3.8+
- PyTorch with CUDA
- nemo_toolkit[asr]

**Performance:**
- 0.6B parameters
- Real-time factor: <0.1 on modern GPU
- WER competitive with Whisper large-v3

---

## Migration Plan

### Phase 1: STT Upgrade (Whisper → Parakeet)
1. Create `utils/stt/parakeet_stt.py`
2. Implement common interface matching existing TTS pattern
3. Test with sample audio files
4. Update observability hooks to use new STT

### Phase 2: TTS Upgrade (Current → VibeVoice)
1. Create `utils/tts/vibevoice_tts.py`
2. Implement Replicate API wrapper (start simple)
3. Add streaming support for real-time variant
4. Update hooks to use VibeVoice

### Phase 3: Integration
1. Update `session_start.py` with new voice components
2. Add configuration for voice provider selection
3. Document API key requirements

---

## Dependencies

### VibeVoice (Replicate)
```bash
pip install replicate
export REPLICATE_API_TOKEN="your_token"
```

### Parakeet (NeMo)
```bash
pip install nemo_toolkit[asr]
pip install torch torchaudio
```

---

## Cost Estimates

| Service | Pricing |
|:--------|:--------|
| Replicate VibeVoice | ~$0.05/minute generated |
| Fal.ai VibeVoice | $0.03-0.05/minute |
| NVIDIA Parakeet | Free (local compute) |
| NVIDIA Riva | Enterprise pricing |

---

## Recommended Approach

1. **STT**: NVIDIA Parakeet via NeMo (local, free, high quality)
2. **TTS**: VibeVoice via Replicate API (simple integration, good quality)
3. **Fallback TTS**: pyttsx3 (offline, zero cost)
