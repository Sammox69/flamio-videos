# RÈGLES VIDÉO v2 (priorité absolue sur PLAYBOOK.md et topics.md en cas de conflit)

## Pourquoi
Analyse TikTok du 05/10 : 93 % des spectateurs partaient à la 1re seconde, et Sam trouve les explications trop courtes : on ne comprend pas À QUI la vidéo s'adresse, QUEL est le problème, QUELLE est la solution, ni COMMENT l'utiliser.

## Structure obligatoire (5 scènes, 22 à 32 s au total, jamais plus de 34 s)
1. hook (3 à 5 s parlées) : le "pill" nomme la CIBLE (ex. « GÉRANTS DE KEBAB », « PIZZERIAS ET SNACKS »). Le titre (3 lignes courtes, "size" 138 max) est une phrase tranchée sur une situation concrète. Le "say" commence par la cible (« Gérants de kebab. ») puis lit le titre mot pour mot, puis une courte phrase de résolution. Interdit : question vague ou générale, « Conseil/Astuce/Savez-vous » en 1er mot, chiffres de résultat inventés. (La forme du hook dépend du TYPE D'ACCROCHE imposé par la phase de test ci-dessous.)
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

## PHASE DE TEST DES ACCROCHES (du 08/10/2026 au 07/12/2026) — priorité sur la forme du hook ci-dessus
Contexte : stats TikTok très faibles (1,3 s de visionnage moyen, 0,35 % jusqu'au bout). Stratégie de Sam : beaucoup de contenu, mais en testant des accroches DIFFÉRENTES pour apprendre ce qui retient. Chaque vidéo teste un TYPE d'accroche. Ajoute le champ "hook_type" (lettre A à F) au spec ET au journal.
Les 6 types (la structure en 5 scènes, la cible dans le pill et les faits autorisés restent obligatoires) :
- A "affirmation choc" : phrase tranchée sur une situation (« Il est venu une fois. Plus jamais. »).
- B "question douloureuse" : question PRÉCISE sur un problème concret du gérant (« Combien de clients ne reviennent jamais chez vous ? »), jamais une question vague.
- C "scène" : une mini-scène datée et concrète (« Il est 15 h. Votre snack est vide. »).
- D "erreur à arrêter" : un ordre/interdit (« Arrêtez les cartes en papier. Voici pourquoi. »).
- E "bénéfice direct" : la promesse de résultat sans chiffre (« Vos clients reviennent. Sans que vous leur parliez. »).
- F "mythe" : on démonte une idée reçue (« Fidéliser coûte cher. Faux. »).
Choix : lis le journal ; compte les "hook_type" déjà utilisés ; les 3 vidéos du jour utilisent 3 types différents, en prenant les types les MOINS utilisés jusque-là (à égalité, tire dans l'ordre alphabétique décalé d'un cran chaque jour). Les 3 vidéos du jour ne doivent pas non plus partager la même cible. La première vidéo de chaque type est écrite sans a priori ; ne force pas un type si les faits autorisés ne le permettent pas (change alors de thème, pas de type).
Pendant la phase de test, ne favorise PAS un type d'après learnings.json (équilibre strict) ; utilise learnings.json seulement pour éviter les thèmes/cibles les plus faibles.
APRÈS le 07/12/2026 : si learnings.json contient un classement des types (champ "classement_hook_type" et "phase":"decision"), consacre 2 vidéos sur 3 aux 2 meilleurs types et 1 sur 3 à un type moins utilisé (exploration), puis continue d'itérer.

## HOOK 3D (carte de fidélité animée) — test, environ 1 vidéo sur 3
Sur la scène hook d'une vidéo, ajoute `"d3":true` pour afficher une carte de fidélité Flamio en 3D (jetons qui tombent, 10/10, particules) sous le sous-titre. Règles :
- 1 vidéo sur 3 au maximum (une seule des 3 vidéos du jour), jamais plus. Compatible avec tous les types d'accroche A à F.
- Avec d3 : "size" du hook = 104 (jamais plus), titre de 3 lignes maximum, pas de "deco" nécessaire. Optionnel : "reward" (texte de la carte pleine, défaut "CADEAU DÉBLOQUÉ"), "slots" (défaut 10), "brand".
- Ajoute "d3":true/false au journal pour chaque vidéo (analyse hebdomadaire : comparer les vidéos d3 aux autres).
- build.py affiche "3D: ok" ou "3D: indisponible". Si indisponible, la carte n'est simplement pas dessinée : continue normalement.
- Le rendu 3D est plus lent (environ 3 à 4 minutes de plus par vidéo avec d3). Garde cela en tête dans le planning du rendu.

## Voix (depuis le 16/10 : voix du narrateur de la VSL, remplace la voix clonée de Sam)
build.py applique automatiquement : voix plus dynamique, pauses longues raccourcies, rythme +8 %, son nettoyé, et « f r » lu « effe erre » (écris toujours « flamio app point f r » dans "say").

## TARIFS (mise à jour du 16/10/2026 — PRIORITÉ ABSOLUE, remplace TOUT ancien prix : 149 € et 1 490 € n'existent plus)
Essai gratuit 1 mois avec toutes les fonctions, sans engagement, résiliable à tout moment depuis le tableau de bord ; on choisit sa formule à la fin de l'essai. Ne jamais écrire ni dire « HT », « hors taxes » ni mentionner la TVA. Trois formules :
- ÉTINCELLE 49 € par mois, 50 SMS inclus par mois : programme de fidélité par QR code, base clients (numéros collectés automatiquement), points, cadeaux et statistiques, clients illimités.
- FLAMME 99 € par mois, 150 SMS inclus : tout Étincelle + avis Google et retours de satisfaction, parrainage entre clients, vidéos TikTok récompensées, offres flash par SMS.
- BRASIER 129 € par mois (formule « recommandée » : seule formule qualifiée ainsi), 300 SMS inclus : tout Flamme + relance automatique des clients inactifs, demande d'avis automatique après la visite, défis par SMS pour faire revenir les clients, accompagnement à la mise en place.
- SMS en plus : recharge de 250 SMS pour 25 €, sans expiration.
Règles : les prix ne sont cités QUE dans une vidéo de type OFFRE (une par semaine maximum) ; jamais d'ancien prix ; ne dis pas « par restaurant ». Dans une vidéo offre, rattache chaque fonction à la bonne formule (ex. relance automatique des clients inactifs = Brasier ; avis Google et parrainage = Flamme ; QR code, points et cadeaux = Étincelle). Dans les autres vidéos, ne cite aucun prix ; parle des fonctions sans dire dans quelle formule elles sont, et évite de promettre « tout inclus ». Ne cite jamais le nom « Brasier/Flamme/Étincelle » hors vidéo offre.

## ÉTAPES DE L'ENTONNOIR TOFU / MOFU / BOFU (mise en place le 12/10/2026 — chaque vidéo a une "etape")
Ajoute le champ "etape" ("TOFU", "MOFU" ou "BOFU") au spec ET au journal, à côté de hook_type. Les 3 vidéos du jour couvrent les 3 étapes : n°1 (12:30) = TOFU, n°2 (18:00) = MOFU, n°3 (20:30) = BOFU. Elles gardent la structure en 5 scènes, les hook_type, les tarifs et toutes les autres règles ; seul le fond change :
- TOFU (toucher) : une douleur ou une situation vécue par le gérant de la cible (clients qui ne reviennent pas, jours creux, avis absents...). Le hook compte le plus (c'est ici que les types A à F et le hook 3D servent le mieux). La solution reste légère : une idée ou un conseil utile, Flamio seulement évoqué en une phrase, aucun forfait, aucun prix. CTA doux : « Suivez-nous pour d'autres conseils » + flamioapp.fr discret.
- MOFU (convaincre) : montrer comment ça marche concrètement avec les scènes phone_* (carte QR, SMS, avis, tableau de bord). On explique une fonction précise et son bénéfice pour la cible. Aucun prix. CTA : « Découvrez-le sur flamioapp.fr ».
- BOFU (convertir) : lever une objection (« et si mes clients ne scannent pas ? », « c'est trop compliqué ? », « je n'ai pas le temps »), ou rappeler l'essai gratuit d'1 mois sans engagement, ou une mise en situation de démarrage en 5 minutes. Aucun chiffre de résultat inventé. CTA direct : « Essai gratuit 1 mois, sans engagement : flamioapp.fr ». Les prix n'apparaissent que dans une vidéo OFFRE (max 1 par semaine, voir TARIFS) : une OFFRE est forcément la vidéo BOFU du jour.
La contrainte « 3 formats différents par jour » et « 3 hook_type différents par jour » reste valable. La phase de test des accroches continue : l'étape ne remplace pas le hook_type, elle s'y ajoute. Si learnings.json contient un classement "classement_etape", favorise légèrement l'étape qui retient le mieux mais garde les 3 étapes chaque jour.
