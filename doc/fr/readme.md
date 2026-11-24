# ChatGPT Desktop Access for NVDA

ChatGPT Desktop Access prend en charge à la fois le mode ChatGPT et le mode Codex dans l'application Windows. Il se rattache automatiquement après un changement de mode ou un retour depuis la page d'utilisation ; aucun redémarrage de NVDA n'est requis.

[![Valider l'extension NVDA](https://github.com/jcoffin1/chatgpt-desktop-access/actions/workflows/ci.yml/badge.svg)](https://github.com/jcoffin1/chatgpt-desktop-access/actions/workflows/ci.yml)

ChatGPT Desktop Access for NVDA fournit des annonces d'activité en direct, le braille, des sons de progression, la navigation et les actions de discussion, ainsi qu'un focus système accessible sur les boîtes de dialogue en mode navigation et en mode formulaire. Elle s'appelait auparavant Codex Access Toolkit et Codex Status Announcer ; l'identifiant interne de l'extension reste inchangé afin que les paramètres existants et les attributions dans Gestes de commandes continuent de fonctionner.

## Téléchargement

Note de compatibilité pour la version de développement : les analyses de transcription Chromium UIA utilisent désormais un déplacement natif groupé des points de terminaison plutôt qu'un parcours caractère par caractère de la navigation Web. L'historique, la révision des messages récents et la réactivité au démarrage nécessitent encore une vérification en direct avec l'application mise à jour avant que cette version ne soit approuvée pour publication.

Téléchargez les paquets testés depuis la [page GitHub Releases](https://github.com/jcoffin1/chatgpt-desktop-access/releases). Le projet est en cours de préparation pour le Store d'extensions officiel de NVDA, mais il n'y est pas encore répertorié.

## Paramètres

Ouvrez **Menu NVDA > Préférences > Paramètres > ChatGPT Desktop Access**. Le panneau est divisé en huit pages accessibles au clavier : **Général**, **Parole et Braille**, **Sons**, **Sorties d'activité**, **Libellés et aperçu**, **Accès au navigateur**, **Avancé** et **Assistance**.

Appuyez sur Contrôle+Tab ou Maj+Contrôle+Tab pour passer d'une page à l'autre. Chaque contrôle actif dispose d'une touche de raccourci Alt distincte au sein de sa page. Général contient les principaux choix de sortie, et Sortie d'activité contient la temporisation en arrière-plan et le routage des catégories.

Avancé contient les contrôles techniques de compatibilité. Assistance contient les actions relatives au compte, à la documentation, au dépannage et aux fichiers de paramètres.

Les paramètres incluent :

- Un interrupteur dans la page Général pour la liste native des messages de conversation, activé par défaut.
- Des libellés de progression Minimaux ou Complets (Complet par défaut).
- Des profils de parole Minimale Essentiel, Équilibré ou Informatif. Équilibré est le profil par défaut ; Essentiel limite la parole aux états critiques, tandis qu'Informatif ajoute les noms de fichiers sûrs, les compteurs et les durées utiles sans exposer les commandes complètes.
- Des profils de parole Complète Standard, Développeur ou Brut. Standard annonce une action avec des cibles concises, des compteurs et des durées utiles ; Développeur conserve les commandes normalisées complètes et la progression ; Brut conserve le libellé exact exposé. Le braille complet reste entier indépendamment du profil vocal.
- La parole et le braille configurables indépendamment.
- Un niveau de détail braille Concis, Informatif ou Complet indépendant de la verbosité vocale.
- Une protection optionnelle de la lecture de conversation qui empêche la progression courante de l'extension et les mises à jour ordinaires en direct des réponses en cours de diffusion d'interrompre la parole, de remplacer la ligne braille actuelle ou de déplacer la lecture en mode navigation dans ChatGPT. La sortie des réponses en mode formulaire, les résultats importants, les boîtes de dialogue d'autorisation et les alertes urgentes continuent normalement.
- Lors du retour à une tâche toujours active, un focus obsolète sur une carte d'activité Chromium est corrigé vers le titre de réponse le plus récent en mode navigation si une sortie plus récente le suit. Cela déplace uniquement la position de lecture virtuelle de NVDA, jamais le focus système de Windows, et toute frappe de l'utilisateur annule la correction.
- Interruption optionnelle de la parole NVDA en cours pour les autorisations urgentes et les échecs.
- Masquage optionnel des secrets probables et des données personnelles.
- L'intervalle pour les mises à jour du temps de travail écoulé.
- Une impulsion récurrente « Toujours en cours d'exécution en arrière-plan » en modes Minimal et Complet, avec de doux sons alternés à deux notes.
- Des catégories de progression individuelles. Chaque élément de catégorie indique s'il est activé et sa voie de sortie actuelle, par exemple « Commandes : activé ; parole uniquement ».
- Des mises à jour de commentaires Codex en langage clair dans les modes Minimal et Complet.
- Des sons de fin d'exécution et une journalisation de diagnostic expurgée.
- Des sons immédiats et optionnels d'envoi de message avec un délai configurable avant le début des sons continus de travail.
- La détection de l'envoi de message pour la touche Entrée et le bouton Envoyer, la détection de l'annulation de message, la suppression des événements en double et l'isolation de l'état entre les tâches Codex.
- La détection immédiate de l'envoi observe la touche Entrée non modifiée du clavier et le point 8 autonome (Entrée) d'un afficheur braille avant que ChatGPT ne remplace sa zone de message éditable. L'observateur n'intercepte ni ne renvoie jamais le geste ; Maj+Entrée et toutes les autres saisies conservent leur comportement natif.
- La protection de la saisie de message suspend les analyses complètes de compatibilité Chromium pendant la saisie de texte. Les vérifications d'état locales au message sont temporisées jusqu'à une pause dans la saisie, laissant le fil d'exécution principal de NVDA disponible pour la traduction braille, le retour de l'éditeur et le traitement normal des touches.
- Une fenêtre de stabilisation de fin d'exécution annulable empêche qu'un commentaire ne soit pris pour la fin d'une tâche lorsqu'un travail d'outil différé suit.
- Un choix entre des sons de clics originaux doux ou des sons musicaux pour chaque annonce, y compris lorsque la parole est activée. Les clics sont sélectionnés par défaut.
- Dix-sept signatures percussives de clics distinctes. Les commandes, modifications de code, recherches, tests, outils, commentaires, demandes d'attention, fins d'exécution, échecs, envois, travaux en arrière-plan et changements de focus utilisent des rythmes, des directions de hauteur et des textures différents.
- Fréquence d'interrogation en veille.
- Niveaux de clic Doux, Normal ou Fort, avec un sélecteur d'action et des boutons d'aperçu distincts pour le son uniquement et la parole uniquement.
- Libellé d'annonce modifiable pour chaque action, avec un bouton de restauration et les variables `{message}`, `{activity}`, `{seconds}` et `{duration}` pour les détails en direct.
- Routage par catégorie vers tous les canaux activés, la parole, le son, le braille ou désactivé.
- Réparation de la configuration, autotest de compatibilité, diagnostics d'assistance expurgés, rapport d'assistance expurgé enregistré dans un fichier choisi par l'utilisateur, importation/exportation des paramètres et réinitialisation ciblée du profil vocal.
- Le rapport d'assistance expurgé inclut les temps derniers et maximaux d'analyse de conversation et de sondage de mode en arrière-plan, ainsi que le nombre d'opérations lentes. Les temps lents sont journalisés au plus une fois par minute et par opération ; aucun texte de message n'est enregistré dans ces mesures. Utilisez la liste de contrôle reproductible dans `tests/performance-scenarios.md` lors de la vérification de grandes discussions, de la saisie braille, des changements de mode ou du redémarrage de NVDA.
- Contrôles de la ponctuation des commandes et de la longueur maximale énoncée. Les commandes longues complètes restent disponibles pour le braille et pour une action assignable de copie dans le presse-papiers.
- Compteurs de résultats de recherche et actualisation pour les listes de tâches Récentes et Archivées.
- Un délai d'expiration maximal pour l'activité en arrière-plan.
- Alertes haute priorité pour les autorisations et les demandes de saisie utilisateur.
- Alertes haute priorité pour les limites d'utilisation qui arrêtent le retour sonore de travail, omettent les URL brutes du tableau de bord et signalent toute heure de réinitialisation exposée, option de mise à niveau et option d'achat de crédits.
- Noms de processus d'application configurables pour les futurs hôtes Codex.
- Un son continu optionnel de travail pendant que Codex est occupé. Son intervalle est configurable, il commence après un délai de démarrage configurable et est reporté par d'autres sons de progression pour éviter tout chevauchement. Il suit le style sélectionné (Clics ou Tonalités musicales). Un signal sonore d'envoi distinct et optionnel est joué immédiatement lorsqu'un message non vide est envoyée avec Entrée ou Envoyer.
- Clics ascendants et descendants optionnels lorsque ChatGPT/Codex obtient ou perd le focus. Lorsque Alt+F4 ferme ChatGPT sans événement de focus Windows final, le signal d'inactivité est tout de même joué et la parole ainsi que le braille de NVDA reviennent à l'application précédemment focalisée sans nécessiter un autre Alt+Tab, y compris lorsque ChatGPT se ferme au démarrage avant la fin de l'attachement de la surveillance des conversations. Si cette application a également été fermée, l'extension se déplace vers la fenêtre d'application utilisable la plus haute restante au lieu de laisser NVDA sur un objet ChatGPT défunt.
- Accès natif au navigateur intégré qui laisse inchangés les rôles, états, actions, focus, Entrée, Espace, Tab, Maj+Tab, NVDA+Espace, la navigation rapide et les listes d'éléments de Chromium. Il n'y a pas de couche de commandes de navigateur distincte à apprendre.
- Messages vocaux et braille optionnels **Chargement de la page** et **Chargement terminé**. Les états natifs d'occupation du document et les événements de progression sont utilisés lorsqu'ils sont disponibles, avec un mécanisme de repli limité pour les pages qui n'exposent aucun événement final. Le retour n'analyse jamais la page et ne déplace jamais le focus.
- Un bouton **Ouvrir utilisation et crédits** pour le tableau de bord officiel du compte ChatGPT, où l'utilisateur peut consulter son utilisation et les options d'achat disponibles. L'extension n'effectue jamais d'achat automatiquement.

Le bouton **Tester les sorties d'annonce actuelles** vérifie les canaux de parole et de braille sélectionnés, y compris les sons de progression.

Le bouton **Tester le son de progression de commande** joue directement le son de commande sélectionné, quels que soient les paramètres vocaux actuels.

Choisissez une action sous **Action d'aperçu**, puis utilisez **Aperçu du son sélectionné** ou **Aperçu de la parole sélectionnée** pour n'entendre que cette sortie. Les aperçus ne lancent jamais automatiquement toute la collection de sons.

Pour personnaliser une annonce, sélectionnez son action, saisissez le libellé souhaité dans **Texte de l'annonce** et enregistrez les paramètres. Laissez le champ vide — ou choisissez **Restaurer l'annonce intégrée** — pour utiliser le libellé standard de l'extension. Par exemple, `Toujours occupé avec {activity} après {duration}` conserve les détails en direct de la progression en arrière-plan. Utilisez `{message}` partout où le texte original de commande ou de progression en mode Complet doit apparaître dans un libellé personnalisé.

L'exportation des paramètres propose `chatgpt-desktop-access-settings.json` comme nom de fichier ; l'utilisateur peut choisir un autre nom ou emplacement. Les rapports d'assistance continuent d'utiliser un nom de fichier texte horodaté. Aucun fichier n'est créé tant que l'utilisateur n'a pas approuvé sa boîte de dialogue Enregistrer.

Après chaque premier démarrage d'une version nouvellement installée, NVDA ouvre un résumé concis de la version actuelle et place le focus en haut. **Afficher les notes de version actuelles…** et **Afficher l'historique complet des versions…** sont également disponibles dans le panneau des paramètres de l'extension.

## Gestes de commandes

Toutes les actions de l'extension apparaissent sous **Menu NVDA > Préférences > Gestes de commandes > ChatGPT Desktop Access**. Un geste par défaut peut y être modifié ou supprimé, et une action non attribuée peut recevoir un geste si nécessaire.

### Révision des messages récents

Contrôle+1 à Contrôle+0 permettent de réviser les dix messages les plus récents de l'utilisateur ou de ChatGPT :

- Contrôle+1 lit le message le plus récent.
- Contrôle+2 lit l'avant-dernier message.
- La séquence continue jusqu'à Contrôle+0, qui lit le dixième message le plus récent.

Chaque position est une action nommée séparément. Ces raccourcis fonctionnent aussi bien en mode formulaire qu'en mode navigation. Dans les conversations ramifiées et latérales, la révision suit la branche actuellement visible. L'extension maintient un petit cache de la branche active afin qu'une commande de révision n'analyse pas à nouveau l'intégralité de l'arborescence d'accessibilité Chromium.

Pour obtenir une liste native au lieu de la vue Web de la conversation, attribuez **Ouvrir les messages de la conversation actuelle dans une liste native** sous Gestes de commandes NVDA, puis utilisez cette attribution lorsque ChatGPT a le focus. Aucune touche n'est attribuée par défaut ; NVDA+Alt+Maj+R est déjà utilisé par NVDA pour la compatibilité des extensions.

La page Général des paramètres permet d'activer ou de désactiver la liste ; elle est activée par défaut. La boîte de dialogue affiche jusqu'aux 100 derniers échanges visibles, du plus ancien au plus récent. Utilisez les flèches pour parcourir la liste ; Entrée déplace vers le texte intégral en lecture seule du message sélectionné. La recherche et l'actualisation sont disponibles ; Actualiser demande une nouvelle analyse sans bloquer la boîte de dialogue. Échap ferme la boîte de dialogue. Les échanges plus anciens restent dans la vue de conversation de ChatGPT. La liste n'envoie, ne modifie ni n'active aucun message.

### Mode vocal

NVDA+Alt+V démarre ou arrête le mode vocal de ChatGPT. **Couper ou réactiver le micro de ChatGPT** n'a pas de geste par défaut ; attribuez-en un dans Gestes de commandes si souhaité.

Les versions antérieures attribuaient NVDA+Alt+M à l'action du microphone. Cette touche est la commande par défaut de NVDA **Interagir avec le contenu mathématique**, l'extension ne la réserve donc plus. Une attribution de microphone existante créée par l'utilisateur reste configurable dans Gestes de commandes.

### Chat et Travail

Au-dessus du champ de message d'une nouvelle discussion, ChatGPT dispose d'un commutateur **Chat** et **Travail**. Les deux réglages offrent des outils différents et un menu **Ajouter des fichiers et plus** différent. NVDA+Alt+W indique lequel est sélectionné, par exemple « Travail sélectionné. Appuyez deux fois rapidement pour passer à Chat ». Appuyez deux fois rapidement sur NVDA+Alt+W pour basculer. L'action est nommée **Annoncer si le champ de message de ChatGPT est réglé sur Chat ou Travail ; appuyer deux fois pour basculer**. Si le commutateur n'est pas affiché, comme dans une conversation existante ou dans Codex, NVDA le signale.

### Ce qui est joint au message

NVDA+Alt+A indique quels fichiers et outils sont joints au message que vous rédigez, par exemple « Joint : rapport.pdf. Outils : Recherche Web », ou « Rien n'est joint au message ». Des outils tels que Recherche Web, Créer une image et Recherche approfondie apparaissent à l'intérieur du champ de message, où NVDA ne les lit autrement que comme un objet sans étiquette. L'action est nommée **Annoncer les fichiers et outils joints au message ChatGPT**. Pour supprimer un fichier, utilisez Tab ou déplacez-vous en mode navigation jusqu'à son bouton **Supprimer** au-dessus du champ de message.

### Sélecteur de mode ChatGPT et Codex

NVDA+accent grave — la touche normalement étiquetée backtick (`` ` ``) — ouvre et place le focus sur le sélecteur de mode natif de ChatGPT. L'action est nommée **Ouvrir et placer le focus sur le sélecteur de mode ChatGPT et Codex**.

La commande fonctionne sans naviguer vers le haut de la page. NVDA annonce le mode actuel. Utilisez les flèches Haut ou Bas pour choisir ChatGPT ou Codex, puis appuyez sur Entrée.

### Portée des gestes et actions supplémentaires

Les dix commandes de révision de messages, la commande du mode vocal, l'action du microphone, la commande du sélecteur de mode, la commande Chat et Travail et le rapport des pièces jointes sont implémentés par le module d'application de ChatGPT. Les gestes par défaut et attribués par l'utilisateur ne sont interceptés que lorsque ChatGPT ou Codex a le focus. En dehors des deux, NVDA et les autres extensions restent libres d'utiliser les mêmes frappes au clavier.

Les actions supplémentaires non attribuées comprennent :

- Répéter la dernière activité ou parcourir l'historique des annonces.
- Afficher ou effacer l'historique des annonces.
- Mettre en pause ou reprendre les annonces.
- Basculer entre la sortie Minimale et Complète ou le masquage de confidentialité.
- Afficher ou copier les diagnostics et enregistrer un rapport d'assistance expurgé. Le rapport indique la version installée de l'application ChatGPT, qui change à chaque mise à jour de ChatGPT.
- Ouvrir l'utilisation et les crédits dans le tableau de bord officiel du compte ChatGPT.
- Ouvrir l'historique de discussion ChatGPT ou Codex consultable par recherche.

N'attribuez que les commandes supplémentaires que vous souhaitez. Le navigateur intégré n'ajoute délibérément aucune action dans Gestes de commandes ; utilisez plutôt les commandes normales de navigation Web de NVDA.

### Historique des chats

**Ouvrir l'historique des chats de ChatGPT ou de Codex avec recherche et navigation par flèches** ouvre une boîte de dialogue réactive et spécifique au mode depuis le mode formulaire ou le mode navigation. Tapez pour rechercher, appuyez sur Tab pour passer des chats récents aux chats archivés, utilisez les flèches Haut et Bas pour parcourir et appuyez sur Entrée pour ouvrir le chat sélectionné.

Sur une discussion récente, Maj+F10 ouvre un menu contextuel Windows. Le focus démarre sur **Épingler ou désépingler la discussion** ; appuyez sur Flèche bas pour **Archiver la discussion**, puis appuyez sur Entrée pour exécuter l'action native ChatGPT sélectionnée. Sur une discussion archivée, Maj+F10 propose **Ouvrir la discussion archivée**.

Si deux discussions récentes portent le même titre, l'extension ne peut pas en identifier une de manière sûre à partir du seul titre. Ouvrir, Épingler et Archiver vous demandent alors de choisir la discussion souhaitée dans la liste native des discussions récentes de ChatGPT ; aucune discussion n'est modifiée automatiquement.

La région native des discussions récentes de ChatGPT combine les discussions ChatGPT et les tâches Codex. L'extension sépare cette région à l'aide de l'index de session Codex local actif, de sorte que l'historique ChatGPT exclut les titres de tâches Codex et que l'historique Codex ne conserve que les titres de tâches Codex.

L'extension lit le contrôle de mode actuel exposé par ChatGPT car le document de l'application lui-même reste nommé ChatGPT dans les deux modes. Après un changement de mode, elle attend que la barre latérale unifiée se stabilise et confirme deux instantanés correspondants avant de séparer les entrées. Si l'historique est ouvert trop tôt, NVDA signale que la liste est en cours d'actualisation au lieu d'afficher une liste non classée.

Les titres archivés de Codex sont lus à partir des métadonnées de session JSONL locales. Les titres archivés de ChatGPT proviennent uniquement de la vue accessible des discussions archivées de ChatGPT. Si cette vue n'a pas encore été exposée, la boîte de dialogue explique comment la charger.

Les contrôles de message et les panneaux de sources — y compris Partager, Copier, Lire à voix haute, les évaluations de réponses, les Sources, les Sorties et Plus d'actions — sont exclus des deux listes d'historique.

Lorsque les discussions récentes proposent **Afficher plus**, l'ouverture de l'historique active ce contrôle natif une page à la fois et attend que le nombre d'éléments accessibles augmente. Chaque demande est limitée à 20 pages de dix éléments ; rouvrez l'historique pour continuer s'il reste d'autres pages.

Cette expansion utilise uniquement le contrôle **Afficher plus** de ChatGPT. Elle ne simule pas le défilement dans une mise en page à défilement infini, s'arrête si le focus quitte ChatGPT et ne modifie jamais l'état d'archivage simplement en ouvrant l'historique.

### Contrôles de la barre d'outils de message

L'extension améliore **Ajouter des fichiers et plus**, le contrôle de **modèle** et **Modifier les autorisations** sans ajouter de commandes ni de gestes. Atteignez-les avec la navigation normale par Tab ou en mode navigation.

Le sélecteur de produit de l'application de bureau bascule entre ChatGPT et Codex. Dans ChatGPT, le commutateur séparé Chat/Travail apparaît au-dessus de la zone de rédaction d'une nouvelle discussion. Dans Work et Codex, le contrôle de modèle et de raisonnement apparaît sous la zone de rédaction. L'extension reconnaît à la fois les noms complets de modèles préfixés par GPT et les libellés plus courts tels que **6 Sol Light** sans conserver une liste fixe de modèles. Le compte et l'application déterminent les choix disponibles ; l'extension ne choisit pas automatiquement un modèle ou un niveau de raisonnement.

NVDA donne à chaque contrôle reconnu une description concise tout en préservant son nom, son état et son action natifs. Pour les menus de modèle et d'autorisations, utilisez Entrée ou Espace pour ouvrir, les touches fléchées pour naviguer, Entrée pour choisir et Échap pour fermer.

Le bouton **Ajouter des fichiers et plus** ouvre une fenêtre contextuelle que ChatGPT ajoute à la fin de la page. ChatGPT ramène ensuite le focus clavier sur le message, où les touches fléchées déplacent une surbrillance qui n'est jamais annoncée, et Tab ou Entrée choisit l'option en surbrillance sans dire laquelle c'était.

Les options de la fenêtre contextuelle dépendent de l'endroit où vous vous trouvez. Dans Codex, et dans ChatGPT avec **Travail** sélectionné, elle répertorie des éléments tels que Fichiers et dossiers, Objectif, Mode Plan, Croquis et plugins, et peut se terminer par **Tapez pour rechercher des fichiers ou des discussions**. Dans ChatGPT avec **Chat** sélectionné, où le champ de message s'appelle **Demander à ChatGPT**, elle répertorie des éléments tels que Ajouter des photos et des fichiers, Ajouter depuis la bibliothèque, Créer une image, Recherche Web, Recherche approfondie et Croquis. L'extension gère les deux.

Lorsque vous activez **Ajouter des fichiers et plus** avec la touche Entrée, Espace ou Entrée braille, l'extension lit la fenêtre contextuelle et ouvre une liste **Ajouter des fichiers et plus**. Chaque option est répertoriée avec son titre d'abord, puis sa description et, lorsque ChatGPT regroupe les options, sa section, par exemple « GitHub — Trier les PR, les problèmes, la CI et les flux de publication (Plugins) ».

Utilisez les touches fléchées ou tapez une première lettre, appuyez sur Entrée pour choisir, ou utilisez Tab jusqu'à **Filtrer les options** et tapez une partie d'un nom. Échap annule et ferme la fenêtre contextuelle de ChatGPT.

Après votre choix, l'extension revient à ChatGPT, rouvre la fenêtre contextuelle et déplace la propre surbrillance de ChatGPT jusqu'à votre option une ligne à la fois, en vérifiant chaque étape, puis la sélectionne. Gardez les mains éloignées du clavier pendant un instant pendant qu'elle effectue cette opération. Vous entendez ensuite ce qui a été ajouté au message, tel que « GitHub ajouté », ou NVDA lit la boîte de dialogue ouverte par l'option, telle que **Sélectionner des fichiers**.

Si les options ne peuvent pas être lues mais que la fenêtre contextuelle se termine par **Tapez pour rechercher des fichiers ou des discussions**, l'extension ramène plutôt NVDA en mode navigation sur cette ligne. Appuyez sur Flèche haut pour lire les options au-dessus et sur Entrée pour en choisir une.

Si la fenêtre contextuelle n'apparaît pas, l'extension se rabat sur le contrôle distinct **Joindre des fichiers ou connecter des applications** que certaines vues Codex affichent sous la navigation **Messages de l'utilisateur**. Si aucun des deux n'est présent, si la fenêtre change ou si vous naviguez ailleurs, l'extension ne touche pas au focus. Elle ne choisit jamais que l'option que vous avez sélectionnée et ne choisit jamais un fichier à votre place.

#### Les menus de suggestions « / » et « @ »

Taper « / » ou « @ » dans le champ de message ouvre un menu de suggestions de commandes, ou de fichiers, d'outils et de discussions. ChatGPT maintient le focus dans le champ de message et déplace une surbrillance non annoncée à l'aide des touches fléchées. L'extension indique combien il y a de suggestions et laquelle est mise en surbrillance, par exemple « Suggestions : 28. Commentaires, Envoyer des commentaires sur cette discussion, 1 sur 28 », et annonce chacune d'elles lorsque vous appuyez sur Flèche haut ou Flèche bas, comme « Objectif, Définir un objectif à poursuivre, 2 sur 28 ». Taper davantage filtre la liste ; l'extension annonce la nouvelle première suggestion lorsque la liste change. Appuyez sur Tab ou Entrée pour choisir, ou sur Échap pour fermer.

Désactivez cette fonction avec **Annoncer les menus de suggestions « / » et « @ » dans le champ de message** dans la catégorie Général des paramètres. Si l'extension distincte Slash Menus est installée, cette extension lui laisse ces menus afin que les deux ne parlent jamais en même temps.

#### Diagnostics du menu des pièces jointes

Si la fenêtre contextuelle ne fonctionne toujours pas, activez **Activer la journalisation de diagnostic expurgée** dans la catégorie Avancé des paramètres, puis ouvrez **Ajouter des fichiers et plus**. L'extension enregistre l'endroit où apparaît la fenêtre contextuelle : le focus de NVDA, les menus et éléments de menu UI Automation et toute nouvelle fenêtre ChatGPT. Enregistrez ensuite un rapport d'assistance depuis la catégorie Assistance des paramètres ; la capture se trouve à la fin. **Capturer les diagnostics pour le menu Ajouter des fichiers et plus ouvert**, une commande non attribuée dans Gestes de commandes, capture à la demande pendant que le menu est ouvert. Seuls les noms de contrôles de type menu sont enregistrés, jamais le texte de la discussion.

Si l'application de bureau n'expose pas de contrôle de pièce jointe fonctionnel, ouvrez la conversation dans ChatGPT sur le Web dans votre navigateur et utilisez son menu de rédaction.

## Accès au navigateur intégré

Lorsque ChatGPT expose un conteneur de navigateur ou d'aperçu Web via l'accessibilité Chromium, l'extension reconnaît les objets situés sous ce conteneur explicitement nommé. Elle reconnaît également un véritable document Web imbriqué à l'intérieur du document externe de ChatGPT, ce qui correspond à la façon dont certains onglets de navigateur sont exposés. Le sous-menu natif Navigateur et ses commandes sont délibérément exclus. L'extension ne clique pas, ne soumet pas, ne déplace pas le focus, ne remplace pas les rôles natifs, n'ajoute pas de descriptions de contrôle et ne lit pas la page à la place de l'utilisateur.

Le résultat fonctionne comme une page Chromium ordinaire dans NVDA. En mode formulaire, utilisez Tab et Maj+Tab pour vous déplacer entre les contrôles, Entrée ou Espace pour activer le contrôle natif actuel, et les touches fléchées là où le contrôle les prend en charge.

Appuyez sur NVDA+Espace pour basculer entre les modes formulaire et navigation. En mode navigation, utilisez la navigation Web normale de NVDA, notamment H pour les titres, K pour les liens, F pour les champs de formulaire, D pour les régions, T pour les tableaux et NVDA+F7 pour la Liste d'éléments.

Aucune de ces touches n'est interceptée ni simulée par l'extension.

L'extension conserve son tampon virtuel de conversation Codex d'origine pendant que le focus se trouve à l'intérieur de la page intégrée. Cela permet à la surveillance de l'activité Codex de se poursuivre sans traiter la page comme une nouvelle tâche ni se détacher de la conversation.

La catégorie Accès au navigateur des paramètres comporte une option, activée par défaut, pour les messages automatiques **Chargement de la page** et **Chargement terminé**.

L'extension observe la création native de documents Chromium, les changements d'état d'occupation et la progression du chargement exposée. Un court minuteur de stabilisation termine les pages rapides qui n'exposent pas d'événement final. Un délai de sécurité plus long s'applique tant que Chromium signale le document comme occupé.

Les événements répétés ne repètent pas le même message. La fermeture ou la sortie du navigateur intégré annule l'état de chargement en attente, de sorte qu'une ancienne page ne puisse pas annoncer son achèvement plus tard. Ces messages d'état ne modifient pas le focus, le mode navigation, le curseur de revue ni la position de lecture braille.

L'historique des annonces contient au plus 20 entrées, reste en mémoire et est effacé lorsque le document Codex surveillé change ou que NVDA se ferme.

## Tests et compilation

Exécutez `build.ps1` pour lancer les tests automatisés, valider le modèle de traduction et la syntaxe Python, auditer la cohérence des versions, les dépendances, la politique de gestes, la structure de l'archive, les CRC et l'inventaire sonore, et créer un paquet reproductible sous `outputs`.

GitHub Actions exécute les mêmes vérifications de version lors des envois (push) et des demandes d'extraction (pull requests). Si Python n'est pas disponible sous le nom `python`, indiquez son exécutable avec `-PythonPath`. Des fichiers source identiques produisent une somme de contrôle de paquet identique, y compris entre les extractions Git LF et CRLF.

Consultez `docs/TESTING.md` pour la liste de contrôle manuelle NVDA utilisée avant de publier une version. Les contributeurs aux traductions doivent consulter `docs/TRANSLATING.md`. Les mainteneurs du Store d'extensions doivent consulter `docs/ADDON_STORE.md`.

## Gestion des versions

Les versions de l'extension suivent la version stable actuelle de NVDA. Avec NVDA 2026.2 stable, la ligne de base est 2026.2.0 et les correctifs de l'extension sont 2026.2.1, 2026.2.2, 2026.2.3, 2026.2.4, 2026.2.5, 2026.2.6, 2026.2.7, 2026.2.8, et ainsi de suite. Une nouvelle version stable de NVDA démarre une nouvelle ligne correspondante. Les versions préliminaires (preview) de NVDA ne modifient pas la ligne de version de l'extension. Consultez `docs/VERSIONING.md` pour tous les détails.

## Confidentialité

Le mode Complet peut énoncer des commandes, des commentaires, des chemins d'accès, des noms de fichiers, des URL et des termes de recherche. Le journal de débogage de NVDA enregistre la sortie vocale, indépendamment de la journalisation interne expurgée de l'extension. Activez le masquage ou le mode Minimal avant de partager un journal NVDA, et vérifiez l'absence de données personnelles dans les journaux avant de les envoyer à quiconque.

L'action de masquage de confidentialité peut être attribuée dans Gestes de commandes pour des changements temporaires de confidentialité. Le masquage s'applique également aux commentaires complets conservés pour le braille, l'historique et l'action Copier la dernière progression complète de Codex. Les diagnostics expurgés signalent la configuration et l'état de surveillance sans inclure le texte des commandes.

## Temporisation braille

La progression utilise le mécanisme standard de messages flash braille de NVDA. Sa durée est contrôlée par le paramètre global de délai d'expiration des messages braille de NVDA.

Les messages braille de routine de l'extension sont supprimés lorsque le focus se trouve dans ChatGPT et que **Maintenir stable la lecture de la conversation** est activé. Pendant que l'utilisateur lit en mode navigation, les mises à jour ordinaires de régions dynamiques en flux `Réponse :`, `ChatGPT a dit :` et `Réponse terminée` sont également retenues du gestionnaire de sortie natif de NVDA. Cela les empêche de remplacer la parole, le curseur de navigation ou la fenêtre d'affichage braille.

Les flashs de fin d'exécution non urgents de l'extension sont retenus du braille au même moment, tandis que leur sortie vocale et sonore sélectionnée continue. La sortie des réponses en mode formulaire, les messages d'autorisation, les boîtes de dialogue et les alertes urgentes ne sont jamais supprimées.

L'inspection complète du tampon de conversation est mise en pause pendant la modification de message et pendant trois secondes après une navigation au clavier ou au braille dans une conversation. Les événements directs d'état et d'autorisation restent disponibles sans attendre une analyse. Lorsque Chromium remplace son tampon, l'extension n'inspecte qu'une fin limitée au lieu de copier toute la discussion.

Après une réponse finale, les impulsions de travail et les sons continus se mettent en pause pendant que l'extension attend cinq secondes une autre opération et exige l'absence du contrôle Arrêter. Elle confirme ensuite que la tâche est inactive.

La fermeture ou le masquage de la fenêtre ChatGPT pendant deux secondes efface l'activité conservée, même si des processus auxiliaires Electron restent actifs. Le simple fait de passer à une autre application maintient la surveillance active.

Lors de la saisie de braille abrégé dans le message ChatGPT focalisée, l'extension protège également la composition active d'un nouveau mot contre l'événement de curseur différé que Chromium peut émettre pour le mot précédent. Cela ne modifie pas les tables de traduction, ne consomme pas les gestes braille, ne remplace pas le gestionnaire d'entrée de NVDA et ne s'exécute pas en dehors du message ChatGPT.

## Installation et suppression

Installez le paquet `.nvda-addon` via le gestionnaire de la boutique d'extensions NVDA. Redémarrez NVDA lorsque cela est demandé. Supprimez-le ou désactivez-le depuis le même gestionnaire. Les mises à niveau conservent les paramètres enregistrés ; les nouvelles fonctionnalités utilisent des valeurs par défaut sûres.

## Assistance et compatibilité

L'extension prend en charge NVDA 2023.1 et versions ultérieures et a été testée avec NVDA 2026.2 stable. Si une mise à jour de l'interface Codex interrompt les annonces, activez les diagnostics expurgés et fournissez un journal NVDA après avoir supprimé les clés distantes et autres données personnelles.

Après chaque mise à jour de ChatGPT, l'extension vérifie une fois qu'elle peut toujours trouver le champ de message, **Ajouter des fichiers et plus** et le commutateur de mode ChatGPT et Codex. Le résultat figure dans le journal NVDA et sur la ligne **Vérification de compatibilité ChatGPT** du rapport d'assistance. Si quelque chose manque après une mise à jour, NVDA indique une fois que certaines fonctionnalités de l'extension peuvent ne pas fonctionner tant que l'extension n'est pas mise à jour.

## Licence

ChatGPT Desktop Access est un logiciel libre distribué sous la licence publique générale GNU (GNU General Public License), version 2 ou, à votre choix, toute version ultérieure. Consultez `LICENSE.txt` pour les termes complets de la licence.
