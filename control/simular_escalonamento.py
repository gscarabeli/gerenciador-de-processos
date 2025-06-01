from control import fcfs, sjf, round_robin, srtf, prioridade_cooperativo, prioridade_preemptivo
from control.algoritmos import inversaoDePrioridade
from control.algoritmos import herancaDePrioridade
#import copy

def simular_escalonamento(processos, algoritmo, quantum_entry=0, ctx_time=0.5):
    if not processos:
        raise Exception("Nenhum processo foi adicionado.")

    #processos = copy.deepcopy(processos)
    ctx_time = float(ctx_time)  # Converte para float caso venha como string

    if algoritmo == 1:
        media_espera, media_execucao, nome_processo = fcfs(processos, ctx_time)
    elif algoritmo == 2:
        media_espera, media_execucao, nome_processo = sjf(processos, ctx_time)
    elif algoritmo == 3:
        quantum = int(quantum_entry)
        media_espera, media_execucao, nome_processo = round_robin(processos, quantum, ctx_time)
    elif algoritmo == 4:
        media_espera, media_execucao, nome_processo = srtf(processos, ctx_time)
    elif algoritmo == 5:
        media_espera, media_execucao, nome_processo = prioridade_cooperativo(processos, ctx_time)
    elif algoritmo == 6:
        media_espera, media_execucao, nome_processo = prioridade_preemptivo(processos, ctx_time)
    elif algoritmo == 7:
        media_espera, media_execucao, nome_processo = inversaoDePrioridade.inversao_prioridade(processos, ctx_time)
    elif algoritmo == 8:
        media_espera, media_execucao, nome_processo = herancaDePrioridade.heranca_prioridade(processos, ctx_time)
    else:
        raise Exception("Selecione um algoritmo válido.")
    
    return media_execucao, media_espera, nome_processo