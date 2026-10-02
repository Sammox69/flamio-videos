# Routine quotidienne Flamio : créer et programmer 1 vidéo par jour

But : 1 vidéo verticale 9:16 de 15 à 25 secondes par jour, publiée sur TikTok, Instagram (Reel) et YouTube (Short) du compte flamioapp via Metricool (blogId 7201770, fuseau Europe/Paris). Public : gérants de snacks et de fast-foods en France. Ton : direct, concret, sans hype, tutoiement interdit (vouvoiement).

## Règles de fond (à ne jamais enfreindre)
- Aucun chiffre de résultat inventé (« +30 % de clients » interdit). Les chiffres d'illustration sont autorisés seulement s'ils sont présentés comme exemple (« Exemple », « Par exemple »).
- Faits autorisés sur Flamio : programme de fidélité par scan de QR code (sans appli à télécharger), points et cadeaux, défis de fréquence, SMS automatiques (clients inactifs, anniversaires), tableau de bord (clients fidèles, passages, avis Google, SMS), demande d'avis Google, parrainage, visibilité sur TikTok. Offre : essai gratuit 1 mois, sans engagement. Prix cités uniquement dans une vidéo « offre » : 149 € par mois et par restaurant, ou 1 490 € par an (2 mois offerts).
- Ne pas critiquer de concurrent nommé. Pas de promesse médicale/juridique.
- Une vidéo ne répète pas un sujet déjà présent dans `content_log.json` (cf. `topics.md`).

## Structure d'une vidéo (fichier spec JSON, cf. `spec_example.json` et `spec_demo.json`)
Toujours : 1 scène `hook` en premier (la phrase d'accroche donne le résultat ou la question, pas de « bonjour »), 1 à 3 scènes de contenu, 1 scène `cta` en dernier. Durée totale visée 15 à 25 s : environ 45 à 65 mots parlés au total.
Types de scènes : `hook`, `phone_loyalty`, `phone_sms`, `phone_review`, `phone_dash`, `tips`, `cta`. Les champs de chaque type sont ceux des fichiers d'exemple. Dans les titres, `*mot*` met le mot en orange et `\n` fait un saut de ligne.
Chaque scène a : `say` (texte dit à voix haute, écrire « S M S », « Q R code », « flamio app point f r » pour la prononciation), `cap` (sous-titres affichés, écriture normale), `hl` (mots en couleur dans les sous-titres, en minuscules).
Varier les types d'une vidéo à l'autre ; alterner conseils et démos de l'app.

## Marges de sécurité (déjà gérées par le moteur, ne pas les contourner)
Rien d'important dans les 220 px du haut, 450 px du bas, 160 px de droite. Sous-titres entre y=1285 et 1465.

## Étapes
1. Cloner le dépôt `Sammox69/flamio-videos` (outil add_repo en accès push, puis `git clone`). Lire `content_log.json` et `topics.md`, choisir le prochain sujet non traité.
2. `bash engine/setup.sh` (installe la voix, ~2 min). Si `engine/sfx/` est absent, le moteur utilise des sons synthétiques de secours.
3. Écrire `engine/spec_AAAA-MM-JJ.json`. Rendre : `cd engine && python3 build.py spec_AAAA-MM-JJ.json ../videos/AAAA-MM-JJ_<slug>.mp4`.
4. Contrôles obligatoires avant publication : durée entre 14 et 28 s (ffprobe), résolution 1080x1920, piste audio présente, loudness entre -18 et -12 LUFS (ffmpeg ebur128). Si un contrôle échoue : corriger une fois ; sinon NE PAS publier et signaler l'échec.
5. Commit et push sur `main` (message en français). Adresse publique : `https://raw.githubusercontent.com/Sammox69/flamio-videos/main/videos/<fichier>.mp4`.
6. Programmer avec Metricool (createScheduledPost, blogId 7201770) à 18:00 Europe/Paris le jour même, providers tiktok + instagram + youtube. Légende en français, 2 à 3 lignes + « Essai gratuit 1 mois, sans engagement : flamioapp.fr » + 5 à 7 hashtags (#snack #restaurant #fastfood #fidelisation #restauration #flamio + 1 lié au sujet). Réglages : tiktokData {privacyOption PUBLIC_TO_EVERYONE, title, isAigc true}, instagramData {type REEL, showReelOnFeed true, isAiGenerated true}, youtubeData {type short, privacy public, madeForKids false, isAiGeneratedContent true, title avec #Shorts}.
7. Mettre à jour `content_log.json` (date, slug, sujet, types de scènes, id du post Metricool), supprimer du dépôt les vidéos de plus de 7 jours (`git rm`), commit, push.
8. Rendre compte en 3 lignes maximum : sujet, heure de publication, lien du post dans le planificateur Metricool. En cas d'erreur, dire laquelle et ce qui n'a pas été publié.

Mode test : si le message de lancement contient « MODE TEST », exécuter toutes les étapes sauf 5 (push de la vidéo) à 7 : ne rien publier, ne rien programmer, et envoyer la vidéo à l'utilisateur.
