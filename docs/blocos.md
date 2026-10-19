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
| B06 | Servidor MCP | BUS-22, 23, 24 | B05 | — |
| B07 | Hooks do Claude Code | BUS-25, 26, 27 | B06 | — |
| B08 | Onboarding e dogfooding | BUS-28, 29 | B07 | — |
| B09 | Aprovações e notificação | BUS-30, 31, 32, 33 | B05 (B06 para `ask_human`) | — |
| B10 | Kill switch | BUS-34 | B04 | — |
| B11 | Painel: base | BUS-35, 36 | B05 | — |
| B12 | Painel: operação | BUS-37, 38, 39 | B11, B09 | — |
| B13 | Painel: controle e admin | BUS-40, 41, 42 | B11, B10 | — |
| B14 | Resumo vivo | BUS-43, 44 | B05 | — |
| B15 | Métricas e custo | BUS-45, 46 | B09, B14 | — |
| B16 | Conector Plane | BUS-47, 48, 49 | B05 | — |
| B17 | GitLab e spikes | BUS-50, 51 | B16 | — |
| B18 | Produção | BUS-52, 53, 54 | B13 | — |
| B19 | Piloto | BUS-55, 56 | B18 | — |

Paralelismo inicial: **B01 e B02 em paralelo**; depois B03 → B04 → B05 em sequência (contrato de
dados). Após B05, abrem em paralelo: B06, B09, B10, B11, B14, B16.
