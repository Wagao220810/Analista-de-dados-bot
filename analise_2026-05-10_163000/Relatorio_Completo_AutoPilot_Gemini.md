# 📊 Relatório Analítico Executivo - Dataset do Titanic

## Sumário Executivo

Este relatório apresenta uma análise aprofundada do dataset do Titanic, com o objetivo de compreender a estrutura dos dados, identificar padrões e anomalias, e fornecer recomendações acionáveis. A análise inicial revela um dataset rico em informações demográficas e de viagem, mas com desafios notáveis na qualidade dos dados, especialmente na presença de valores nulos significativos. Observamos uma taxa de sobrevivência geral de aproximadamente 38%, e insights iniciais já apontam para a importância de características como a classe do bilhete e a idade na probabilidade de sobrevivência.

---

## 1. Visão Geral e Qualidade dos Dados

### O que este dataset representa?
O dataset em questão compreende informações detalhadas sobre 891 passageiros do RMS Titanic, abrangendo dados como identificação, status de sobrevivência, classe do bilhete, nome, sexo, idade, número de irmãos/cônjuges a bordo (`SibSp`), número de pais/filhos a bordo (`Parch`), número do bilhete, tarifa paga, cabine e porto de embarque. O principal objetivo deste conjunto de dados é, geralmente, analisar os fatores que influenciaram a sobrevivência ou não dos passageiros durante o naufrágio.

### Os dados estão limpos?
O dataset apresenta uma mistura de tipos de dados (`int64`, `float64`, `str`) e está razoavelmente estruturado. No entanto, a qualidade dos dados não é ideal, com a presença de valores nulos significativos em algumas colunas cruciais.

### Existem nulos problemáticos?
Sim, a presença de valores nulos é uma questão importante que precisa ser abordada:

*   **`Age` (Idade):** 177 valores nulos (aproximadamente 19.8% do total). Esta é uma coluna de alta relevância para a análise de sobrevivência, e a imputação desses valores será essencial para a robustez de qualquer modelo preditivo.
*   **`Cabin` (Cabine):** 687 valores nulos (aproximadamente 77.1% do total). A vasta maioria dos registros não possui informação de cabine. Devido à alta taxa de valores ausentes, esta coluna é altamente problemática para uso direto e provavelmente exigirá uma estratégia de feature engineering (e.g., criar uma feature binária indicando "Possui Cabine" ou "Não Possui Cabine") ou a remoção completa da análise.
*   **`Embarked` (Porto de Embarque):** 2 valores nulos (aproximadamente 0.2%). Esta é uma quantidade insignificante e pode ser facilmente tratada pela imputação com a moda (o valor mais frequente) sem impacto substancial na análise.

Outras colunas como `Name` e `Ticket`, embora completas, contêm dados textuais com alta cardinalidade, o que sugere a necessidade de feature engineering para extrair informações úteis (e.g., títulos do nome). `PassengerId` é apenas um identificador e não tem valor preditivo direto.

---

## 2. Principais Insights Estatísticos

A análise das estatísticas descritivas revela padrões iniciais importantes:

