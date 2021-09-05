# ero1

Tuto installation OSMnx :

1. Installer la dernière version de Pycharm Pro (gratuit avec la license d'EPITA)

2. Ouvrir/creer n'importe quel projet

3. Si dans la barre des menus, il y a un onglet "Git", passer à l'étape 5, sinon continuer

4. Cliquer sur l'onglet "VCS" -> "Enable Version Control Integration", sélectionner "Git" dans le menu déroulant, puis OK

5. Dans l'onglet "Git", sélectionner "Clone...", puis "GitHub" dans la barre à gauche, "Login via GitHub" et se connecter à GitHub

6. Une fois connecté, sélectionner la repo "Bugul/ero1" puis "Clone". Un nouveau projet devrait être créer.

7. Bien vérifier que dans "File" -> "Settings..." -> "Project: ero1" -> "Python Interpreter", l'interpreteur soit de type Conda.

8. Ouvrir la console Python de Pycharm, en bas

9. Entrer cette commande : conda config --prepend channels conda-forge

10. Puis entrer celle ci : conda create -n ox --strict-channel-priority osmnx -y

11. Une fois l'installation terminée, retourner dans "File" -> "Settings..." -> "Project: ero1" -> "Python Interpreter", cliquer sur la roue crantée à gauche du menu déroulant puis "Add..." -> "Conda Environment" -> "Existing environment", cliquer sur les 3 petits points à gauche d'"Interpreter", naviguer jusqu'au répertoire d'installation de votre conda, puis sélectionner "envs/ox/python.exe"

12. Après avoir validé, vous pouvez descendre la liste des package dispo pour voir si osmnx est bien présent.

13. Cliquer sur "Apply" puis "OK", puis "Add Configutation..." en haut à droite
\n
14. Cliquer sur "Add new run configuration..." -> Python, nommer la config comme souhaité, dans "Script path:" choisir le script voulu (par exemple test.py), puis Python interpreter, sélectionner "Python X.Y (ox)" puis "Apply" -> "OK"

# Lancer le script

Il suffit de lancer snow.py, l'itinéraire du drone sera enregistré dans drone_path.txt et celui de la déneigeuse dans snow_path.txt
