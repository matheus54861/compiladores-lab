# Minha Pequena Linguagem (MPL)

Trabalho semestral de **Compiladores** — Ciência da Computação, UNISAGRADO.  
Professor: Luiz Ricardo Mantovani da Silva · Semestre: 2026-2

Repositório do grupo para o desenvolvimento do compilador completo da linguagem MPL, gerando bytecode executável para a máquina virtual própria.

---

## Instruções da Máquina Virtual (VM)

Abaixo estão descritas as instruções suportadas pela nossa máquina virtual, detalhando o funcionamento de cada uma na pilha:

* `FUNC nome` — Define o ponto de entrada de uma função no bytecode textual.
* `PARAM nome` — Declara um parâmetro formal recebido pela função atual.
* `dest = op1 op op2` — Executa uma operação aritmética ou relacional de três endereços e guarda o resultado.
* `ESCREVA val` — Avalia e escreve o valor correspondente na saída padrão da execução.
* `RETORNE val` — Interrompe a execução da função atual e retorna o valor opcional para o chamador.
* `JEZ cond, rotulo` — Retira o topo da pilha de condição e desvia para o rótulo se o valor for falso ou zero.
* `JMP rotulo` — Realiza um desvio incondicional para o rótulo especificado.