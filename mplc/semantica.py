"""
Entrega 3 — análise semântica.

Tabela de símbolos, escopos aninhados e verificação de tipos.
"""
from mplc.erros import ErroMPL

class Escopo:
    def __init__(self, id, nome, categoria="global", pai=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria  # 'global', 'funcao' ou 'bloco'
        self.pai = pai
        self.simbolos = {}

    def definir(self, nome, categoria, tipo, linha, coluna):
        if nome in self.simbolos:
            raise ErroMPL("semantico", linha, coluna, f"variável '{nome}' já declarada neste escopo")
        self.simbolos[nome] = {
            "nome": nome,
            "categoria": categoria,
            "tipo": tipo,
            "linha": linha
        }

    def buscar(self, nome):
        if nome in self.simbolos:
            return self.simbolos[nome]
        if self.pai:
            return self.pai.buscar(nome)
        return None


def analisar(arvore):
    """Percorre a árvore recursivamente, monta a tabela e valida as regras semânticas."""
    global_escopo = Escopo(id=0, nome="global", categoria="global", pai=None)
    escopos_lista = [global_escopo]
    
    tem_principal = False

    def visitar(no, escopo_atual):
        nonlocal tem_principal
        if not no:
            return

        rotulo = no.rotulo or ""

        if rotulo.startswith("funcao"):
            partes = rotulo.split()
            nome_func = no.extra.get('nome') or (partes[1] if len(partes) > 1 else 'principal')
            tipo_ret = no.extra.get('tipo') or (partes[2] if len(partes) > 2 else 'inteiro')
            
            if nome_func == "principal":
                tem_principal = True

            # 1. Escopo da função
            func_id = len(escopos_lista)
            func_escopo = Escopo(id=func_id, nome=nome_func, categoria="funcao", pai=escopo_atual)
            escopos_lista.append(func_escopo)
            
            # Extrai parâmetros e regista no escopo da função
            params_tipos = []
            tem_params = False
            for sub in no.filhos:
                if sub.rotulo and sub.rotulo.startswith("parametros"):
                    for p in sub.filhos:
                        if p.rotulo and p.rotulo.startswith("parametro"):
                            tem_params = True
                            p_partes = p.rotulo.split()
                            p_nome = p.extra.get('nome') or (p_partes[1] if len(p_partes) > 1 else 'x')
                            p_tipo = p.extra.get('tipo') or (p_partes[2] if len(p_partes) > 2 else 'inteiro')
                            params_tipos.append(p_tipo)
                            func_escopo.definir(p_nome, "parametro", p_tipo, p.linha or 1, p.coluna or 1)
            
            if nome_func == "principal" and tem_params:
                raise ErroMPL("semantico", no.linha or 1, no.coluna or 1, "função 'principal' não pode ter parâmetros")

            tipo_completo = f"{tipo_ret}({','.join(params_tipos)})"
            escopo_atual.definir(nome_func, "funcao", tipo_completo, no.linha or 1, no.coluna or 1)
            
            # Visita os filhos da função passando o escopo da função
            for sub in no.filhos:
                visitar(sub, func_escopo)

        elif rotulo.startswith("bloco"):
            # 2. Cada bloco cria um novo escopo filho aninhado
            bloco_id = len(escopos_lista)
            bloco_escopo = Escopo(id=bloco_id, nome="bloco", categoria="bloco", pai=escopo_atual)
            escopos_lista.append(bloco_escopo)
            
            for sub in no.filhos:
                visitar(sub, bloco_escopo)

        elif rotulo.startswith("declaracao"):
            d_partes = rotulo.split()
            d_nome = no.extra.get('nome') or (d_partes[1] if len(d_partes) > 1 else 'v')
            d_tipo = no.extra.get('tipo') or (d_partes[2] if len(d_partes) > 2 else 'inteiro')
            escopo_atual.definir(d_nome, "variavel", d_tipo, no.linha or 1, no.coluna or 1)
            for sub in no.filhos:
                visitar(sub, escopo_atual)

        elif rotulo.startswith("identificador"):
            i_nome = no.extra.get('nome') or rotulo.split()[-1]
            if not escopo_atual.buscar(i_nome):
                raise ErroMPL("semantico", no.linha or 1, no.coluna or 1, f"variável '{i_nome}' não declarada")
            for sub in no.filhos:
                visitar(sub, escopo_atual)

        else:
            for sub in no.filhos:
                visitar(sub, escopo_atual)

    if arvore and arvore.filhos:
        for filho in arvore.filhos:
            visitar(filho, global_escopo)

    if not tem_principal:
        raise ErroMPL("semantico", 1, 1, "função 'principal' não declarada")

    return {"escopos_obj": escopos_lista}


def despejar(tabela):
    """Devolve as linhas do --tabela, no formato da seção 4 do contrato."""
    linhas = []
    escopos = tabela.get("escopos_obj", [])
    for escopo in escopos:
        if escopo.id == 0:
            linhas.append(f"escopo {escopo.id} {escopo.nome}")
        elif escopo.categoria == "funcao":
            pai_id = escopo.pai.id if escopo.pai else 0
            linhas.append(f"escopo {escopo.id} funcao {escopo.nome} pai {pai_id}")
        elif escopo.categoria == "bloco":
            pai_id = escopo.pai.id if escopo.pai else 0
            linhas.append(f"escopo {escopo.id} bloco pai {pai_id}")
        
        for nome, simbolo in escopo.simbolos.items():
            linhas.append(f"  {simbolo['nome']}|{simbolo['categoria']}|{simbolo['tipo']}|{simbolo['linha']}")
    return linhas