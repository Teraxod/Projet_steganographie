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

Relancer ensuite votre VS Code

- Pour être sûr qu'il n'y ait pas de problème de droit, nous allons taper ces commandes dans le terminal :
```bash
sudo chmod -R 755 /var/www/html/Code_serveur
sudo chown -R www-data:www-data /var/www/html/Code_serveur
```

Maintenant vous pouvez cliquer sur les liens et de nouvelles pages devront s'afficher (exemple avec le lien : cacher un mot dans une image) :





![image](https://github.com/user-attachments/assets/46dde51b-6da9-4274-93a9-70b2429409f8)


Nous avons bientôt fini, il ne nous manque plus qu'a faire intéragir notre serveur avec nos scripts en python 

- Pour commencer nous allons nous rendre dans le fichier _/etc/apache2/conf-available/serve-cgi-bin.conf_
C’est un fichier de configuration Apache (souvent dans /etc/apache2/conf-available/) qui contient les directives pour activer et gérer le dossier des scripts CGI.
```bash
sudo nano /etc/apache2/conf-available/serve-cgi-bin.conf
```

Vous allez avoir ça : 
```bash
<IfModule mod_alias.c>
    <IfModule mod_cgi.c>
        Define ENABLE_USR_LIB_CGI_BIN
    </IfModule>

    <IfModule mod_cgid.c>
        Define ENABLE_USR_LIB_CGI_BIN
    </IfModule>

    <IfDefine ENABLE_USR_LIB_CGI_BIN>
        ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
        <Directory "/usr/lib/cgi-bin">
            AllowOverride None
            Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
            Require all granted
        </Directory>
    </IfDefine>
</IfModule>
```
Et là vous allez ajouter ce : 
```bash
ScriptAlias /scripts/ /usr/lib/cgi-bin/scripts/
```
Il dit à Apache : “quand quelqu’un visite /scripts/..., cherche les fichiers dans /usr/lib/cgi-bin/scripts/”.

Et rajoutez ce bloc : 
```bash
<Directory "/usr/lib/cgi-bin/scripts">
    AllowOverride None
    Options +ExecCGI -Indexes +SymLinksIfOwnerMatch
    AddHandler cgi-script .py
    Require all granted
</Directory
```
Il autorise l'exécution des scripts _**.py**_ dans ce dossier (et ses sous-dossiers).

- Ce qui va vous donnez ceci : 
```bash
<IfModule mod_alias.c>
    <IfModule mod_cgi.c>
        Define ENABLE_USR_LIB_CGI_BIN
    </IfModule>

    <IfModule mod_cgid.c>
        Define ENABLE_USR_LIB_CGI_BIN
    </IfModule>

    <IfDefine ENABLE_USR_LIB_CGI_BIN>
        ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
        <Directory "/usr/lib/cgi-bin">
            AllowOverride None
            Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
            Require all granted
        </Directory>

        # 🎯 AJOUT POUR PRENDRE EN CHARGE /usr/lib/cgi-bin/scripts
        ScriptAlias /scripts/ /usr/lib/cgi-bin/scripts/
        <Directory "/usr/lib/cgi-bin/scripts">
            AllowOverride None
            Options +ExecCGI -Indexes +SymLinksIfOwnerMatch
            AddHandler cgi-script .py
            Require all granted
        </Directory>
    </IfDefine>
</IfModule>
```
- On va rendre tous les scripts exécutables :
```bash
sudo find /usr/lib/cgi-bin/script/ -type f -name "*.py" -exec chmod +x {} \;
```
- Assurer la bonne propriété des fichiers:
```bash
sudo chown -R www-data:www-data /usr/lib/cgi-bin/script/
```
- Redémarrer Apache pour appliquer la nouvelle config :
```bash
sudo systemctl reload apache2
```
- Tu peux tester en mettant ton script dans le navigateur :
```bash
http://<ton-ip-ou-domaine>/script/exiftool/cache_flag_exif.py
```
Ce qui va te renvoyer : 


![image](https://github.com/user-attachments/assets/ed8b8790-d84d-409d-807c-888cad175372)


- Maintenant testez directement dans la page web, en completant le formulaire (toujours sur le premier lien)
 Et on obtient ça :



![image](https://github.com/user-attachments/assets/a44fd16e-9bfb-422f-9b8f-664b88c5ebfd)

Avec la possiblité de téléchargée l'image et de revenir à l'accueil

Si cela fonctionne, votre serveur est fonctionnel !! 

Pour ouvrir votre dossier avec tous les scripts python, faites le de la même manière que pour ouvrir celui du **html**
Pour modifier vos fichiers sur VS Code que ce soit en **html** ou en **python**, vous devrez le faire en mode sudo, comme ceci : 

- Faire un _**CTRL+S**_ pour sauvegarder, puis vous aurez cet avertissement :



![image](https://github.com/user-attachments/assets/ba21c914-e1f4-4a33-8a09-121f9a3eeed9)


- Faites "Retry as sudo", puis entrez votre mot de passe **root**

- Pour savoir si votre fichier à été modifier et à besoin d'être sauvegardé, vous le verrez grâce à une petite pastille blanche à dans l'onglet à coté du nom du fichier :



![image](https://github.com/user-attachments/assets/712cff3c-2366-4004-91e3-cd879307a026)




