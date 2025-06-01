def fcfs(processos, ctx_time=0.5):
    tempo_atual = 0
    total_execucao = 0
    total_espera = 0
    ultimo_processo = None

    processos_ordenados = sorted(processos, key=lambda p: p.chegada)
    
    for processo in processos_ordenados:
        if processo.chegada > tempo_atual:
            tempo_atual = processo.chegada        # Adiciona tempo de troca de contexto se necessário
        if ultimo_processo is not None and ctx_time > 0:
            # Apenas o processo que está saindo registra a troca de contexto
            ctx_duracao = ultimo_processo.adicionar_troca_contexto(tempo_atual, tempo_atual + ctx_time)
            tempo_atual += ctx_duracao
            
        tempo_atual += processo.adicionar_processamento(tempo_atual, tempo_atual + processo.duracao)
        
        total_execucao += processo.get_turnaround()
        total_espera += processo.get_espera()
        
        ultimo_processo = processo
        
    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao, "FCFS"