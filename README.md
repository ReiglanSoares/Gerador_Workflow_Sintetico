# Modelos de Códigos Utilizando um Gerador de Workflows Sintéticos

Este repositório reúne implementações e adaptações de workflows reais utilizando um gerador de workflows sintéticos. Atualmente, estão disponíveis exemplos baseados em benchmarks clássicos, como:

* **WordCount** – contagem de palavras em grandes conjuntos de dados;
* **KMeans** – agrupamento de dados por meio de cálculos matemáticos;
* **TeraSort** – ordenação de grandes volumes de arquivos binários.

Os modelos presentes neste repositório são destinados a experimentos em ambientes de Computação de Alto Desempenho (HPC), permitindo a avaliação de desempenho, escalabilidade e comportamento de diferentes motores de workflow.

## Estrutura do Repositório

O repositório está organizado de acordo com os benchmarks e os motores de workflow utilizados:

* **Modelos_DAG/** – Contém os modelos utilizados para representar e gerar os DAGs dos workflows sintéticos.
* **wordcount_sintetico_parsl/** e **wordcount_sintetico_pycompss/** – Implementações sintéticas do WordCount em Parsl e PyCOMPSs.
* **kmeans_sintetico_parsl/** e **kmeans_sintetico_pycompss/** – Implementações sintéticas do KMeans em Parsl e PyCOMPSs.
* **terasort_sintetico_parsl/** e **terasort_sintetico_pycompss/** – Implementações sintéticas do TeraSort em Parsl e PyCOMPSs.

## Padrões Utilizados

Os modelos dos DAGs foram construídos utilizando os padrões disponibilizados pelo **Parsl Pattern Workflow Builder**, combinados de acordo com a estrutura necessária para cada workflow sintético.

### WordCount

Construído utilizando o padrão **SingleTask**, com as tarefas e suas dependências definidas individualmente para representar a estrutura completa do workflow sintético.

<p align="center">
  <img src="Modelos_DAG/wordcount_dag.jpg" width="850">
</p>

<p align="center">
  <em>DAG do workflow sintético WordCount.</em>
</p>

### KMeans

Utiliza uma combinação dos padrões **SingleTask** e **MapReduce**. As tarefas de inicialização e finalização são representadas por **SingleTask**, enquanto as iterações são construídas utilizando o padrão **MapReduce**.

<p align="center">
  <img src="Modelos_DAG/kmeans_dag.jpg" width="850">
</p>

<p align="center">
  <em>DAG do workflow sintético KMeans.</em>
</p>

### TeraSort

Construído utilizando o padrão **MapReduce**, com quatro padrões iniciais conectados a um padrão **MapReduce** final.

<p align="center">
  <img src="Modelos_DAG/terasort_dag.jpg" width="850">
</p>

<p align="center">
  <em>DAG do workflow sintético TeraSort.</em>
</p>

Os códigos utilizados para a construção desses DAGs estão disponíveis no diretório **Modelos_DAG/**.

> Novos benchmarks e implementações serão adicionados conforme o desenvolvimento do projeto.

## Créditos

Os modelos sintéticos disponibilizados neste repositório foram desenvolvidos a partir dos workflows reais disponíveis nos demais repositórios do meu perfil no GitHub, preservando sua estrutura e características de execução para fins de avaliação experimental.

A geração dos DAGs e das execuções sintéticas foi realizada utilizando o **Parsl Pattern Workflow Builder**, desenvolvido por **Rafael Terra**, disponível em:

https://github.com/rafaelstjf/parsl-pattern-workflow-builder



