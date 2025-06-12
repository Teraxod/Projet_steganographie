# Projet_stéganographie
Projet de stéganographie d'étude

Objectif, creer un moteur de recherche steganographique sous forme de challenges avec des flags à cacher à ou trouver 


Différentes méthodes de stéaganographie sont disponible, l'utilisateur est libre de faire ce qu'il souhaite.

- Voici les étapes à suivre pour mettre en place le serveur.

  En prérequis, une machine linux fonctionnelle _(pour le projet nous avons utilisée une machine vituelle ubuntu **desktop**, la version **server** n'est pas obligatoire)_
  lien vers l'image ISO que nous avons utilisée : https://releases.ubuntu.com/releases/24.04.2/

1. Commencer par installer apache server sur une machine linux :
```bash
sudo apt update
sudo apt install apache2 -y
```

- Vérifier que le service Apache est actif : 
```bash
sudo systemctl status apache2
```

- S'il n'est pas actif : 
```bash
sudo systemctl start apache2
```

- Pour l'arrêter :
```bash
sudo systemctl stop apache2
```

- Pour le redémarrer : 
```bash
sudo systemctl restart apache2
```

- Si vous voulez que votre service apache se lance automatiquement au démarrage du système :
```bash
sudo systemctl enable apache2
```

- Pour désactiver le démarrage automatique de Apache2 au démarrage du système : 
```bash
sudo systemctl disable apache2
```

- Ensuite tu peux tester en tapant ton adresse local dans le navigateur et la page par défaut d'Apache2 devrait être affichée : 
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


2. Mise en place de **CGI**

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

- Vérifier que le dossier _/usr/lib/cgi-bin_ est bien utilisé, ce dossier est généralement déjà configuré par défaut dans le fichier :
```bash
/etc/apache2/conf-available/serve-cgi-bin.conf
```

- Placer un script dans /usr/lib/cgi-bin/ avec par exemple _test.py_ :
```bash
sudo nano /usr/lib/cgi-bin/test.py
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
Tu devrais voir : "**Script Python CGI fonctionne !**"


**Lorsque tout cela fonctionne, nous allons passer à l'étape suivante, celle qui nous permettra de mettre en place notre moteur de recherche stéganographique **
