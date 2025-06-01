from model.prioridade import Prioridade

class Periodo:
    def __init__(self, inicio, fim, tipo="Execução"):
        self.inicio = inicio
        self.fim = fim
        self.tipo = tipo  # "Execução" ou "CTX"
    
    def get_duracao(self):
        return self.fim - self.inicio

    def contem_instante(self, instante, epsilon=0.0001):
        return self.inicio - epsilon <= instante < self.fim + epsilon

class Processo:
    def __init__(self, id, chegada, duracao, prioridade : Prioridade):
        self.id = id
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.tempo_restante = duracao
        self.processamentos = []
        self.ultimo_contexto = None  # Para rastrear último processo em execução
    
    def adicionar_processamento(self, inicio, fim):
        if self.tempo_restante - (fim - inicio) < 0:
            fim = inicio + self.tempo_restante

        self.processamentos.append(Periodo(inicio, fim))
        self.tempo_restante -= fim - inicio

        return self.processamentos[-1].get_duracao()

    def adicionar_troca_contexto(self, inicio, fim):
        self.processamentos.append(Periodo(inicio, fim, "CTX"))
        return fim - inicio
    
    def get_turnaround(self):
        if not self.processamentos:
            return 0
        
        # Filtra apenas os períodos de execução
        periodos_execucao = [p for p in self.processamentos if p.tipo == "Execução"]
        if not periodos_execucao:
            return 0
        
        # Turnaround = término da última execução - chegada
        ultimo_periodo = periodos_execucao[-1]
        return ultimo_periodo.fim - self.chegada

    def get_espera(self):
        if not self.processamentos:
            return 0
            
        # Filtra apenas os períodos de execução
        periodos_execucao = [p for p in self.processamentos if p.tipo == "Execução"]
        if not periodos_execucao:
            return 0
            
        # Espera = início da primeira execução - chegada
        primeiro_periodo = periodos_execucao[0]
        return primeiro_periodo.inicio - self.chegada

    def verificar_estado(self, instante, epsilon=0.0001):
        if not self.processamentos:
            return "Desconhecido"
        
        if instante < self.chegada - epsilon:
            return "Antes da chegada"
        
        if instante >= self.processamentos[-1].fim - epsilon:
            return "Após a chegada"

        for periodo in self.processamentos:
            if periodo.contem_instante(instante, epsilon):
                return periodo.tipo
            
        return "Espera"
    
    def __str__(self):
        return f'Processo(id={self.id})'
