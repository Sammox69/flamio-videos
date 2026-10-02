# flamio-videos

Vidéos courtes de promotion de Flamio (TikTok, Instagram Reels, YouTube Shorts) et moteur qui les fabrique.

- `videos/` : vidéos finales (9:16, 1080x1920). Metricool les récupère par adresse publique avant publication.
- `engine/` : moteur de rendu (scènes HTML animées capturées image par image, voix off locale, musique et bruitages synthétiques, montage ffmpeg).
  - `setup.sh` : installe les dépendances et la voix dans un environnement vide.
  - `build.py <spec.json> <sortie.mp4>` : fabrique une vidéo à partir d'un script de scènes.
  - `spec_example.json` : exemple de script.

Marges de sécurité : rien d'important dans les 220 px du haut, les 450 px du bas et les 160 px de droite.
