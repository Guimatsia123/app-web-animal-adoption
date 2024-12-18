# inf3190-tp3-20243

## Description 
Ce document décrit le travail pratique 3 du cours [INF3190: Introduction a la programmation web](https://etudier.uqam.ca/cours?sigle=INF3190) au trimestre Automne 2024. 

## Auteur
MARIUS GUIMATSIA  AKALONG (GUIM27309006)

## Description
L'objectif est de concevoir une application web servant à offrir un animal de compagnie en adoption. L'adoption et la mise en adoption sont gratuites pour les utilisateurs.
## **Installation et Execution de l'application**
### Installation 
On prends pour acquis que Python, pip3, flask sont installés. Les lignes qui suivent indique juste comment configurer l'application. 
#### 1 :  Compilé le code python 
Se déplacé dans le dossier parent du projet et exécuter la commande suivante:
`python -m GUIM27309006.index`

#### 2 : Spécifier index.py comme le point d'entré de l'application  
Lancé la commande suivante  pour avec --app pour spécifier index.py comme point d'entré.
`flask --app index.py run`
####  3 : Définir la variable d’environnement FLASK_APP
`set FLASK_APP = index` 
####  4:  Lancer le serveur
`flask run` 
