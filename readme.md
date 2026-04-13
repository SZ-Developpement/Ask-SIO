# Ask SIO

> Plateforme d'apprentissage par IA générative (RAG Multi-Agents), dédiée aux étudiants BTS SIO.

![Status](https://img.shields.io/badge/status-en%20développement-yellow)
![React](https://img.shields.io/badge/React-18-blue?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--db-orange)
![License](https://img.shields.io/badge/licence-MIT-green)

---

## Sommaire

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Stack technique](#-stack-technique)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)
- [API](#-api)
- [Équipe](#-équipe)

---

## À propos

**Ask SIO** est une plateforme d'apprentissage intelligente conçue pour les étudiants BTS SIO (SLAM & SISR). Elle permet d'importer des ressources pédagogiques (PDF, cours) et d'interroger un système d'IA qui répond en citant précisément ses sources.

Le projet repose sur une architecture **RAG (Retrieval-Augmented Generation)** couplée à un système **multi-agents** collaboratifs pour garantir des réponses fiables et adaptées au référentiel BTS SIO.

---

## Fonctionnalités

- **Import de documents** — PDF de cours, fiches, TP vectorisés automatiquement
- **Chat en langage naturel** — pose tes questions comme à un professeur
- **Réponses sourcées** — chaque réponse cite le document et la page source
- **Multi-agents IA** — Le Bibliothécaire, Le Professeur, Le Vérificateur
- **Authentification sécurisée** — JWT via FastAPI
- **Outils utilitaires** — calculateur de moyenne, convertisseur de bits, etc.

---

## Stack technique

| Couche           | Technologie                      |
| ---------------- | -------------------------------- |
| Frontend         | React 18, Vite TypeScript, Axios |
| Backend          | Python 3.12, FastAPI             |
| Base vectorielle | ChromaDB                         |
| Orchestration IA | LangChain, LangGraph             |
| Auth             | JWT (python-jose)                |
| DevOps           | Docker, GitHub Actions           |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React 18 + Vite                    │
│   Sidebar | Chat | Import PDF | Outils              │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / Axios
┌──────────────────────▼──────────────────────────────┐
│                 FastAPI (Python 3.12)               │
│   /api/ingest | /api/chat | /api/auth               │
└──────┬──────────────────────────┬───────────────────┘
       │                          │
┌──────▼──────┐         ┌────────▼────────────────────┐
│  ChromaDB   │         │    Multi-Agents (LangGraph) │
│  Vecteurs   │         │                             │
│  PDF/cours  │         │  Agent A — Bibliothécaire   │
└─────────────┘         │  Agent B — Professeur       │
                        │  Agent C — Vérificateur     │
                        └─────────────────────────────┘
```

### Flux RAG

```
PDF importé
    │
    ▼
Chunking (découpage)
    │
    ▼
Embeddings (vectorisation)
    │
    ▼
Stockage ChromaDB
    │
    ▼
Question utilisateur → Recherche vectorielle → Contextes extraits
    │
    ▼
LLM (OpenAI/Anthropic) + Contextes → Réponse sourcée
```

---

## Installation

### Prérequis

- Node.js >= 20
- Python 3.12
- Docker (recommandé)
- Clé API OpenAI ou Anthropic

### 1. Cloner le projet

```bash
git clone https://github.com/SZ-Developpement/Ask-SIO.git
cd Ask-SIO
```

### 2. Variables d'environnement

```bash
# Backend
cp apps/backend/.env.example apps/backend/.env

# Frontend
cp apps/frontend/.env.example apps/frontend/.env
```

Remplir les variables :

```env
# apps/backend/.env
OPENAI_API_KEY="sk-..."
JWT_SECRET="votre_secret_jwt"
CHROMA_PATH="./chroma_db"
```

```env
# apps/frontend/.env
VITE_API_URL="http://localhost:8000"
```

### 3. Démarrage avec Docker (recommandé)

```bash
docker-compose up -d
```

### 4. Démarrage manuel

```bash
# Backend
cd apps/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (dans un autre terminal)
cd apps/frontend
npm install
npm run dev
```

L'app sera disponible sur `http://localhost:5173`
La doc API sur `http://localhost:8000/docs` (Swagger auto-généré)

---

## Structure du projet

```
Ask-SIO/
├── apps/
│   ├── frontend/              # React 18 + Vite
│   │   ├── src/
│   │   │   ├── components/    # Composants React
│   │   │   ├── pages/         # Pages de l'app
│   │   │   ├── hooks/         # Custom hooks
│   │   │   ├── services/      # Appels API (Axios)
│   │   │   └── utils/         # Fonctions utilitaires
│   │   ├── .env.example
│   │   └── package.json
│   │
│   └── backend/               # FastAPI Python
│       ├── routers/           # Routes API
│       │   ├── auth.py        # Authentification JWT
│       │   ├── ingest.py      # Import et vectorisation PDF
│       │   └── chat.py        # Endpoint chat multi-agents
│       ├── agents/            # Agents LangGraph
│       │   ├── librarian.py   # Agent A — Bibliothécaire
│       │   ├── professor.py   # Agent B — Professeur
│       │   └── verifier.py    # Agent C — Vérificateur
│       ├── rag/               # Pipeline RAG
│       │   ├── ingest.py      # Chunking + Embeddings
│       │   └── retriever.py   # Recherche vectorielle
│       ├── chroma_db/         # Base vectorielle locale
│       ├── main.py            # Point d'entrée FastAPI
│       ├── requirements.txt
│       └── .env.example
│
├── .github/
│   ├── workflows/             # CI/CD GitHub Actions
│   └── ISSUE_TEMPLATE/        # Templates issues
├── docs/                      # Documentation technique
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## API

| Méthode | Endpoint             | Description                                    |
| ------- | -------------------- | ---------------------------------------------- |
| `POST`  | `/api/auth/register` | Créer un compte                                |
| `POST`  | `/api/auth/login`    | Connexion, retourne JWT                        |
| `POST`  | `/api/ingest`        | Import PDF + vectorisation                     |
| `POST`  | `/api/chat`          | Envoyer une question, recevoir réponse sourcée |

Documentation interactive disponible sur `/docs` (Swagger) et `/redoc`.

---

## Équipe

| Membre                                      | Rôle                                               |
| ------------------------------------------- | -------------------------------------------------- |
| [Alexis](https://github.com/FlytziTv)       | Backend RAG & ChromaDB + Composant Chat & Axios    |
| [Thomas](https://github.com/thomas-montout) | Auth JWT & FastAPI Routes + Gestion d'état & UI/UX |

---

## Licence

MIT — voir [LICENSE](./LICENSE)
