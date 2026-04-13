# Guide de contribution — Ask SIO

Bienvenue sur Ask SIO ! Ce guide explique tout ce qu'il faut savoir pour contribuer proprement au projet.

---

## Table des matières

1. [Stratégie de branches](#-stratégie-de-branches)
2. [Convention de commits](#-convention-de-commits)
3. [Procédure de Pull Request](#-procédure-de-pull-request)
4. [Règles de code](#-règles-de-code)
5. [Workflow quotidien](#-workflow-quotidien)
6. [Résolution de conflits](#-résolution-de-conflits)
7. [FAQ](#-faq)

---

## Stratégie de branches

### Schéma général

```
main          ← PRODUCTION — code stable, déployé
│
dev           ← INTÉGRATION — code testé, prêt à merger dans main
├── feat/...  ← Nouvelles fonctionnalités
├── fix/...   ← Corrections de bugs
├── chore/... ← Config, dépendances, refacto
└── docs/...  ← Documentation
```

### Règles absolues 🚨

| Règle                            | Détail                                 |
| -------------------------------- | -------------------------------------- |
| Jamais de push direct sur `main` | Passe toujours par une PR              |
| Jamais de push direct sur `dev`  | Passe toujours par une PR              |
| Une branche = une tâche          | Chaque feature/fix a sa propre branche |
| PR revue par au moins 1 personne | Pas de merge sans review               |

### Nommage des branches

```
type/description-courte-en-kebab-case
```

| Type    | Usage                   | Exemple                |
| ------- | ----------------------- | ---------------------- |
| `feat`  | Nouvelle fonctionnalité | `feat/chat-component`  |
| `fix`   | Correction de bug       | `fix/jwt-expiry`       |
| `chore` | Config, deps, refacto   | `chore/setup-chromadb` |
| `docs`  | Documentation           | `docs/update-readme`   |
| `test`  | Ajout de tests          | `test/rag-pipeline`    |
| `style` | CSS/UI sans logique     | `style/sidebar-layout` |

---

## Convention de commits

Format : `type(scope): description courte en minuscules`

**Scopes disponibles :** `auth`, `chat`, `ingest`, `rag`, `agents`, `ui`, `db`, `ci`

### Exemples

```bash
feat(chat): add chat component with axios integration
feat(rag): implement pdf chunking and embedding pipeline
feat(agents): add librarian agent with chroma retrieval
fix(auth): resolve jwt token expiration on refresh
chore(deps): add langchain and chromadb to requirements
docs(readme): add api documentation section
test(rag): add unit tests for retriever module
style(ui): update sidebar active state
```

### Règles

- ✅ Description en **anglais**
- ✅ Verbe à **l'infinitif** (`add`, `fix`, `update`)
- ✅ **Minuscules** partout
- ✅ **Pas de point** à la fin
- ❌ Pas de message vague : `fix`, `update`, `wip` sont interdits

---

## Procédure de Pull Request

### Étape 1 — Créer ta branche depuis `dev`

```bash
git checkout dev
git pull origin dev
git checkout -b feat/ma-feature
```

### Étape 2 — Développer et committer

```bash
git status
git add src/components/MonComposant.tsx
git commit -m "feat(ui): add matiere card component"
git push origin feat/ma-feature
```

### Étape 3 — Ouvrir la PR sur GitHub

1. GitHub → Pull Requests → New Pull Request
2. Base : `dev` ← Compare : `feat/ma-feature`
3. Remplir le template de PR
4. Assigner l'autre membre comme reviewer
5. Submit

### Étape 4 — Après review

- Changements demandés → corriger sur la même branche puis push
- Approuvé → **Squash and Merge** dans `dev`
- Supprimer la branche après le merge

---

## Règles de code

### Python (Backend)

```python
# ✅ Toujours typer avec les annotations Python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    session_id: str

# ✅ Une route = un fichier router
# routers/chat.py
from fastapi import APIRouter
router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/")
async def chat(request: ChatRequest) -> ChatResponse:
    ...

# ✅ Variables d'environnement via pydantic-settings
# Jamais de clé API en dur dans le code
```

### TypeScript/React (Frontend)

```tsx
// ✅ Composants en PascalCase
// MatiereCard.tsx, ChatWindow.tsx

// ✅ Services Axios séparés des composants
// services/api.js
import axios from "axios";
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL });
export const sendMessage = (question) => api.post("/api/chat", { question });

// ✅ Jamais d'appel API directement dans un composant
```

### Nommage

| Élément          | Convention      | Exemple              |
| ---------------- | --------------- | -------------------- |
| Composants React | PascalCase      | `ChatWindow.tsx`     |
| Fichiers Python  | snake_case      | `librarian_agent.py` |
| Variables Python | snake_case      | `chroma_client`      |
| Constantes       | SCREAMING_SNAKE | `MAX_CHUNK_SIZE`     |

---

## Workflow quotidien

### Début de journée

```bash
git checkout dev
git pull origin dev
git checkout feat/ma-feature
git rebase dev
```

### Vérifier avant de PR

```bash
# Frontend
npm run lint
npm run build

# Backend
flake8 .           # lint Python
pytest             # tests
```

---

## Résolution de conflits

```bash
git checkout dev && git pull
git checkout feat/ma-feature
git rebase dev

# Résoudre les conflits dans les fichiers concernés
git add fichier-résolu.py
git rebase --continue

# Push force sur TA branche uniquement
git push origin feat/ma-feature --force-with-lease
```

---

## FAQ

**Q : J'ai commité sur `dev` directement.**
R : `git reset HEAD~1` pour défaire le commit (garde les fichiers), crée ta branche, recommit.

**Q : Comment annuler mon dernier commit ?**
R : `git reset HEAD~1` (garde les fichiers) ou `git reset --hard HEAD~1` (supprime tout).

**Q : Comment voir toutes les branches ?**
R : `git branch -a`

**Q : Je ne dois jamais commiter le dossier `chroma_db/` ?**
R : Exact, il est dans le `.gitignore`. Idem pour `venv/`, `.env`, et `__pycache__/`.
