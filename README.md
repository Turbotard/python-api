# Projet Python avec API 

Ce projet est une application Python qui nécessite un environnement virtuel pour fonctionner correctement. Suivez les étapes ci-dessous pour configurer l'environnement virtuel et lancer le projet.

## Installation de FastAPI 

Pour installer FastAPI il faut taper la commande suivante :

pip install fastapi[all]

Puis :

pip install uvicorn

## Configuration de l'environnement virtuel

Pour créer l'environnement virtuel, suivez ces étapes :

1. Ouvrez un terminal dans le répertoire de ce projet.

2. Utilisez la commande suivante pour créer un environnement virtuel nommé "env" : $ python -m venv env

## Lancement du projet

Après avoir configuré l'environnement virtuel et installé les dépendances, vous pouvez lancer le projet avec uvicorn en utilisant la commande suivante :

uvicorn main:app --reload

