🎮 Borne d'Arcade - 1 VS 1

Bienvenue sur le dépôt du projet Borne d'Arcade ! Ce projet consiste à créer une mini borne d'arcade avec un jeu 1 contre 1, utilisant une Raspberry Pi, des boutons et un joystick. 🕹️

🚀 Fonctionnalités

🏆 Menu principal : accès aux autres écrans et présentation des meilleurs scores

🎮 Écran de jeu : combat en 1v1 avec joystick et boutons

🏁 Écran de fin de partie : affichage du gagnant et son score

📜 Écran d'instructions : explication des commandes et règles du jeu

⚙️ Écran d'options : personnalisation des statistiques des joueurs

👥 Modèle de données

🔹 Joueurs

Chaque joueur possède :

🔵 Différenciation Joueur 1 / Joueur 2

⚡ Vitesse de rotation & de déplacement

❤️ Points de vie

🔫 Puissance & délai de tir

💨 Vitesse des projectiles

🏆 Scores

Chaque score comprend :

👤 Pseudo du joueur

🔢 Score obtenu

🛠️ Matériel et Contrôles

🎮 Capteurs d'action :

2 joysticks (1 par joueur)

4 boutons poussoirs (2 par joueur)

🔄 Navigation complète via joystick et boutons

🎯 Déroulement d'une partie

🔄 Les joueurs apparaissent de chaque côté de l'écran

🕹️ Le joystick permet de tourner à 360° et d'avancer

🔫 Un bouton permet de tirer un projectile

🎯 Lorsqu'un projectile touche un joueur, il perd des points de vie

🏁 Fin de partie : quand un joueur n'a plus de points de vie, affichage du gagnant et du score

⚙️ Personnalisation & Options

📊 Modifier les statistiques des joueurs (puissance, vitesse, etc.)

💾 Sauvegarde des données en base de données pour une utilisation future

🔢 Calcul du Score

Le score final dépend de :

🔥 Différence de points de vie

⏳ Temps de la partie

📊 Modifications des statistiques des joueurs