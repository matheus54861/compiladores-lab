# Compilador MPL (Minha Pequena Linguagem)

Trabalho semestral desenvolvido para a disciplina de Compiladores do curso de Ciência da Computação na **UNISAGRADO** (Semestre 2026-2).

## Integrantes do Grupo
- Matheus Pereira Marques

---

## 1. Tabela de Tokens
Abaixo estão os principais tokens reconhecidos pelo analisador léxico (`mplc/lexico.py`):

| Categoria | Lexemas / Exemplos | Descrição |
| :--- | :--- | :--- |
| **Palavras-Chave** | `funcao`, `inteiro`, `real`, `texto`, `logico`, `vazio`, `se`, `senao`, `enquanto`, `retorne`, `escreva` | Palavras reservadas da linguagem MPL. |
| **Identificadores** | `[a-zA-Z_][a-zA-Z0-9_]*` | Nomes de variáveis, funções e parâmetros. |
| **Literais Inteiros** | `[0-9]+` | Números inteiros. |
| **Literais Reais** | `[0-9]+\.[0-9]+` | Números de ponto flutuante. |
| **Literais de Texto** | `"..."` | Cadeias de caracteres delimitadas por aspas. |
| **Literais Lógicos** | `verdadeiro`, `falso` | Valores booleanos. |
| **Operadores** | `+`, `-`, `*`, `/`, `%`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=` | Operadores aritméticos e relacionais. |
| **Pontuação** | `;`, `,`, `(`, `)`, `{`, `}` | Delimitadores estruturais e de escopo. |

---

## 2. Gramática da Linguagem (BNF)
Estrutura gramatical simplificada da MPL utilizada pelo analisador sintático (`mplc/sintatico.py`):

```text
programa       ::= declaracao*
declaracao     ::= funcao
funcao         ::= "funcao" tipo ID "(" parametros? ")" Bloco
tipo           ::= "inteiro" | "real" | "texto" | "logico" | "vazio"
parametros     ::= tipo ID ("," tipo ID)*
Bloco          ::= "{" comando* "}"
comando        ::= declaracao_var
               | atribuicao
               | condicional
               | laco
               | retorno
               | escrita
declaracao_var ::= tipo ID ("=" expressao)? ";"
atribuicao     ::= ID "=" expressao ";"
condicional    ::= "se" "(" expressao ")" Bloco ("senao" Bloco)?
laco           ::= "enquanto" "(" expressao ")" Bloco
retorno        ::= "retorne" expressao? ";"
escrita        ::= "escreva" "(" expressao ")" ";"
expressao      ::= relacional

3. Estrutura de Escopos e Símbolos
O analisador semântico (mplc/semantica.py) gerencia os escopos da seguinte forma:

Escopos Aninhados com Sombreamento: Variáveis declaradas em escopos internos (como dentro de blocos se ou enquanto) ocultam temporariamente as variáveis de escopo externo com o mesmo nome.

Duas Passadas: A tabela de símbolos realiza uma passagem prévia apenas para coletar assinaturas de funções globais, permitindo a chamada mútua e o uso de funções antes de sua definição formal no arquivo fonte.

4. Instruções da Máquina Virtual (VM)
Instruções suportadas pelo bytecode textual .mplb e executadas pela VM (mplc/vm.py):

FUNC nome — Define o ponto de entrada de uma função no bytecode, inicializando o seu registro de ativação.

PARAM nome — Declara e vincula um parâmetro formal recebido pela função atual a partir da pilha de execução.

dest = op1 op op2 — Executa uma operação aritmética ou relacional de três endereços utilizando dois operandos e guarda o resultado na variável de destino.

ESCREVA val — Avalia o argumento correspondente e imprime o seu valor na saída padrão (stdout) da execução.

RETORNE val — Interrompe a execução da função atual e devolve opcionalmente o valor resultante ao escopo chamador.

JEZ cond, rotulo — Retira o valor do topo da pilha de condição; se o valor for falso ou zero (0), desvia o fluxo de execução para o rótulo especificado.

JMP rotulo — Realiza um desvio incondicional do fluxo para o rótulo indicado no bytecode.