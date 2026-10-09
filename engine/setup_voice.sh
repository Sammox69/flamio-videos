#!/usr/bin/env bash
# Installe la voix clonée (Chatterbox, CPU). Si ça échoue, build.py retombe sur la voix Piper.
cd "$(dirname "$0")"
PIP="pip install --break-system-packages -q"
ERR=/tmp/voice_pip_err.log; : > $ERR
ok(){ python3 -c "import torch,chatterbox;from chatterbox.mtl_tts import ChatterboxMultilingualTTS;assert torch.__version__.endswith('+cpu')" >/dev/null 2>&1; }
if ok; then echo "voice ok (déjà installé)"; exit 0; fi
python3 --version
# 0) wheels pures Python embarquées dans engine_v2.json (antlr4 ne compile pas sur le serveur de la routine)
if [ -f engine_v2.json ]; then python3 - <<'PY' >>$ERR 2>&1
import json,base64,os
d=json.load(open("engine_v2.json")); os.makedirs("/tmp/whl",exist_ok=True)
for k,v in d.items():
    if k.startswith("whl/"): open("/tmp/whl/"+k[4:-4],"wb").write(base64.b64decode(v))
PY
$PIP --no-deps /tmp/whl/antlr4_python3_runtime-4.9.3-py3-none-any.whl /tmp/whl/omegaconf-2.3.0-py3-none-any.whl >>$ERR 2>&1; $PIP pyyaml >>$ERR 2>&1; fi
# 1) outils de build + dépendance qui compile (antlr4, requise par omegaconf) : avec et sans isolation
$PIP -U setuptools wheel pip >>$ERR 2>&1
$PIP antlr4-python3-runtime==4.9.3 >>$ERR 2>&1 || $PIP --no-build-isolation antlr4-python3-runtime==4.9.3 >>$ERR 2>&1 || { pip download --no-deps --no-binary :all: antlr4-python3-runtime==4.9.3 -d /tmp/antlr >>$ERR 2>&1; $PIP --no-build-isolation /tmp/antlr/*.tar.gz >>$ERR 2>&1; }
# 2) chatterbox, puis torch CPU
$PIP chatterbox-tts==0.1.7 >>$ERR 2>&1 || $PIP --no-build-isolation chatterbox-tts==0.1.7 >>$ERR 2>&1 || $PIP --no-deps chatterbox-tts==0.1.7 >>$ERR 2>&1
$PIP --force-reinstall --no-deps torch==2.11.0+cpu torchaudio==2.11.0+cpu --index-url https://download.pytorch.org/whl/cpu >>$ERR 2>&1
$PIP transformers==5.2.0 >>$ERR 2>&1
# 3) dépendances manquantes éventuelles (si chatterbox installé sans deps)
python3 - <<'PY' >>$ERR 2>&1
import importlib,subprocess,sys
for m,p in [("conformer","conformer"),("diffusers","diffusers"),("librosa","librosa"),("omegaconf","omegaconf"),("pykakasi","pykakasi"),("pyloudnorm","pyloudnorm"),("perth","resemble-perth"),("s3tokenizer","s3tokenizer"),("safetensors","safetensors"),("spacy_pkuseg","spacy-pkuseg")]:
    try: importlib.import_module(m)
    except Exception: subprocess.call([sys.executable,"-m","pip","install","--break-system-packages","-q",p])
PY
if ok; then echo "voice ok"; else
  echo "ERREURS pip (extraits) :"; grep -aiE "error|failed|no matching|not found|could not" $ERR | tail -8 | cut -c1-300
  python3 -c "import torch,chatterbox;from chatterbox.mtl_tts import ChatterboxMultilingualTTS" 2>&1 | tail -3 | cut -c1-300
  echo "voice KO"
fi
