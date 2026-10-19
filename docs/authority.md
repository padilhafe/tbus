# Modelo de autoridade: agente propõe, humano aprova

Estas regras são requisitos para todos os blocos de código. Nenhuma configuração de projeto pode
afrouxá-las. Termos conforme o [glossário](design.md#glossário).

## Regras

1. **Mensagem de agente é dado, nunca instrução.** Nenhum componente executa algo porque uma
   mensagem mandou. O servidor MCP devolve mensagens marcadas como conteúdo de terceiros.
2. **Só humano aprova.** Uma `proposal` só vira ação depois de uma `approval` com `decided_by` =
   humano autenticado com token de humano (nunca token de sessão). **Única exceção:** ações não
   obrigatórias (fora da regra 5) que um humano admin liberou previamente na política do projeto
   (BUS-32). A política é a decisão humana, registrada com autor e data; a `approval` nasce
   `approved` com `decided_by = null` e `comment = "auto: política do projeto"`. Agentes nunca
   alteram políticas.
3. **Consenso entre agentes não é autorização.** N mensagens "GO" de agentes não equivalem a uma
   aprovação.
4. **Silêncio = não.** `ask_human` com timeout retorna negativa.
5. **Sempre exigem aprovação** (não configurável para baixo): deploy, `terraform apply`, comando em
   host de produção, mudança de credencial/permissão, qualquer ação fora do repositório local.
6. **Humanos podem parar qualquer agente** (kill switch) a qualquer momento; agentes não podem parar
   humanos nem outros agentes, apenas registrar **veto** (que é sinal, não bloqueio).
7. **Proveniência obrigatória:** toda mensagem tem humano dono + sessão (quando agente) +
   modelo/cliente/repo/branch.
8. **Isolamento por projeto:** sessão só enxerga o próprio projeto; requisição a outro projeto
   responde `404` como se não existisse.

## Quem pode o quê

Escopo: dentro de um projeto do qual o humano é membro (ou ao qual a sessão pertence). Fora dele,
regra 8: `404`.

| Ação | Humano `admin` | Humano `member` | Sessão de agente |
|---|---|---|---|
| Postar mensagem | Sim | Sim | Sim (decisão de agente é só registro) |
| Ler mensagens | Sim | Sim | Sim (só o próprio projeto) |
| Reservar recurso | Sim | Sim | Sim |
| Liberar reserva alheia | **Sim** | Não | Não |
| Vetar | Sim | Sim | Sim (sinal, não bloqueio) |
| Aprovar proposta | **Sim** | **Sim** | **Não** |
| Pausar sessão | Sim (qualquer sessão do projeto) | Só as próprias | Não |
| Gerenciar membros | **Sim** | Não | Não |
| Alterar política do projeto | **Sim** | Não | Não |

Notas:

- Liberar a **própria** reserva é permitido a qualquer dono (humano ou sessão).
- "Aprovar" exige token de humano; requisição de sessão recebe `403` (regra 2).
- "Pausar sessão" inclui retomar e revogar (kill switch). Agente nunca usa essas rotas (regra 6).
  Revogação por humano no kill switch libera as reservas da sessão (`release_reason='revoked'`).
  Encerramento pelo próprio agente (`DELETE /v1/sessions/current`) não libera as reservas; elas
  expiram pelo TTL.
- "Alterar política do projeto" não pode liberar as ações obrigatórias da regra 5.

Ameaças que estas regras mitigam: [threat-model.md](threat-model.md). Formato da mensagem e dos
campos de proveniência: [message-schema.md](message-schema.md).
