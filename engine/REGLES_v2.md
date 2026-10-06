# RÈGLES VIDÉO v2 (priorité absolue sur PLAYBOOK.md et topics.md en cas de conflit)

## Pourquoi
Analyse TikTok du 05/10 : 93 % des spectateurs partaient à la 1re seconde, et Sam trouve les explications trop courtes : on ne comprend pas À QUI la vidéo s'adresse, QUEL est le problème, QUELLE est la solution, ni COMMENT l'utiliser.

## Structure obligatoire (5 scènes, 22 à 32 s au total, jamais plus de 34 s)
1. hook (3 à 5 s parlées) : le "pill" nomme la CIBLE (ex. « GÉRANTS DE KEBAB », « PIZZERIAS ET SNACKS »). Le titre (3 lignes courtes, "size" 138 max) est une phrase tranchée sur une situation concrète. Le "say" commence par la cible (« Gérants de kebab. ») puis lit le titre mot pour mot, puis une courte phrase de résolution. Interdit : question vague, « Conseil/Astuce/Savez-vous » en 1er mot, chiffres inventés.
2. LE PROBLÈME (type "tips", pill « LE PROBLÈME ») : 3 cartes qui décrivent concrètement ce qui se passe chez le gérant. Le "say" explique le problème en 1 ou 2 phrases simples.
3. LA SOLUTION (type phone_sms / phone_loyalty / phone_review / phone_dash, pill « LA SOLUTION ») : dit clairement que c'est Flamio et ce que Flamio fait pour résoudre CE problème.
4. COMMENT ÇA MARCHE (type "tips", pill « COMMENT ÇA MARCHE », 3 étapes numérotées dans l'ordre : ce que fait le client, ce que fait Flamio, ce que voit/fait le gérant). N'utilise QUE les faits autorisés du PLAYBOOK (scan de QR code sans appli, points et cadeaux, SMS automatiques, tableau de bord, avis Google, parrainage). N'invente aucune étape d'installation, aucun délai (« en 5 minutes »), aucun prix hors vidéo OFFRE.
5. cta (garde le CTA actuel : « Essayez Flamio gratuitement un mois, sur flamio app point f r. »).
Vouvoiement. Phrases courtes. 70 à 100 mots parlés au total.

## Musique
Chaque spec contient "music": un entier de 0 à 5 (6 styles différents : 0 house 124 bpm, 1 hip-hop 96, 2 funk 112, 3 house 128, 4 chill 88, 5 afro-pop 118). Les 3 vidéos du jour utilisent 3 styles différents, et le style d'une vidéo est différent de celui des 6 dernières vidéos du journal (champ "music" du journal : ajoute-le à chaque entrée).

## Contrôles
Durée 22 à 34 s, 1080x1920, audio présent, -18 à -12 LUFS. Extraire les images n°3, n°130, n°400 (ffmpeg) et les regarder : aucun mot coupé, texte dans les marges (gauche 70 px, droite 160 px, haut 220 px, bas 450 px).

## Hashtags (priorité sur le PLAYBOOK) : 5 MAXIMUM par post, jamais plus. #flamio + 4 liés au sujet.

## Prononciation de la voix
La voix française lit mal les mots anglais (« burger » devenait « burgé »). build.py applique automatiquement un dictionnaire de respellings au texte "say" (burger, tacos, kebab, bubble tea, food truck, fast-food, Google, wifi, cheese, brunch, milkshake, ketchup, sandwich, nuggets, TikTok, YouTube, followers, like, live, reel, story, marketing, business...). Les sous-titres ("cap") et les titres gardent l'orthographe normale.
Règle : dans "say", écris le mot normalement s'il est dans cette liste. Pour tout autre mot étranger ou inhabituel (marque, anglicisme), écris-le phonétiquement à la française dans "say" (ex. « ketchup » → « kétchoupe ») ou reformule avec un mot français. En cas de doute, évite le mot.
Rappel : « S M S », « Q R code », « flamio app point f r » dans "say".

## Fonctionnalité retirée : cadeaux et SMS d'anniversaire
Les cadeaux et SMS d'anniversaire n'existent PLUS dans Flamio (info de Sam, 06/10). Ne jamais les mentionner (ni dans la voix, ni dans les titres, ni dans les SMS d'exemple à l'écran, ni dans la légende, ni dans les hashtags). Retire « SMS d'anniversaire » de la liste des thèmes de l'étape 3. Cette règle prime sur le PLAYBOOK et les instructions de la routine.
