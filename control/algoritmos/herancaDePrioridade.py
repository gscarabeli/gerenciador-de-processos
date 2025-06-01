from model.prioridade import Prioridade

def heranca_prioridade(processos, ctx_time=0.5):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    # Rastreamento de recursos e prioridades
    recursos = {}  # Mapa de processo -> tempo de liberação do recurso
    prioridade_original = {}  # Mapa de processo -> prioridade original
    processo_bloqueado = None  # Processo que está esperando pelo recurso

    # Ordenação inicial por chegada e prioridade
    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade.numero))

    while processos_ordenados:
        # Define próximo processo a executar
        processo_atual = processos_ordenados[0]

        # Avança o tempo se necessário
        if processo_atual.chegada > tempo_atual:
            tempo_atual = processo_atual.chegada

        # Verifica se há processos de maior prioridade querendo o recurso
        for processo in processos_ordenados:
            if processo.chegada <= tempo_atual and processo.prioridade.numero > processo_atual.prioridade.numero:
                if processo_atual in recursos:  # Se o processo atual tem um recurso
                    # Guarda prioridade original se ainda não guardada
                    if processo_atual not in prioridade_original:
                        prioridade_original[processo_atual] = processo_atual.prioridade.numero
                    # Herda a prioridade mais alta
                    processo_atual.prioridade.numero = processo.prioridade.numero
                    processo_bloqueado = processo
                    break

        # Verifica se é hora de liberar algum recurso
        if processo_atual in recursos and tempo_atual >= recursos[processo_atual]:
            # Restaura prioridade original
            if processo_atual in prioridade_original:
                processo_atual.prioridade.numero = prioridade_original[processo_atual]
                del prioridade_original[processo_atual]
            # Libera o recurso
            del recursos[processo_atual]
            # Desbloqueia o processo que estava esperando
            if processo_bloqueado:
                processo_bloqueado = None

        # Adiciona tempo de troca de contexto se necessário
        if ultimo_processo is not None and ultimo_processo != processo_atual and ctx_time > 0:
            ctx_duracao = ultimo_processo.adicionar_troca_contexto(tempo_atual, tempo_atual + ctx_time)
            tempo_atual += ctx_duracao

        # Executa por 1 unidade de tempo
        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)

        # Se o processo está começando, aloca o recurso
        if processo_atual.tempo_restante == processo_atual.duracao - 1:
            # Aloca o recurso por metade da duração do processo
            recursos[processo_atual] = tempo_atual + (processo_atual.duracao / 2)

        # Se o processo terminou
        if processo_atual.tempo_restante == 0:
            # Restaura prioridade original se necessário
            if processo_atual in prioridade_original:
                processo_atual.prioridade.numero = prioridade_original[processo_atual]
                del prioridade_original[processo_atual]
            # Remove processo da lista
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            processos_ordenados.remove(processo_atual)

        # Reordena os processos considerando as prioridades herdadas
        processos_ordenados.sort(key=lambda p: (
            p.chegada > tempo_atual,  # Primeiro os que já chegaram
            -p.prioridade.numero,     # Depois por prioridade (maior primeiro)
            p.chegada                 # Por fim, por ordem de chegada
        ))
        
        ultimo_processo = processo_atual

    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao, "Herança de Prioridade"