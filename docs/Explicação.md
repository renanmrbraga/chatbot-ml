# Business Understanding

## Visão Geral
A empresa enfrenta desafios na integração de múltiplas fontes de dados internos (**PostgreSQL, MySQL, MongoDB, PDFs**) e externos (**APIs de portais públicos, agências reguladoras e bancos de dados governamentais**).
Essa falta de integração prejudica a eficiência do time comercial, que precisa de informações atualizadas para embasar propostas, identificar oportunidades e manter vantagem competitiva.

## Objetivos de Negócio
- **Reduzir tempo de pesquisa**: Minimizar horas gastas pelo time comercial na busca manual de dados sobre contratos e oportunidades.
- **Aumentar a assertividade em propostas**: Disponibilizar dados confiáveis e atualizados para embasar decisões e estratégias de pitch a potenciais clientes.
- **Gerar insights estratégicos**: Facilitar a identificação de oportunidades em infraestrutura, saneamento, energia, transportes, habitação, telecomunicações, mobilidade urbana, educação, saúde e meio ambiente.

### ROI Estimado
- **ROI Financeiro**: `[ESTIMATIVA DE LUCRO OU ECONOMIA FINANCEIRA]`
- **Economia de Tempo**: `[PERCENTUAL OU HORAS ECONOMIZADAS]`
- **Outros Benefícios Tangíveis**: `[MELHORIAS EM EFICIÊNCIA, VELOCIDADE DE DECISÕES, ETC.]`

## Perguntas de Negócio
1. **Onde encontrar contratos públicos ativos e planejados em uma região específica?**
2. **Quais políticos ou autoridades locais podem influenciar decisões de contratos ou projetos?**
3. **Quais são as principais lacunas de infraestrutura e saneamento em determinado município ou estado, e como a empresa pode abordar essas lacunas?**
4. **Quais indicadores de sucesso ou insucesso para projetos passados em regiões específicas, e como isso projeta oportunidades futuras?**

## Público-Alvo e Stakeholders
- **Equipe Comercial** → Acelera fechamento de negócios e identifica oportunidades.
- **Gerência Executiva** → Necessita de relatórios concisos sobre potencial de novos contratos.
- **Equipe de TI** → Responsável por segurança, integração dos dados e evolução contínua do chatbot.
- **Time de Planejamento e Inteligência de Negócios** → Utiliza o chatbot para análises profundas de risco e projeção de resultados.

## Priorização das APIs para Integração
Critérios de priorização:
✔ **Impacto Comercial** → Dados essenciais para negociações da empresa.
✔ **Disponibilidade e Atualização** → APIs com dados frequentes e acessíveis.
✔ **Facilidade de Implementação** → APIs REST bem documentadas e fáceis de integrar.

| Ordem | Área | API / Fonte | Uso no Chatbot |
|---------|--------|---------------|------------------|
| 1️⃣ | Contratos Públicos | Portal da Transparência | Informações sobre licitações e contratos em andamento. |
| 2️⃣ | Políticos Locais | TSE Dados Abertos | Informações sobre prefeitos, vereadores e governadores. |
| 3️⃣ | Saneamento Básico | SNIS | Cobertura de saneamento e indicadores municipais. |
| 4️⃣ | Infraestrutura e Transportes | DNIT | Obras rodoviárias e concessões de transporte. |
| 5️⃣ | Energia | ANEEL | Dados sobre concessões de energia e novas licitações. |
| 6️⃣ | Clima e Meio Ambiente | INMET | Clima e impactos ambientais para projetos. |
| 7️⃣ | Indicadores Econômicos | IBGE | Informações socioeconômicas e desenvolvimento regional. |

## Métricas de Sucesso (KPIs)
- **Tempo médio de resposta** do chatbot durante reuniões comerciais.
- **Aumento de propostas** geradas a partir de insights do chatbot (% ou número absoluto).
- **Redução do tempo** que a equipe comercial leva para encontrar dados críticos (em horas ou dias).
- **Índice de satisfação** do time comercial com o projeto (**pesquisa interna**).

## Restrições e Riscos
- **Confiabilidade dos dados** → Qualidade e frequência de atualização das fontes externas.
- **Integrações complexas** → Manter várias conexões com bases internas e APIs públicas pode aumentar a complexidade.
- **Adoção pelo time** → A mudança cultural de recorrer a um chatbot ao invés de métodos manuais pode levar tempo.
- **Outros Riscos** → `[POSSÍVEIS IMPACTOS LEGAIS, RISCOS DE SEGURANÇA DE DADOS, ETC.]`

## Alinhamento Estratégico
O projeto está diretamente vinculado à estratégia de crescimento da empresa em licitações e concessões públicas, melhorando a competitividade em propostas e o relacionamento com stakeholders políticos e técnicos.

## Fases, Prazos e Responsáveis
| Fase | Descrição | Prazo Estimado | Responsável |
|--------|-------------|----------------|----------------|
| **Fase 1: Pesquisa Interna** | Explorar os dados e verificar o que pode ser utilizado para melhorar a busca | `[Data]` | `[Responsáveis]` |
| **Fase 2: MVP** | Escolher bases de dados cruciais (Portal da Transparência, TSE) e configurar chatbot básico | `[Data]` | `[Responsáveis]` |
| **Fase 3: Teste Piloto** | Liberar o chatbot para uso em ambiente controlado e colher feedback | `[Data]` | `[Responsáveis]` |
| **Fase 4: Avaliação e Iteração** | Ajustar o modelo, melhorar integrações e planejar expansão para outras fontes de dados | `[Data]` | `[Responsáveis]` |
| **Fase 5: Expansão** | Integrar fontes adicionais (ANEEL, SNIS, etc.) e ampliar funcionalidades do chatbot | `[Data]` | `[Responsáveis]` |

## Plano de Comunicação
- **Status Reports** → `[Frequência]` com reuniões de acompanhamento.
- **Responsável por Comunicação** → `[Nome]` para consolidar informações e distribuir aos stakeholders.
- **Ferramentas** → `[Plataforma usada (Slack, Teams, e-mail, etc.)]`.
