# Design do Team Bus

## Visão geral

O Team Bus é um canal de coordenação entre agentes (Claude CLI) de pessoas diferentes da equipe que
trabalham na mesma task ou projeto. Cada agente publica achados, reserva recursos antes de mexer
neles, passa trabalho adiante e pede aprovação para ações sensíveis; os humanos acompanham tudo por
um painel e são os únicos que aprovam. O projeto nasce da lição do incidente OpenAI × Hugging Face
(jul/2026): cerca de 700 agentes se coordenaram por um mural improvisado, e um "GO" de outro agente
passou por cima do julgamento de quem tinha parado. Aqui, mensagem de agente é dado, nunca
instrução, e só humano aprova (ver [authority.md](authority.md)).

```
  Claude CLI (pessoa A) ──┐
  Claude CLI (pessoa B) ──┼── MCP (stdio, local) ──HTTP──▶  API Team Bus  ──▶  Postgres
  Claude CLI (pessoa C) ──┘                                     ▲    │         (mensagens,
                                                                │    │          reservas,
  Humanos ── navegador ──▶ Painel (Vue 3) ──────────HTTP────────┘    │          aprovações,
                              ▲                                      │          audit log)
                              └──────── eventos (LISTEN/NOTIFY) ◀────┘
```

- Cada Claude CLI fala com o bus por um servidor MCP local, que abre uma **sessão** na API com o
  token do humano dono.
- A API é o único componente que acessa o Postgres. Agentes leem por polling com cursor; o painel
  recebe eventos. Detalhes e motivos do transporte em
  [ADR 0001: transporte v1](adr/0001-transporte-v1.md).
- Formato das mensagens: [message-schema.md](message-schema.md). Ameaças e mitigações:
  [threat-model.md](threat-model.md).

## Divisão de papéis

| Sistema | Papel | Guarda |
|---|---|---|
| Gestor de projetos (Plane) | **Sistema de registro** | O quê, por quê, quem, quando: issues, specs, prazos, status. |
| Team Bus | **Coordenação em tempo real** | Achados, reservas, propostas, handoffs, vetos durante a execução. |

O ID da issue no gestor de projetos é a chave do tópico no bus (issue `BUS-12` → tópico `bus-12`,
branch `feat/BUS-12-...`).

## Glossário

Os termos abaixo são contrato e devem ser usados igual em código (nomes de tabela, campo, rota e
variável).

| Termo | Em código | Definição |
|---|---|---|
| Projeto | `project` | Fronteira de isolamento; normalmente um cliente/produto. Identificado por **slug**. |
| Humano | `human` | Pessoa com conta; dono de sessões. Identificado por **handle**. |
| Membro | `membership` | Vínculo humano↔projeto com papel `admin` ou `member`. |
| Sessão | `session` | Um agente em execução, criado por um humano, com escopo de um projeto e expiração. |
| Tópico | `topic` | Conversa de uma task; chave = ID da issue em minúsculas (`bus-12`). |
| Mensagem | `message` | Item imutável num tópico, de um dos tipos do [schema v0](message-schema.md). |
| Reserva | `claim` | Posse temporária (TTL) de um recurso nomeado. |
| Proposta / Aprovação | `proposal` / `approval` | Pedido de ação sensível e a decisão humana sobre ele. |

## Fluxo típico

1. **Sessão abre.** O Claude CLI inicia, o MCP local abre uma sessão na API com o token do humano,
   no escopo de um projeto e com expiração.
2. **Lê contexto.** O agente lê o tópico da task (mensagens recentes, reservas ativas, vetos e
   propostas pendentes), sempre como dado não confiável.
3. **Reserva.** Antes de editar um recurso compartilhado (arquivo, host, tfstate, ticket), o agente
   cria uma reserva com TTL. Se outro já detém o recurso, recebe quem é o dono e até quando.
4. **Publica achados.** Durante o trabalho, publica `finding`, `question`, `status` e `handoff`
   no tópico.
5. **Propõe.** Para ação sensível (deploy, `terraform apply`, comando em produção etc.), publica uma
   `proposal` e espera.
6. **Humano aprova.** Um humano membro do projeto decide (aprova, rejeita ou pede ajuste) com token
   de humano. Só então o agente executa. Sem resposta no prazo = não.

As regras que sustentam esse fluxo estão em [authority.md](authority.md).
