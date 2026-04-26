# CLAUDE.md

This file provides context and conventions for AI assistants (Claude Code and others) working in this repository.

## Repository Status

Repositório de trabalho do projeto **Legal One** (Andersen Ballão Advocacia,
Departamento Tributário). Cobre a gestão de horas no Legal One/Novajus em duas
camadas complementares:

- **`docs/kit_v2/`** — espelho em Markdown do Kit Documental v2.0
  (`KIT-LEGALONE-2026-V2`, data-base 12/04/2026): POP, PB01–PB09, README de
  carregamento, fluxograma. PDFs originais versionados ao lado dos `.md`.
  Conteúdo marcado como **uso interno restrito** — manter este repositório
  privado.
- **`legalone_robot_v1/`** — robô determinístico Python/Selenium para a
  **Fase 1 (lançamento primário)** do POP. Lê planilha XLSX, valida e dispara
  navegação assistida no Legal One.

- **Remote**: `dinizadv/claude-` on GitHub (privado)
- **Primary development branch**: `claude/analyze-legal-one-project-VR7f0`

### Como usar o Kit como contexto

Combinações mínimas por tipo de tarefa estão em
`docs/kit_v2/04_Contexto_Referencia/README_Carregamento_de_Contexto_LegalOne_v2_0.md`.
Resumo:

| Tarefa | Leitura mínima |
|---|---|
| Reconstrução linha a linha | PB01 + PB02 + PB03 + PB04 + PB05 |
| Triagem, aprovação e devolução | POP + PB02 + PB03 + PB04 + PB05 + PB06 |
| Auditoria mensal | POP + PB06 + PB07 + PB09 |
| Rollout | POP + PB06 + PB08 |

---

## Development Workflow

### Branch Strategy

- All feature work happens on dedicated branches, not directly on `main`.
- Branch names follow the pattern: `<owner>/<short-description>-<id>` (e.g., `claude/add-feature-abc123`).
- Push with tracking: `git push -u origin <branch-name>`.
- Do **not** create pull requests unless explicitly requested by the user.

### Committing

- Write clear, descriptive commit messages that explain *why*, not just *what*.
- Prefer small, focused commits over large batches.
- Never use `--no-verify` or skip hooks unless explicitly instructed.
- Never amend published commits; create new ones instead.

### Git Safety Rules

- Never force-push to `main` or `master`.
- Never run destructive commands (`reset --hard`, `clean -f`, `branch -D`) without explicit user confirmation.
- Never commit secrets, credentials, or `.env` files.

---

## Code Conventions (to be updated as the project evolves)

As the codebase grows, document the following here:

### Language & Runtime
- [ ] Primary language(s) and version(s)
- [ ] Runtime environment (Node.js, Python, etc.)
- [ ] Package manager (npm, yarn, pnpm, pip, poetry, etc.)

### Project Structure
- [ ] Source directory layout
- [ ] Where tests live
- [ ] Where configuration files live

### Style & Linting
- [ ] Linter and formatter in use (ESLint, Prettier, Ruff, Black, etc.)
- [ ] How to run lint: `<command>`
- [ ] How to auto-fix: `<command>`

### Testing
- [ ] Test framework in use
- [ ] How to run tests: `<command>`
- [ ] Where test fixtures and mocks live

### Build & Run
- [ ] How to install dependencies: `<command>`
- [ ] How to run the project locally: `<command>`
- [ ] How to build for production: `<command>`

---

## AI Assistant Guidelines

### General Principles

- Read files before editing them — never modify code you haven't read.
- Prefer editing existing files over creating new ones.
- Make only the changes necessary for the current task — no unsolicited refactoring, no extra features.
- Do not add comments or docstrings to code you didn't change.
- Do not introduce speculative abstractions or future-proofing.

### Security

- Never introduce SQL injection, XSS, command injection, or other OWASP Top 10 vulnerabilities.
- Never commit secrets or credentials.
- Validate input only at system boundaries (user input, external APIs) — trust internal code.

### Risky Actions (always confirm before proceeding)

- Deleting files, branches, or database tables
- Force-pushing, hard resets, or amending published commits
- Pushing to remote repositories
- Opening, closing, or commenting on PRs/issues
- Sending messages to external services

### Tool Preferences

- Use dedicated tools (Read, Edit, Grep, Glob, Write) over raw Bash equivalents.
- Use Bash only for operations that require shell execution.
- Run independent tool calls in parallel to maximize efficiency.

---

## Updating This File

When the project structure is established, update the sections above with:
1. Actual language, runtime, and toolchain details
2. Real commands for lint, test, build, and run
3. Any project-specific conventions discovered in the codebase
4. Links to additional documentation (architecture docs, ADRs, API specs, etc.)
