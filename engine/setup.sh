#!/usr/bin/env bash
# Installe le moteur de vidéo Flamio dans un environnement vide (cloud). ~2 min.
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q sherpa-onnx soundfile scipy numpy playwright 2>&1 | tail -1 || true
if [ ! -d models/vits-piper-fr_FR-tom-medium ]; then
  mkdir -p models && cd models
  curl -sSL -o tom.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-tom-medium.tar.bz2
  tar xjf tom.tar.bz2 && rm tom.tar.bz2
fi
echo "setup ok"
