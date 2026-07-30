## Como Usar (Passo a Passo)
### 1. Execute as Funções Base do Pipeline
Copie o código do arquivo pipeline_universal.py (ou rode a célula correspondente no Google Colab) para carregar as funções carregar_dados_universal() e gerar_grafico_universal().

### 2. Carregue seus Dados
Você pode carregar uma série do Banco Central apenas informando o código da série, ou passar o caminho do seu próprio arquivo CSV:

```Python

#Exemplo A: Carregando a série do IPCA (Código 433 do BACEN)
df_dados = carregar_dados_universal(fonte=433)

#Exemplo B: Carregando um arquivo CSV próprio
#df_dados = carregar_dados_universal(fonte="meus_dados.csv", col_data="data", col_valor="valor", sep=";")
```

### 3. Gere o Gráfico que Desejar
Chame a função gerar_grafico_universal escolhendo o parâmetro tipo_grafico:

#### Gráfico de Linha (Série Temporal)
```Python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='linha', 
    titulo='Evolução Histórica do Indicador', 
    nome_arquivo='grafico_linha'
)
```
#### Gráfico de Barras (Média Anual)
```Python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='barra', 
    agregacao='mean', 
    agrupar_por='ano', 
    titulo='Média Anual do Indicador', 
    nome_arquivo='grafico_barras', 
    cor='teal'
)
```
#### Gráfico de Pizza (Categorização por Faixas)
```python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='pizza', 
    num_faixas=3, 
    titulo='Distribuição Proporcional por Faixas', 
    nome_arquivo='grafico_pizza'
)
```
#### Histograma de Frequência
```Python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='histograma', 
    eixo_y='valor', 
    titulo='Distribuição de Frequência', 
    nome_arquivo='grafico_histograma', 
    cor='orange'
)
```
#### Boxplot (Análise de Outliers)
```Python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='boxplot', 
    eixo_y='valor', 
    titulo='Dispersão e Outliers', 
    nome_arquivo='grafico_boxplot', 
    cor='purple'
)
```
#### Gráfico de Área (Preenchimento Temporal)
```Python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='area', 
    titulo='Evolução e Volume da Série Temporal', 
    nome_arquivo='grafico_area', 
    cor='seagreen'
)
```
#### Gráfico de Dispersão (Dispersão de Observações)
```Python
gerar_grafico_universal(
    df_dados, 
    tipo_grafico='dispersao', 
    eixo_y='valor', 
    titulo='Dispersão dos Valores ao Longo do Tempo', 
    nome_arquivo='grafico_dispersao', 
    cor='crimson'
)
```
## Autoria e Citação
Trabalho desenvolvido na disciplina de Técnicas de Pesquisa e Análise Econômica 2 do curso de Ciências Econômicas da Universidade Federal da Paraíba (UFPB), no âmbito da pesquisa em Economia Aplicada e Reprodutibilidade Acadêmica.

João Henrique B. M. Cavalcanti

Joice Alves da Silva
