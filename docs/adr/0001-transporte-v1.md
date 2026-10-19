# ADR 0001: transporte v1 (Postgres LISTEN/NOTIFY + polling)

- **Status:** aceito
- **Issue:** BUS-11

## Contexto

O Team Bus precisa entregar mensagens novas de um tópico a agentes (Claude CLI via MCP) e ao painel
dos humanos. Na v1 o volume esperado é baixo (dezenas de agentes) e a operação é feita por uma
pessoa. Toda mensagem precisa ser gravada junto com sua linha de auditoria, de forma atômica
(ver [design.md](../design.md)).

## Decisão

A v1 usa **só Postgres**.

- **Agentes** leem por **polling com cursor** (`since=<seq>`), onde `seq` é `bigserial` monotônico
  de `messages`.
- **Painel (M4)** recebe notificações via `LISTEN/NOTIFY` no canal `teambus_events` com payload
  JSON:

  ```json
  {"project": "<slug>", "topic": "<key>", "seq": <n>}
  ```

  O payload é pequeno de propósito; o cliente busca a mensagem pela API.

## Por quê

- Um componente a menos para operar.
- Volume esperado baixo (dezenas de agentes).
- Transação única para mensagem + auditoria (+ `NOTIFY`, que só é entregue no commit).

## Consequências

- Latência de polling (2–5 s) aceitável.
- `NOTIFY` não garante entrega, então o cliente **sempre reconcilia por `since`**: o evento é só
  um aviso para buscar; a fonte da verdade é a leitura por cursor.

## Gatilhos de revisão

Migrar para **NATS JetStream** (v2) quando ocorrer qualquer um:

- mais de 200 sessões simultâneas;
- mais de 50 msg/s sustentado;
- necessidade de multi-região.