*   **Taxa de Sobrevivência (Target `Survived`):** A média de 0.3838 indica que, dos 891 passageiros, aproximadamente **38.4% sobreviveram** ao naufrágio. Este é o ponto de partida para qualquer análise, buscando entender quais fatores se correlacionam com essa taxa.
*   **Classe do Bilhete (`Pclass`):** A média de 2.30 indica que a maioria dos passageiros viajava na 2ª ou 3ª classe. A mediana e o 3º quartil em 3 sugerem que a 3ª classe era a mais populosa. Isso é um forte indício de que a classe social (ou poder aquisitivo) pode ter desempenhado um papel na sobrevivência.
*   **Idade (`Age`):** A idade média dos passageiros era de aproximadamente **29.7 anos**, com um desvio padrão de 14.5 anos, indicando uma distribuição razoavelmente ampla. A presença de passageiros muito jovens (mínimo de 0.42 anos, ou seja, bebês) e muito idosos (máximo de 80 anos) destaca a diversidade demográfica a bordo e a necessidade de investigar a relação da idade com a sobrevivência.
*   **Parentes a Bordo (`SibSp` e `Parch`):** As médias de 0.52 para `SibSp` e 0.38 para `Parch` sugerem que a maioria dos passageiros viajava sozinha ou com poucos familiares diretos. No entanto, os valores máximos (8 para `SibSp` e 6 para `Parch`) indicam a presença de algumas famílias grandes. Combinar essas duas características em uma única feature de "Tamanho da Família" (`FamilySize`) poderia ser mais informativo.
*   **Tarifa (`Fare`):** A tarifa média foi de **£32.20**, mas com um desvio padrão muito alto (£49.69). A diferença significativa entre a média (£32.20) e a mediana (£14.45) é um forte indicativo de uma distribuição altamente assimétrica, com muitos passageiros pagando tarifas baixas e alguns poucos pagando tarifas extremamente altas. O valor máximo de £512.33 demonstra essa disparidade.
*   **Gênero (`Sex`):** Embora não explicitamente nas estatísticas descritivas numéricas, a amostra de dados (`male`, `female`) aponta para o gênero como uma variável categórica fundamental. A regra histórica de "mulheres e crianças primeiro" é uma hipótese forte a ser testada.

---

## 3. Detecção de Anomalias

Ao revisar as estatísticas e a amostra de dados, algumas observações importantes, embora nem todas sejam anomalias no sentido de erro de dado, merecem destaque:

*   **`Age`:** Os valores mínimos (0.42 anos) e máximos (80 anos) são válidos e representam a amplitude etária real dos passageiros. Não são anomalias a serem removidas, mas indicam a necessidade de explorar como a idade extrema (muito jovens vs. muito idosos) pode influenciar a sobrevivência.
*   **`Fare`:**
    *   **Mínimo de £0.00:** Este valor pode ser considerado anômalo se todos os passageiros devessem pagar. Pode indicar tripulantes, passageiros com bilhetes patrocinados ou cortesias. É crucial investigar esses casos para entender seu contexto e se eles devem ser tratados de forma diferente.
    *   **Máximo de £512.33:** Embora seja um outlier estatístico, é um valor válido que representa passageiros de altíssima renda, provavelmente viajando na 1ª classe e possivelmente em cabines de luxo. A distribuição altamente assimétrica do `Fare` (evidenciada pela grande diferença entre média e mediana) não é uma anomalia de dado, mas uma característica da distribuição que exige consideração em modelagem (e.g., transformação logarítmica para reduzir o skewness).
*   **`SibSp` e `Parch`:** Os valores máximos de 8 e 6, respectivamente, são estatisticamente outliers (muito distantes da média/mediana), mas representam famílias reais e numerosas a bordo. Não devem ser removidos, mas sua representação em features (como `FamilySize`) pode ser mais eficaz.
*   **`Cabin`:** A anomalia mais significativa é a **esmagadora quantidade de valores nulos (77%)**. Isso torna a coluna quase inutilizável em sua forma original e é uma "anomalia de qualidade de dados" que impacta diretamente a capacidade de extrair insights ou construir modelos robustos baseados na localização da cabine.

---

## 4. Próximos Passos e Ações de Negócio

Com base nesta análise inicial, as seguintes ações são recomendadas para aprofundar o entendimento e preparar o dataset para a construção de modelos preditivos:

