
# Seção de Avaliação

## 1. Introdução
- **Objetivo**: Explique que a seção avalia a eficácia da abordagem proposta em cenários simulados representando diferentes incertezas, com foco em:
  - Cumprimento das tarefas sob constraints.
  - Escolha do melhor componente.
  - Impacto de diferentes pesos e configurações no desempenho.
- **Estrutura**: Resuma como a seção está organizada:
  1. Configuração experimental: descrição dos cenários, atributos simulados e métodos.
  2. Resultados e discussão por RQs consolidadas.
  3. Comparação com trabalhos relacionados.
  4. Limitações e ameaças à validade.

## 2. Configuração Experimental
### 2.1 Descrição dos Cenários
- Liste as cinco incertezas simuladas: 
  - Bad Weather, Internal Failure (Car), Internal Failure (Drone), Restricted Area, Traffic Jam.
- Explique que cada incerteza foi avaliada em cinco configurações de constraints:
  - Sem constraints.
  - 1 constraint.
  - 2 constraints.
  - 3 constraints.
  - 3 constraints com hard constraint.

### 2.2 Formalização das Tasks
- Descreva o modelo em JSON usado para representar as tasks, incluindo:
  - **Atributos**: custo, benefício, risco.
  - **Constraints**: soft e hard.
- Apresente um exemplo de JSON e explique como ele foi processado.

### 2.3 Simulação da Rede de Apoio
- Explique a API mockada que simula componentes (drones, carros, bicicletas, pedestres, caminhões).
- Detalhe os atributos gerados semi-aleatoriamente:
  - Distância, tempo de entrega, preço, presença de container seguro.
- Relacione esses atributos com as constraints das tasks.

### 2.4 Abordagens Avaliadas
- Descreva as abordagens comparadas:
  - **Random**: seleção aleatória de componentes.
  - **FIFO**: seleção baseada na ordem de chegada.
  - **U-CBR**: seleção baseada em custo-benefício-risco com pesos binários, pesos = 1, e pesos escalados (Likert).

### 2.5 Métricas de Avaliação
- Taxa de missões concluídas.
- Compliance com constraints.
- Taxa de seleção do componente mais adequado.
- Impacto de diferentes configurações de pesos.

## 3. Resultados e Discussão
Organize os resultados pelas RQs consolidadas:

### RQ1: A abordagem consegue cumprir a tarefa respeitando as constraints?
- Apresente uma tabela com a taxa de sucesso de missões para cada abordagem em todas as configurações.
- Inclua gráficos comparando taxas de sucesso (ex.: Figura X do "Bad Weather").
- Destaque:
  - Como as constraints impactaram o desempenho.
  - Cenários onde a abordagem falhou.

### RQ2: A abordagem seleciona o componente mais adequado para a tarefa?
- Mostre os resultados de seleção por abordagem e componente (ex.: drone, carro).
- Utilize tabelas para destacar a taxa de escolhas corretas versus subótimas.
- Analise:
  - Cenários onde a escolha foi subótima e seus impactos.

### RQ3: Como diferentes configurações de pesos e constraints impactam a eficácia da abordagem?
- Apresente gráficos/tabelas comparando pesos binários, pesos = 1, e escala Likert.
- Discuta:
  - Impactos de má ponderação.
  - Configurações robustas versus sensíveis a ajustes.

## 4. Comparação com Trabalhos Relacionados
- Compare os resultados obtidos com estudos anteriores.
- Destaque os avanços, como:
  - Formalização em JSON.
  - Simulação de rede de apoio.
  - Robustez da abordagem frente a constraints.

## 5. Limitações e Ameaças à Validade
- **Limitações dos Cenários**: Dependência de simulações.
- **Validade Interna**: Discussão sobre possíveis vieses (ex.: geração semi-aleatória).
- **Validade Externa**: Generalização dos resultados para outros domínios.

## 6. Conclusão da Avaliação
- Resuma os principais achados.
- Reforce como os resultados respondem às RQs e sustentam a relevância da abordagem proposta.
