# Mapa de blocos

Cada bloco = um agente, uma branch `bloco/Bxx-<slug>`, um PR para `main` (merge só pelo Felipe). Issues no Plane (projeto `BUS`)
carregam a label do bloco. "Depende de" = blocos que precisam estar `Feito` antes de começar.

| Bloco | Nome | Issues | Depende de | Spec |
|---|---|---|---|---|
| B01 | Fundação do repositório | BUS-13 | — | ✅ |
| B02 | Design e autoridade (docs) | BUS-8, 9, 10, 11, 12 | — | ✅ |
| B03 | Persistência + harness de testes | BUS-14, 15, 21 | B01 | ✅ |
| B04 | Auth e isolamento | BUS-16, 20 | B03 | ✅ |
| B05 | Mensagens, reservas e filtro de segredos | BUS-17, 18, 19 | B04 | ✅ |
| B06 | Servidor MCP | BUS-22, 23, 24 | B05 | ✅ |
| B07 | Hooks do Claude Code | BUS-25, 26, 27 | B06 | — |
| B08 | Onboarding e dogfooding | BUS-28, 29 | B07 | — |
| B09 | Aprovações e notificação | BUS-30, 31, 32, 33 | B05, B06 | ✅ |
| B10 | Kill switch | BUS-34 | B05 | ✅ |
| B11 | Painel: base | BUS-35, 36 | B05 | ✅ |
| B12 | Painel: operação | BUS-37, 38, 39 | B11, B09 | — |
| B13 | Painel: controle e admin | BUS-40, 41, 42 | B11, B10 | — |
| B14 | Resumo vivo | BUS-43, 44 | B06 | ✅ |
| B15 | Métricas e custo | BUS-45, 46 | B09, B14 | — |
| B16 | Conector Plane | BUS-47, 48, 49 | B06, B09 (B14 opcional) | ✅ |
| B17 | GitLab e spikes | BUS-50, 51 | B16 | — |
| B18 | Produção | BUS-52, 53, 54 | B13 | — |
| B19 | Piloto | BUS-55, 56 | B18 | — |

## Ondas de execução

1. **B01 + B02** em paralelo.
2. **B03 → B04 → B05** em sequência (contrato de dados).
3. Após B05: **B06, B10, B11** em paralelo.
4. Após B06: **B09, B14** em paralelo.
5. Após B09: **B16**.

## Recursos reservados (evita conflito entre blocos paralelos)

| Migration | Bloco |
|---|---|
| `0001_core.sql`, `0002_audit.sql` | B03 |
| `0003_approvals.sql` | B09 |
| `0004_web_logins.sql` | B11 |
| `0005_summaries.sql` | B14 |
| `0006_integrations.sql` | B16 |

O runner aplica toda migration ainda não registrada, então a ordem de merge entre blocos paralelos
não importa, desde que cada bloco use só o número reservado. Novas ações de auditoria e variáveis
de ambiente ficam declaradas na spec de cada bloco.
