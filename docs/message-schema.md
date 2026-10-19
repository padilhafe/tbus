# Schema de mensagens v0

Contrato implementado pela API (B05) e pelo servidor MCP (B06). Termos conforme o
[glossário](design.md#glossário); regras de autoridade em [authority.md](authority.md).

## Tipos (`type`)

Todos imutáveis depois de gravados.

| `type` | Significado |
|---|---|
| `finding` | Fato descoberto ("a migration X quebra o serviço Y"). |
| `decision` | Decisão registrada. Se `author.kind = "agent"` é só registro de algo decidido por humano fora do bus; não tem efeito. |
| `handoff` | Passagem de trabalho para outra pessoa/agente, com estado atual e próximos passos. |
| `question` | Pergunta aberta para qualquer participante. |
| `proposal` | Pedido de ação que exige aprovação humana (fluxo completo no B09). |
| `status` | Progresso/resumo de sessão. |
| `veto` | Objeção a outra mensagem; exige `ref`. |

## Formato de leitura

JSON devolvido pela API:

```json
{
  "id": "uuid",
  "seq": 123,
  "project": "bus",
  "topic": "bus-12",
  "type": "finding",
  "body": "texto, até 16384 bytes UTF-8",
  "ref": "uuid | null",
  "meta": {"objeto JSON livre, até 8192 bytes serializado"},
  "author": {
    "kind": "agent | human",
    "human": "felipe",
    "session": "uuid | null",
    "model": "claude-opus-5-5 | null",
    "client": "claude-code | null",
    "repo": "team-bus | null",
    "branch": "bloco/B03-persistencia | null"
  },
  "created_at": "2026-10-19T14:00:00Z"
}
```

- `seq`: cursor monotônico usado na leitura por polling (`since=`); ver
  [ADR 0001](adr/0001-transporte-v1.md).
- `author`: proveniência obrigatória (regra 7 de [authority.md](authority.md)).

## Formato de escrita

```
{"type", "body", "ref"?, "meta"?}
```

Autor e proveniência **nunca** vêm do cliente; o servidor preenche a partir do token.

## Regras

- `veto` exige `ref` para mensagem do **mesmo tópico**.
- `ref` em outros tipos é opcional e precisa existir no **mesmo projeto**.
