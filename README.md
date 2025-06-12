# Projet_stéganographie
Projet de stéganographie d'étude

Objectif, creer un moteur de recherche steganographique sous forme de challenges avec des flags à cacher à ou trouver 


Différentes méthodes de stéaganographie sont disponible, l'utilisateur est libre de faire ce qu'il souhaite.

- Voici les étapes à suivre pour mettre en place le serveur.

  En prérequis :
  - Avoir une machine linux fonctionnelle _(pour le projet nous avons utilisée une machine virtuelle ubuntu **desktop**, la version **server** n'est pas obligatoire)_
  lien vers l'image ISO que nous avons utilisée : https://releases.ubuntu.com/releases/24.04.2/
  - Savoir utiliser un **CLI** linux
  - savoir utiliser un éditeur de texte en ligne de commande pour gagner du temps (nano,vim,etc)

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
- Ou depuis une autre machine du réseau : 
```bash
http://<adresse_ip_de_ta_machine>
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

- Vérifier que le dossier _/usr/lib/cgi-bin_ est bien utilisé, ce dossier est généralement déjà configuré par défaut dans le fichier, nous allons nous rendre dans _/etc/apache2/conf-available_  :
```bash
cd /etc/apache2/conf-available
```
- Puis faire un _**ls**_ :
```bash
ls
```
Et vous devriez touver un dossier qui s'appelle : _serve-cgi-bin.conf_

- Maintenant, placer un script dans /usr/lib/cgi-bin/ avec par exemple _mon_script.py_ :
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
Ton VS Code devrait se lancer.


**4. Mise en place du moteur de recherche stéganographique**