### 4.1. Tratamento e Limpeza de Dados
*   **Imputação de `Age`:** Utilizar estratégias de imputação mais sofisticadas do que apenas a média/mediana. Uma abordagem interessante seria imputar `Age` com base em `Title` (extraído da coluna `Name`) e `Pclass`, ou usar um modelo preditivo (e.g., KNN Imputer ou regressão) para preencher os valores ausentes.
*   **Imputação de `Embarked`:** Preencher os 2 valores nulos com a moda da coluna (o porto de embarque mais frequente), que provavelmente é 'S' (Southampton).
*   **Tratamento de `Cabin`:** Descartar a coluna `Cabin` original devido à alta taxa de nulos. Em vez disso, criar uma nova feature binária, `Has_Cabin`, que indica se um passageiro tinha uma cabine registrada (1) ou não (0). Isso pode capturar a informação de que a posse de uma cabine (e, por extensão, um status social/econômico mais elevado) pode ter influenciado a sobrevivência.
*   **Investigação de `Fare` = 0:** Entender o contexto dos passageiros que pagaram tarifa zero. Se forem tripulantes ou passageiros especiais, pode ser prudente tratá-los separadamente ou criar uma feature indicadora.

### 4.2. Engenharia de Features
*   **Extração de Títulos:** Criar uma nova feature `Title` a partir da coluna `Name` (ex: Mr., Mrs., Miss, Master, Dr., Rev., etc.). Títulos geralmente se correlacionam com `Sex`, `Age` e `Pclass`, sendo fortes preditores de sobrevivência e úteis para imputar `Age`.
*   **Criação de `FamilySize`:** Combinar `SibSp` e `Parch` em uma nova feature `FamilySize` = `SibSp` + `Parch` + 1 (incluindo o próprio passageiro). Isso pode capturar o efeito de viajar em família. Criar também `Is_Alone` (1 se `FamilySize` == 1, 0 caso contrário).
*   **Binning de `Age` e `Fare`:** Para capturar relações não-lineares, pode ser útil categorizar `Age` e `Fare` em faixas (bins), especialmente para modelos que não lidam bem com distribuições skewed ou variáveis contínuas.
*   **Processamento de `Ticket`:** Embora complexo, o prefixo ou o comprimento do `Ticket` pode ocasionalmente fornecer informações sobre o tipo de bilhete ou grupo de viagem. Uma análise mais aprofundada pode ser considerada.

### 4.3. Análise Exploratória de Dados (EDA) Aprofundada
*   **Análise Bivariada e Multivariada:**
    *   Investigar a relação entre `Survived` e as novas features (`Title`, `FamilySize`, `Has_Cabin`, `Is_Alone`), bem como as features existentes (`Sex`, `Pclass`, `Age` imputada, `Fare` tratada, `Embarked` imputado).
    *   Gerar visualizações (gráficos de barras, box plots, mapas de calor para correlações) para identificar padrões e a força das relações. Ex: Qual a taxa de sobrevivência por `Sex` e `Pclass`? Como a `Age` (distribuição) difere entre sobreviventes e não-sobreviventes?
*   **Validação de Hipóteses:** Confirmar a validade da hipótese "mulheres e crianças primeiro" e a influência da classe social na sobrevivência.

### 4.4. Modelagem Preditiva e Insights de Negócio
*   **Construção de Modelos:** Após a fase de engenharia de features, construir e treinar modelos de classificação (e.g., Regressão Logística, Random Forest, Gradient Boosting Machines, SVM) para prever a sobrevivência.
*   **Interpretabilidade do Modelo:** Avaliar a importância das features no modelo final para quantificar quais fatores foram mais críticos para a sobrevivência. Isso oferece insights valiosos sobre a dinâmica do naufrágio.
*   **Ações e Lições de Negócio:**
    *   **Impacto da Classe Social:** Quantificar o impacto da `Pclass` e `Fare` na sobrevivência pode reforçar a discussão sobre desigualdade e priorização em situações de emergência.
    *   **Demografia Crítica:** Destacar quais grupos demográficos (idade, gênero, tamanho da família) tiveram maiores ou menores chances de sobrevivência.
    *   **Preparação para Emergências:** Embora seja um evento histórico, as lições aprendidas podem ser extrapoladas para discussões sobre protocolos de segurança, design de embarcações e prioridades de evacuação em situações futuras de crise, garantindo que tais tragédias não sejam repetidas e que a chance de sobrevivência seja maximizada para todos, independentemente de fatores externos.

---