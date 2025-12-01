# 🛡️ Guardians

**Role Glyphs & Guardianship — Pi Forge Quantum Genesis**

This document defines the roles, responsibilities, and code ownership within the Quantum Pi Forge.

---

## Guardian Roles

### 🔮 Quantum Architects
*Guardians of the lattice structure*

- **Responsibility**: Core architecture decisions, multi-app coordination
- **Scope**: `server/`, `config/`, Dockerfiles
- **Glyph**: `assets/glyphs/roles/guardian-architect.svg`

### ⚡ Resonance Engineers
*Keepers of the API flow*

- **Responsibility**: FastAPI endpoints, WebSocket handlers, authentication
- **Scope**: `server/main.py`, `api/`
- **Glyph**: `assets/glyphs/roles/guardian-engineer.svg`

### 🎨 Visualization Weavers
*Crafters of the visual experience*

- **Responsibility**: Flask dashboard, SVG generation, frontend integration
- **Scope**: `server/app.py`, `frontend/`, `assets/`
- **Glyph**: `assets/glyphs/roles/guardian-weaver.svg`

### 📿 Ethics Custodians
*Stewards of moral alignment*

- **Responsibility**: Gradio audit interfaces, ethical scoring, model evaluation
- **Scope**: `server/canticle_interface.py`, `src/`
- **Glyph**: `assets/glyphs/roles/guardian-custodian.svg`

---

## CODEOWNERS

```
# Quantum Architects - full repository oversight
* @onenoly1010

# Resonance Engineers - API and auth
/server/main.py @onenoly1010
/api/ @onenoly1010

# Visualization Weavers - dashboard and frontend
/server/app.py @onenoly1010
/frontend/ @onenoly1010
/assets/ @onenoly1010

# Ethics Custodians - audit and evaluation
/server/canticle_interface.py @onenoly1010
/src/ @onenoly1010

# Documentation
/docs/ @onenoly1010
```

---

## Team Structure

| Team                  | Members          | Primary Responsibility                |
|----------------------|------------------|--------------------------------------|
| Core Maintainers     | @onenoly1010     | Full repository access and oversight |
| Documentation        | Community        | Docs, guides, and examples           |
| Community            | Contributors     | Bug fixes, features, testing         |

---

## Becoming a Guardian

1. **Contribute**: Submit meaningful PRs that align with the covenant
2. **Review**: Participate in code reviews and discussions
3. **Resonate**: Demonstrate understanding of the mythic-operational balance
4. **Ascend**: Be nominated and approved by existing guardians

---

## Seals of Guardianship

*Signatories add their GitHub username and date when assuming guardianship*

| Guardian        | Role              | Date       |
|-----------------|-------------------|------------|
| @onenoly1010    | Quantum Architect | 2025-12-01 |

---

*"In guardianship, we find purpose. In purpose, we find resonance."*

*© 2025 Pi Forge Collective — Quantum Genesis Initiative*
