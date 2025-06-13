# Projet_stéganographie
Projet de stéganographie d'étude

Objectif, creer un moteur de recherche steganographique sous forme de challenges avec des flags à cacher à ou trouver 


Différentes méthodes de stéaganographie sont disponible, l'utilisateur est libre de faire ce qu'il souhaite.

- Voici les étapes à suivre pour mettre en place le serveur.

  En prérequis :
  - Avoir une machine linux fonctionnelle _(pour le projet nous avons utilisée une machine virtuelle ubuntu **desktop**, la version **server** n'est pas obligatoire)_
  lien vers l'image ISO que nous avons utilisée : https://releases.ubuntu.com/releases/24.04.2/
  - Savoir utiliser un **CLI** linux (cd, ls, mv, etc...)
  - savoir utiliser un éditeur de texte en ligne de commande pour gagner du temps (nano, vim, etc...)

**1. Commencer par installer apache server sur une machine linux :**
```bash
sudo apt update
sudo apt install apache2 -y
```

- Vérifier que le service Apache est actif : 
```bash
sudo systemctl status apache2
```
S'il n'est pas actif : 
```bash
sudo systemctl start apache2
```
Pour l'arrêter :
```bash
sudo systemctl stop apache2
```
Pour le redémarrer : 
```bash
sudo systemctl restart apache2
```
Si vous voulez que votre service apache se lance automatiquement au démarrage du système :
```bash
sudo systemctl enable apache2
```
Pour désactiver le démarrage automatique de Apache2 au démarrage du système : 
```bash
sudo systemctl disable apache2
```

- Ensuite vous pouvez tester en tapant votre adresse ip local _(127.0.0.1)_ dans le navigateur et la page par défaut d'Apache2 devrait être affichée : 
```bash
http://localhost/
```
- Egalement avec votre adresse ip de la machine (votre page sera alors visible par vous et par une autre machine du même réseau) : 
```bash
http://<adresse_ip_de_ta_machine_serveur>
```

- Le répertoire Web par défaut est : 
```bash
/var/www/html/
```

- Vous pouvez réaliser un test simple avec une page personnalisée : 
```bash
echo "Hello World !" | sudo tee /var/www/html/index.html
```
_(Recharger la page web à chaque modification)_


**2. Mise en place de _CGI_**

Une fois que tout cela fonctionne, on va essayer de faire communiquer la page web avec un script python, pour ce faire, nous allons utiliser **CGI** (Common Gateway Interface) qui est l'interface de passerelle commune, ou CGI, est un ensemble de normes qui définissent la manière dont les informations sont échangées entre le serveur Web et un script personnalisé.

_(Le support CGI est déjà inclus dans Apache via un module appelé **mod_cgi**)_

- Activer le module **CGI**
```bash
sudo a2enmod cgi
```

- Redémarrer Apache :
```bash
sudo systemctl restart apache2
```

- Vérifier que le dossier _/usr/lib/cgi-bin_ est bien utilisé, ce dossier est généralement déjà configuré par défaut dans le fichier, nous allons donc nous rendre dans _/etc/apache2/conf-available_  pour vérifier qu'il est bien présent :
```bash
cd /etc/apache2/conf-available
```
- Puis faire un _**ls**_ :
```bash
ls
```
Et vous devriez touver un dossier qui s'appelle : _serve-cgi-bin.conf_

- Maintenant, placer un script dans _/usr/lib/cgi-bin/_ avec par exemple _mon_script.py_ :
```bash
sudo nano /usr/lib/cgi-bin/mon_script.py
```

- Contenu du script :
```bash
#!/usr/bin/env python3
print("Content-type: text/html\n")
print("<html><body><h1>Script Python CGI fonctionne !</h1></body></html>")
```  

- Rendre le script executable :
```bash
sudo chmod +x /usr/lib/cgi-bin/mon_script.py
```

- On peut accèder à notre script dans un navigateur :
```bash
http://localhost/cgi-bin/mon_script.py
```
Tu devrais voir apparaître sur ta page web : "**Script Python CGI fonctionne !**" 


Lorsque tout cela fonctionne, nous allons passer à l'étape suivante, celle qui nous permettra de mettre en place notre moteur de recherche stéganographique


**3. Installation d'un éditeur de code**

Nous allons commencer par installer un éditeur de code pour pouvoir y mettre nos pages **html** et nos scripts en **python**, ici nous avons ultilisé _**Visual Studio Code**_

- Pour commencer, nous allons installer les dépendances nécessaires :
```bash
sudo apt install wget gpg -y
```
- Ajouter la clé GPG de Microsoft :
```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/
```
- Ajouter le dépôt officiel VS Code :
```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] \
https://packages.microsoft.com/repos/vscode stable main" | \
sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
```
- Mettre à jour et installer VS Code :
```bash
sudo apt update
sudo apt install code -y
```
- Lance VS Code :
```bash
code
```
Votre VS Code devrait se lancer.


**4. Mise en place du moteur de recherche stéganographique**

Maintenant que nous avons tous les outils en main, il ne nous reste plus que la mise en place, pour cela nous allons télécharger les fichiers mis à disposition sur github :

- Soit vous téléchargé le dossier en format **zip** en cliquant sur "<> Code" en vert : 

![image](https://github.com/user-attachments/assets/09facc88-0b06-46fa-8268-f1629441cd35)

- Soit en le téléchargeant en ligne de commande, nous allons commencer par installer **_git_** :
```bash
sudo apt install git
```
- Une fois **_git_** installé, tapé cette commande sur votre **CLI** :
```bash
git clone https://github.com/Teraxod/Projet_steganographie.git
```
Cela va télécharger tous les dossiers à l'endroit où vous avez executé la commande.

- Ensuite, aller dans le dossier "Projet_steganographie"
- Une fois dans le dossier, nous allons déplacer chaque sous dossier dans son répertoire, le sous dossier "Code serveur" dans le répertoire _/var/www/html_ et le sous dossier "script" dans _/usr/lib/cgi-bin_

- Nous allons commencer par renommer notre dossier **'Code serveur'** en **Code_serveur** cela nous évitera par la suite d'obtenir des erreurs :
```bash
sudo mv 'Code serveur' Code_serveur
```

Pour ce faire, executer les commandes suivantes : 
```bash
sudo mv Code_serveur /var/www/html
```
et :
```bash
sudo mv script/ /usr/lib/cgi-bin/
```
Ensuite vérifié qu'ils aient bien été déplacés.

- Maintenant, nous voulons ouvrir ces 2 dossiers dans VS Code, sauf que ces 2 dossiers ne pourrons pas être ouvert depuis VS Code directement à cause des droits **root** où sont stockés nos fichier, on va donc commencer par ouvrir notre dossier fichier :


![image](https://github.com/user-attachments/assets/8ff9ebd4-dc0b-4b41-971a-d69b31ee868d)




Une fois ouvert vous serez à cette endroit : 


![image](https://github.com/user-attachments/assets/39e23986-223c-4b95-ba5f-4fbfab6ad34c)


Allez dans la barre de recherche et tapez ceci : /


![image](https://github.com/user-attachments/assets/d7bc8deb-abcf-47b2-8167-c68ffde0850c)




Une fois fait, vous aurez accés aux dossier stockés dans la racine, vous n'avez plus qu'à vous rendre dans le dossier qui nous intéresse dans _/var/www/html_  : 
```bash
/var/www/html
```
Vous verrez votre dossier "Code_serveur", selectionnez le dossier, puis faites clique droit "Ouvrir" ensuite "Ouvrir avec" et choissisez **VS Code**
Au moment de l'ouverture de **VS Code**, vous verrez une petite fenêtre comme ceci : 


![image](https://github.com/user-attachments/assets/864a33f1-592f-42ea-ad33-0d91d4e7e0c5)



Vous cliquez sur "Yes, I trust the authors"
Et vous aurez accès à tous les fichiers **html** et même le dossier **css**.

- Maintenant nous allons faire en sorte que nos pages s'affichent sur notre page web

Ouvre le fichier de configuration du site par défaut :
```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```
 Modifie la ligne :
 ```bash
DocumentRoot /var/www/html
```
en : 
```bash
DocumentRoot /var/www/html/Code_serveur
```

Enregistrer et fermer le fichier

Redémarre Apache :
```bash
sudo systemctl restart apache2
```

Maintenant, rendez sur votre page web et rafraichissez là et vous devriez voir apparaître ça : 


![image](https://github.com/user-attachments/assets/ffbe8874-8389-428a-9763-482527b53ae6)


