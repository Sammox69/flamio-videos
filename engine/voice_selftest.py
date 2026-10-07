# Test autonome de la voix clonée : écrit un JSON de résultat (envoyé ensuite sur Supabase par la routine de test)
import time,json,os,sys,traceback
r={"ok":False}
try:
    t=time.time()
    import torch,soundfile as sf
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m=ChatterboxMultilingualTTS.from_pretrained(device="cpu"); r["load_s"]=round(time.time()-t,1)
    t=time.time(); w=m.generate("Le client scanne votre QR code, sans appli.",language_id="fr",audio_prompt_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"ref_voice.wav"),exaggeration=0.5,cfg_weight=0.4).squeeze().numpy()
    r["gen_s"]=round(time.time()-t,1); r["audio_s"]=round(len(w)/m.sr,2); r["ok"]=True
except Exception as e:
    r["err"]=traceback.format_exc()[-1500:]
print(json.dumps(r))
