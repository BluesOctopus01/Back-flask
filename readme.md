# Balto 🎓

Balto est une application de **Learning Card** développée en **Flask**.  
Ce projet constitue la partie **Back-End** réalisée dans le cadre de ma formation chez **Technofutur**.  
L’objectif est de fournir une API REST permettant de gérer des utilisateurs, des decks de cartes, des tags, ainsi que des sessions d’apprentissage avec statistiques.

---

## 🚀 Fonctionnalités principales

- **Gestion des utilisateurs**
  - CRUD complet (création, lecture, mise à jour, suppression)
  - Authentification par JWT
  - Rôles : `user` et `admin` (le premier utilisateur créé est admin)
  - Soft delete (désactivation) et hard delete (suppression définitive)

- **Gestion des decks**
  - Création, mise à jour et suppression
  - Association de tags
  - Accès public/privé via `access_key`

- **Gestion des cartes**
  - Types disponibles :
    - `QA` : Question / Réponse
    - `QCM` : Question à choix multiple (3 à 6 réponses possibles)
    - `Gapfill` : Texte à trou
    - `IMG` : Question avec image
  - CRUD complet par deck
  - Suppression par utilisateur ou admin

- **Gestion des tags**
  - Création, mise à jour et suppression (admin uniquement)
  - Consultation publique

- **Sessions d’apprentissage**
  - Création de session (user + deck)
  - Tirage de cartes aléatoires
  - Réponse aux cartes
  - Historique des sessions par utilisateur
  - Statistiques liées aux sessions
  - Gestion par admin (liste complète)

---

## 📂 Structure du projet

   ```bash
app/
│── configs/ #pour instancier les test dans une db fictive
│── controllers/ # Renvoie des HTTPS STATUS
│── DTO/ # Vérification des données fournis (card,deck,tag,user)
│── models/ # Modèles de données (SQLAlchemy)
│── routes/ #route (card,deck,session,tag,user)
│── services/ # Logique métier(card,deck,session,tag,user)
│── tests/ # test unitaires(init,deck,user)
│── utils/ # JWT,data_utils,verify_utils
─ main.py # Initialisation de l'application Flask

```

---

## 🔑 Routes principales

### 👤 Utilisateurs (`/users`)

- `POST /users/register` → Créer un utilisateur
- `POST /users/login` → Connexion
- `GET /users/profiles/<id>` → Récupérer un profil
- `GET /users/admin` → Liste des utilisateurs (admin)
- `PUT /users/update` → Mettre à jour son profil
- `PATCH /users/update/password` → Modifier son mot de passe
- `PATCH /users/delete` → Soft delete (user)
- `DELETE /users/delete/<id>` → Hard delete (admin)

### 🏷️ Tags (`/tags`)

- `POST /tags/` → Créer un tag (admin)
- `GET /tags/` → Liste des tags
- `GET /tags/<id>` → Récupérer un tag
- `PATCH /tags/<id>` → Modifier un tag (admin)
- `DELETE /tags/<id>` → Supprimer un tag (admin)

### 📚 Decks (`/decks`)

- `POST /decks/create` → Créer un deck
- `GET /decks/` → Liste des decks d’un utilisateur
- `GET /decks/<id>` → Récupérer un deck
- `PATCH /decks/<id>` → Modifier un deck
- `DELETE /decks/<id>` → Supprimer un deck
- `GET /decks/admin` → Liste des decks (admin)
- `DELETE /decks/admin/<id>` → Supprimer un deck (admin)

### 🃏 Cartes (`/decks/<deck_id>/cards`)

- `POST /decks/<deck_id>/cards` → Créer une carte
- `GET /decks/<deck_id>/cards` → Liste des cartes d’un deck
- `GET /decks/<deck_id>/cards/<card_id>` → Récupérer une carte
- `PATCH /decks/<deck_id>/cards/<card_id>` → Modifier une carte
- `DELETE /decks/<deck_id>/cards/<card_id>` → Supprimer une carte
- `GET /cards/` → Liste de toutes les cartes (admin)

### 🎯 Sessions (`/sessions`)

- `POST /sessions/decks/<deck_id>` → Créer une session
- `GET /sessions/` → Rejoindre une session active
- `GET /sessions/<id>` → Rejoindre une session par ID
- `GET /sessions/user/history` → Historique des sessions d’un utilisateur
- `GET /sessions/<id>/draw-card` → Tirer une carte
- `PATCH /sessions/<id>` → Mettre en pause une session
- `PATCH /sessions/<id>/cards/<card_id>/answer` → Répondre à une carte
- `DELETE /sessions/<id>` → Terminer une session
- `GET /sessions/admin` → Liste des sessions (admin)

---

## 🛠️ Technologies utilisées

- **Flask** (framework web Python)
- **SQLAlchemy** (ORM)
- **JWT** (authentification sécurisée)
- **Blueprints** (modularisation des routes)
- **Python 3.10+**

---

## ▶️ Installation & lancement

Pour installer et lancer le projet **Balto**, suivez les étapes ci-dessous :

1. **Cloner le projet**

   ```bash
   git clone https://github.com/ton-compte/balto.git
   cd balto
   ```

2. **Créer un environnement virtuel**

    ```bash
    python -m venv venv
    venv\Scripts\activate #Windows
    ```

3. **Installer les dépendances**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurer les variables d’environnement**

    Créez un fichier .env à la racine du projet (non inclus dans Git) avec vos paramètres :

    ```bash
    SECRET_KEY=secret_key
    DATABASE_URL=postgresql://user:password@localhost:5432/balto 
    ```

5. **Démarrer le serveur**

    ```bash
    python main.py
    ```

## 💹 Point d'amélioration

- Utiliser des middlewear pour éviter les répétitions inutiles de codes
