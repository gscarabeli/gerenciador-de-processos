class Prioridade:
    def __init__(self, numero):
        self.numero = numero
        # Para manter compatibilidade com herança e inversão de prioridade
        # alterna entre recursos A e B baseado em número par/ímpar
        self.recurso = 'A' if numero % 2 == 0 else 'B'