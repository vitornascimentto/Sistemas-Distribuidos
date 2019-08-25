class Processo:

    def __init__(self, id, coordenador, vivo):
        self.id = id
        self.coordenador = coordenador
        self.vivo = vivo

    def __str__(self):
        return 'id: ' + str(self.id) + ' | coordenador: ' + str(self.coordenador) + ' | vivo: ' + str(self.vivo)

    def get_id(self):
        return self.id

    def get_vivo(self):
        return self.vivo

    def set_coordenador(self, coordenador):
        self.coordenador = coordenador

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
    
    lista_id = [i.get_id() for i in lista_processos if i.get_vivo()]
    lista_participantes = [i for i in lista_id if i >= inicio]

    for i in range(len(lista_participantes)):
        if i != len(lista_participantes) - 1:
            mensagem(lista_participantes[i], lista_participantes[i + 1])

        else:
            mensagem(lista_participantes[i])
            print('nó {} é o novo coordenador'.format(lista_participantes[i]))
            return lista_participantes[i]

def mensagem(p1, p2=None):

    if p2 == None:
        p2 = 'nó inativo ou inexistente'

    print('{} -> {} (Eleição)'.format(p1, p2))

    if p2 != 'nó inativo ou inexistente':
        print('{} <- {} (OK)'.format(p1, p2))

def mensagem_coordenador(coordenador, lista_processos):
    
    for i in lista_processos:
        if i.get_id() != coordenador:
            print('{} -> {} (Sou o novo coordenador)'.format(coordenador, i.get_id()))
        else:
            i.set_coordenador(True)



if __name__ == "__main__":
    lista_processos = criar_processos(5)

    listar_processos(lista_processos)

    coordenador = eleicao(lista_processos, 2)

    mensagem_coordenador(coordenador, lista_processos)

    listar_processos(lista_processos)





    