![image](https://github.com/user-attachments/assets/1317fd69-bf01-48da-b263-5b7a09b8b4dd)

# Métodos de Pesquisa Operacional Aplicados à Gestão de Portfólios com Restrições de Risco e Diversidade

Este Trabalho aborda o problema clássico de seleção de portfólio sob uma nova perspectiva, considerando a gestão simultânea de carteiras para múltiplos investidores. O objetivo principal é desenvolver um modelo de otimização capaz de maximizar o retorno esperado dos investimentos enquanto respeita as restrições específicas de cada investidor.

Essas restrições incluem:

 - `Orçamento Total por Investidor:` O total investido pelos investidores deve ser igual ao capital disponível.
 - `Número Mínimo de Investimentos:` Cada investidor deve incluir no mínimo 4 ativos diferentes.
 - `Número Máximo de Ativos por Investidor:` O número total de ativos selecionados por investidor deve ser menor ou igual a um limite pré-definido.
 - `Limites de Alocação por Ativo:` A proporção investida em um ativo não pode exceder seu limite de liquidez.
 - `Custos de Transação:` O custo total de transação deve ser menor ou igual a um limite pré-definido.
 - `Alocação Mínima por Ativo Selecionado:` Se um ativo for selecionado, ele deve receber no mínimo uma proporção do capital investido.
 - `Volatilidade Máxima por Investidor:` A volatilidade é aproximada linearmente como a soma ponderada dos desvios padrão (σi) de cada ativo.

O papel do gestor de portfólio é modelado como o "decisor central", responsável por alocar os recursos de maneira eficiente e personalizada, levando em consideração o perfil de risco, preferências individuais e as condições de mercado.

O projeto utilizará ferramentas e técnicas de pesquisa operacional, como:

 - Modelos de programação linear e não linear, para encontrar soluções otimizadas.
 - Métodos heurísticos e metaheurísticos, para explorar soluções em grandes espaços de busca.
 - Simulações estocásticas, para incorporar incertezas nos retornos dos ativos.

Além disso, serão realizados estudos comparativos entre diferentes métodos de otimização, destacando as vantagens e limitações de cada abordagem no contexto multi-investidor.

Os resultados esperados incluem:

 - Desenvolvimento de um modelo genérico e adaptável para gestão de portfólios multi-investidor.
 - Demonstração prática do modelo em cenários reais ou simulados.
 - Geração de insights sobre a relação entre retorno, risco e diversificação em alocações multi-investidor.

Este trabalho também contribuirá para nosso aprendizado em pesquisa operacional, com ênfase na utilização da ferramenta Gurobi para a resolução de problemas complexos de otimização, consolidando conhecimentos teóricos e práticos na área.

## 🔨 Status do projeto

- Iniciação
- [x] Escopo inicial definido    
- [x] Apresentação e aprovação do trabalho 
- Planejamento
- [x] Escopo detalhado elaborado
- [x] Correções identificadas e analisadas
- [ ] Ferramentas de desenvolvimento instaladas
- Execução
- [ ] Desenvolvimento do algoritmo de solução
- [ ] Teste dos limites das ferramentas escolhidas
- Encerramento
- [ ] Resultados finais relatados e documentados
- [ ] Seminário final de apresentação finalizado
- [ ] Entrega formal do trabalho realizada

## ✔️ Técnicas e tecnologias utilizadas  

Abaixo segue informações das ferramentas utilizas no trabalho: 

- **`Python`**: Linguagem de programação utilizada para implementar o modelo de otimização e interagir com a API do Gurobi.  
  - **`Biblioteca Gurobi`**: API para Python usada para definir, resolver e analisar o problema de programação linear inteira mista (PLIM).  
  - **`Biblioteca NumPy`**: Utilizada para manipulação de arrays e cálculos matemáticos necessários para o processamento de dados.  
  - **`Biblioteca Pandas`**: Ferramenta essencial para a análise e organização dos dados relacionados aos ativos e investidores.  
- **`Programação Linear Inteira Mista (PLIM)`**: Técnica de otimização utilizada para modelar o problema de seleção de portfólio com múltiplas restrições e objetivos.  
  - **`Modelagem matemática`**: Formulação do problema com funções objetivo e restrições baseadas em volatilidade, diversificação e retorno esperado.  
  - **`Análise de Sensibilidade`**: Avaliação do impacto de variações nos parâmetros do modelo, como alterações nos limites de risco e diversificação.  
- **`Análise de Dados`**:  
  - **`Pré-processamento de dados`**: Limpeza e transformação de dados financeiros para alimentar o modelo de otimização.  
  - **`Visualização de resultados`**: Geração de gráficos para demonstrar a alocação dos ativos e comparar o desempenho das carteiras otimizadas.  
- **`Simulação Estocástica`**: Incorporada para lidar com a incerteza dos retornos financeiros nos cálculos de otimização.  

## 📁 Acesso ao projeto

⛔Acesso aos relatórios finais do projeto ainda em desenvolvimento⛔


## 🛠️ Execução do algoritmo

Siga os passos abaixo para configurar o ambiente e executar o algoritmo:

#### 1. Instalar Python
- Certifique-se de que o Python **3.11 ou superior** está instalado em sua máquina.
- Baixe a versão mais recente em [python.org](https://www.python.org/downloads/).

#### 2. Instalar o Gurobi
- Baixe e instale o Gurobi de acordo com o sistema operacional da sua máquina.
- Solicite uma licença acadêmica gratuita em: [Gurobi Academic License](https://www.gurobi.com/features/academic-named-user-license/).
- Após a instalação, ative a licença conforme as instruções do Gurobi.

#### 3. Acessar a pasta do projeto
- Navegue até a pasta `simulacao` no terminal ou prompt de comando.

#### 4. Criar um Ambiente Virtual
- Execute o comando abaixo para criar um ambiente virtual que irá isolar as dependências do seu projeto:
  ```
    python -m venv venv
  ```

#### 5. Ativar o Ambiente Virtual
- Ative o ambiente virtual:
  - **Windows:**
    ```
    venv\Scripts\activate
    ```
  - **Linux/macOS:**
    ```
    source venv/bin/activate
    ```

Após ativar o ambiente, você verá o nome do ambiente (`venv`) na linha de comando, indicando que ele está ativo.

#### 6. Instalar as Dependências
- Com o ambiente virtual ativado, instale todas as bibliotecas necessárias executando o seguinte comando:
  ```
    python -m pip install -r requirements.txt
  ```

O arquivo `requirements.txt` contém todas as dependências do projeto, incluindo o Gurobi e outras bibliotecas necessárias.

#### 7. Executar o Algoritmo
- Agora, para rodar o algoritmo, execute o arquivo `main.py` localizado em `simulacao/src`:
```
  python simulacao/src/main.py
```

## 🛠️ Execução do algoritmo

Configuração do Ambiente:
  1. Instalar Python(Versão 3.11 ou acima);
  2. Instalar gurobi e adquirir licença de estudante(https://www.gurobi.com/features/academic-named-user-license/
  )
  3. Acesse a pasta simulacao:
  4. Execute:
    ```python -m venv venv```
    Será criado um ambiente virtual
  5. Ative o ambiente virtual com o comando:
    ```venv\Scripts\activate```
  6. Execute o comando:
    ```python -m pip install -r requirements.txt```
    O arquivo requirements.txt contém todas as bibliotecas necessárias para execução do algoritmo.
  7. Agora execute o arquivo main.py dentro de simulacao/src.
    ```python main.py```


## 📚 Mais informações 

Matéria realizada pela escola de engenharia tem como base os seguintes livros: 

- M. Arenales; V. Armentano; R. Morabito; H. Yanasse. Pesquisa Operacional para Cursos de Engenharia, Editora Campus / Elsevier, 2007.

![image](https://github.com/user-attachments/assets/fc7757af-204f-4a45-ae5b-fdfeb58d5d3f)

- M. C. Goldbarg; H. P. Luna. Otimização Combinatória e Programação Linear - Modelos e Algoritmos, 2a ed., Editora Campus / Elsevier, 2005.

![image](https://github.com/user-attachments/assets/8bab24a8-a936-4039-a3b4-b6ea768a3ea2)

- F. S. Hillier; G. J. Lieberman. Introdução à Pesquisa Operacional, 9a ed., Editora Mc Graw Hill, 2013.

![image](https://github.com/user-attachments/assets/8253301e-ba1b-41c5-ab26-f8172d025e16)


