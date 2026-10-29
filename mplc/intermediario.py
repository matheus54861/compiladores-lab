"""
Geração de código intermédio (código de três endereços).
"""

class GeradorIntermediario:
    def __init__(self, tabela):
        self.tabela = tabela
        self.linhas = []
        self.temp_count = 0

    def novo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def visitar(self, no):
        if not no:
            return None
        
        rotulo = no.rotulo or ""
        
        if rotulo.startswith("funcao"):
            partes = rotulo.split()
            nome_func = no.extra.get('nome') or (partes[1] if len(partes) > 1 else 'principal')
            self.linhas.append(f"funcao {nome_func}")
            for filho in no.filhos:
                self.visitar(filho)
            self.linhas.append(f"fim_funcao {nome_func}")
            
        elif rotulo.startswith("bloco"):
            for filho in no.filhos:
                self.visitar(filho)
                
        elif rotulo.startswith("declaracao"):
            partes = rotulo.split()
            nome = no.extra.get('nome') or (partes[1] if len(partes) > 1 else 'v')
            self.linhas.append(f"declarar {nome}")
            
        elif rotulo.startswith("atribuicao"):
            # Processa atribuição
            for filho in no.filhos:
                self.visitar(filho)
                
        elif rotulo.startswith("retorne"):
            for filho in no.filhos:
                res = self.visitar(filho)
                if res:
                    self.linhas.append(f"retorne {res}")
                else:
                    self.linhas.append("retorne")
                    
        elif rotulo.startswith("literal") or rotulo.startswith("identificador"):
            return no.extra.get('valor') or rotulo.split()[-1]
            
        else:
            for filho in no.filhos:
                self.visitar(filho)

        return None

def gerar(arvore, tabela):
    """Ponto de entrada chamado pelo compilador para gerar o código intermédio."""
    gerador = GeradorIntermediario(tabela)
    if arvore and arvore.filhos:
        for filho in arvore.filhos:
            gerador.visitar(filho)
    return gerador.linhas