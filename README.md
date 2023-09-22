# Projet Python avec API du Groupe 3

Bienvenue dans le projet Python avec API du **Groupe 3**! Suivez le guide ci-dessous pour configurer votre environnement et lancer le projet.

## 🚀 Mise en place

### Pré-requis

- Avoir Python d'installé sur votre machine
- Ouvrir un terminal dans le répertoire du projet

### 📦 Installation de FastAPI

FastAPI est un cadre moderne et performant pour construire des API avec Python basé sur des annotations de type standard.

\```bash
pip install fastapi[all]
pip install uvicorn
\```

### 🌍 Configuration de l'environnement virtuel

Un environnement virtuel est un espace isolé où vous pouvez installer des paquets indépendamment de ceux installés globalement sur votre système. Ceci est pratique pour éviter les conflits entre les versions.

Pour configurer l'environnement virtuel :

1. Créez l'environnement virtuel avec le nom "env" :
\```bash
python -m venv env
\```
2. Activez l'environnement virtuel. La méthode dépend de votre système d'exploitation :

   - **Windows** : `.\env\Scripts\activate`
   - **macOS/Linux** : `source env/bin/activate`

### 🚴 Lancement du projet

Une fois que vous avez configuré l'environnement virtuel et installé toutes les dépendances, vous pouvez lancer l'application.

\```bash
uvicorn main:app --reload
\```

Avec cette commande, vous lancerez le serveur de développement qui se rechargera automatiquement à chaque modification du code.

---

## 👥 Membres du Groupe 3

- **Benjamin Tisserand**
- **Eloi Tranchant**
- **Paul Rivallin**

---

Merci de contribuer et d'utiliser notre projet! Si vous avez des questions ou des préoccupations, n'hésitez pas à nous contacter.
