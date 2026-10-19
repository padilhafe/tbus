# Team Bus

Produto próprio: canal de coordenação entre agentes (Claude CLI) de membros diferentes da equipe,
compartilhando contexto de uma task/projeto. Inspirado no incidente OpenAI × Hugging Face (jul/2026),
onde ~700 agentes se coordenaram por um mural improvisado no cache de pacotes.

## Princípios (não negociáveis)

- **Mensagem de agente é dado, nunca instrução.** Agente propõe; só humano aprova.
- Proveniência obrigatória em toda mensagem (humano dono, sessão, modelo, repo).
- Escopo por projeto: agente de um cliente nunca lê o canal de outro.
- Reservas (claims) sempre com TTL. Ações com efeito externo exigem `ask_human`.
- Audit log append-only. Filtro de segredos na entrada.

## Arquitetura

- **Gestor de projetos (Plane)** = sistema de registro (o quê, por quê, quem, quando).
- **Team bus** = coordenação em tempo real (achados, reservas, propostas, handoffs).
- Stack: Python (FastMCP + FastAPI) + Postgres (LISTEN/NOTIFY na v1; NATS na v2) + painel Vue 3.
- ID da issue no Plane = chave do tópico no bus (branch `feat/BUS-12-...`).

## Plane local (gestão deste projeto)

- `dev/plane/plane-app/` — compose + `plane.env` (v1.4.2). UI em `http://127.0.0.1:8090`
  (admin em `/god-mode`). Dados em volumes nomeados do Docker, **não** nesta pasta (Proton Drive).
- Subir/parar: `cd dev/plane/plane-app && docker compose --env-file plane.env up -d` / `down`.
- Workspace `bus`, projeto `BUS`. Marcos = Modules M0–M7.
- API key em `~/.zshrc_exports/team-bus.env` (`PLANE_API_KEY`), consumida pelo `.mcp.json`.
- Plano de origem: `~/.claude/plans/docker-est-aonline-sobe-jiggly-locket.md`.
- Futuro: migrar para a VPS do hub (ver `../hub/PLANO.md`, Fase 6).

## Como agentes trabalham neste repo (LER ANTES DE CODAR)

Trabalho é entregue **por bloco** (label `Bxx` no Plane, projeto `BUS`). Cada bloco = um agente,
uma branch, uma entrega. A **spec de cada issue no Plane é a fonte da verdade**; mapa de blocos e
dependências em `docs/blocos.md`.

1. **Antes de começar:** ler todas as issues do bloco + as dependências listadas. Se uma dependência
   não estiver `Feito`, **não comece**: comente na issue e pare.
2. **Repo:** `github.com/padilhafe/tbus` (**público**: nada de dado de cliente, IP interno ou
   segredo). Partir sempre da `main` atualizada (`git pull`).
   **Branch:** `bloco/Bxx-<slug>` (ex.: `bloco/B03-persistencia`). Commits: `BUS-<n>: <resumo>`.
   **Agentes em paralelo** usam `git worktree` (um diretório por bloco), nunca a mesma pasta.
3. **Entrega = 1 PR por bloco** para `main` (`gh pr create`), título `Bxx: <nome do bloco>`, corpo
   com issues cobertas, critérios de aceite marcados e como testar. **Agente nunca faz merge**:
   quem aprova e mergeia é o Felipe (mesmo princípio do produto: agente propõe, humano aprova).
   **Plane:** mover as issues do bloco para `Em andamento` ao começar e `Em review` ao abrir o PR,
   comentando o link do PR. O Felipe move para `Feito` após o merge.
4. **Contratos são fixos.** Schema, rotas, nomes de módulo, códigos de erro e variáveis de ambiente
   definidos em spec de outro bloco **não podem ser alterados**. Se precisar mudar, pare e comente
   na issue explicando o porquê. Nunca "conserte" o contrato por conta própria.
5. **Definition of Done (todo bloco):** `make lint` e `make test` verdes; critérios de aceite da
   spec marcados no comentário final; docs atualizadas se o bloco mudou comportamento visível;
   nenhum segredo em código, teste ou fixture (use valores obviamente falsos).
6. **Fora do escopo é fora do escopo.** Não implemente itens de outros blocos, mesmo que pareça
   fácil. Se achar algo faltando, comente na issue.
7. **Nunca** tocar em produção, no Plane de outros clientes, nem no `dev/plane/` (Plane local).
