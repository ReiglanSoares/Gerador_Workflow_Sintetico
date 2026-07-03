# Modelos de Códigos Utilizando um Gerador de Workflows Sintéticos

Este repositório reúne implementações e adaptações de workflows reais utilizando um gerador de workflows sintéticos. Atualmente, estão disponíveis exemplos baseados em benchmarks clássicos, como:

* **WordCount** – contagem de palavras em grandes conjuntos de dados;
* **KMeans** – agrupamento de dados por meio de cálculos matemáticos;
* **TeraSort** – ordenação de grandes volumes de arquivos binários.

Os modelos presentes neste repositório são destinados a experimentos em ambientes de Computação de Alto Desempenho (HPC), permitindo a avaliação de desempenho, escalabilidade e comportamento de diferentes motores de workflow.

## Estrutura do Repositório

* **Modelos_DAG/** – Modelos utilizados para gerar os DAGs dos workflows sintéticos.
* **Wordcount_Sintetico_Parsl/** – Implementação completa do workflow WordCount utilizando Parsl, incluindo scripts de execução.
* **Wordcount_Sintetico_PyCOMPSs/** – Implementação completa do workflow WordCount utilizando PyCOMPSs, incluindo scripts de execução.

> Novos benchmarks e implementações serão adicionados conforme o desenvolvimento do projeto.

## Créditos

Os modelos sintéticos disponibilizados neste repositório foram desenvolvidos a partir dos workflows reais disponíveis nos demais repositórios do meu perfil no GitHub, preservando sua estrutura e características de execução para fins de avaliação experimental.

A geração dos DAGs foi realizada utilizando o **Parsl Pattern Workflow Builder**, desenvolvido por Rafael Terra, disponível em:

https://github.com/rafaelstjf/parsl-pattern-workflow-builder
