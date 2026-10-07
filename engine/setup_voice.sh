#!/usr/bin/env bash
# Installe la voix clonée (Chatterbox, CPU). Si ça échoue, build.py retombe sur la voix Piper.
cd "$(dirname "$0")"
python3 -c "import chatterbox,torch;assert torch.__version__.endswith('+cpu')" 2>/dev/null && { echo "voice ok (déjà installé)"; exit 0; }
pip install --break-system-packages -q chatterbox-tts==0.1.7 2>&1 | tail -2
pip install --break-system-packages -q --force-reinstall --no-deps torch==2.11.0+cpu torchaudio==2.11.0+cpu --index-url https://download.pytorch.org/whl/cpu 2>&1 | tail -2
pip install --break-system-packages -q transformers==5.2.0 2>&1 | tail -1
python3 -c "import torch,chatterbox;from chatterbox.mtl_tts import ChatterboxMultilingualTTS;print('voice ok',torch.__version__)"
