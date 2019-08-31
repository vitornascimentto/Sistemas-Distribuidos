import random

class Processo:

    def __init__(self, id, coordenador, ativo):
        self.id = id
        self.coordenador = coordenador
        self.ativo = ativo
        self.processos = []

    def __str__(self):
        return 'Processo id: ' + str(self.id) + ' | coordenador: ' + str(self.coordenador) + ' | ativo: ' + str(self.ativo) + '\n' + 'Outros processos existentes: ' + str(self.processos) + '\n'

    def get_id(self):
        return self.id

    def get_ativo(self):
        return self.ativo

    def set_coordenador(self, coordenador):
        self.coordenador = coordenador

    def set_ativo(self, ativo):
        self.ativo = ativo

    def atualizar(self, lista_processos):
        for i in lista_processos:
            if i.get_id() != self.id:
                self.processos.append(i.get_id())

def criar_processos(quantidade):
    
    lista_processos = []

    for i in range(quantidade):
        obj = Processo(i, False, True)
        lista_processos.append(obj)

    return lista_processos

def listar_processos(lista):
    for i in lista:
        print(i.__str__())

def eleicao(lista_processos, inicio):
    
    lista_id = [i.get_id() for i in lista_processos if i.get_ativo()]
    lista_participantes = [i for i in lista_id if i >= inicio]

    print('Processo {} começou a eleição'.format(inicio))

    for i in range(len(lista_participantes)):
        if i != len(lista_participantes) - 1:
            for j in range(i + 1, len(lista_participantes)):
                mensagem(lista_participantes[i], lista_participantes[j])
        else:
            mensagem(lista_participantes[i])
            print('Processo {} é o novo coordenador'.format(lista_participantes[i]))
            print()
            return lista_participantes[i]

def mensagem(p1, p2=None):

    if p2 == None:
        p2 = 'Processo inativo ou inexistente'

    print('{} -> {} (Eleição)'.format(p1, p2))

    if p2 != 'Processo inativo ou inexistente':
        print('{} <- {} (OK)'.format(p1, p2))

def mensagem_coordenador(coordenador, lista_processos):
    
    for i in lista_processos:
        if i.get_id() != coordenador:
            print('{} -> {} (Sou o novo coordenador)'.format(coordenador, i.get_id()))
        else:
            i.set_coordenador(True)

    print()

def matar_processo(id, lista_processos):
    
    for i in lista_processos:
        if i.get_id() == id:
            print('Processo {} parou de funcionar'.format(i.get_id()))
            print()
            i.set_ativo(False)

    quantidade_processos = len(lista_processos) - 1
    processo_eleicao = random.randrange(0, quantidade_processos)

    eleicao(lista_processos, processo_eleicao)

def att(lista_processos):
    for i in lista_processos:
        i.atualizar(lista_processos)

if __name__ == "__main__":
    lista_processos = criar_processos(7)
    
    
    att(lista_processos)

    listar_processos(lista_processos)

    coordenador = eleicao(lista_processos, 3)
    mensagem_coordenador(coordenador, lista_processos)

    listar_processos(lista_processos)

    matar_processo(6, lista_processos)