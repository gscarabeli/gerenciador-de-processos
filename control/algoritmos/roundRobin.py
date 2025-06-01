def round_robin(processos, quantum=2, ctx_time=0.5):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    processos_ordenados = sorted(processos, key=lambda p: p.chegada)
    fila = []

    while processos_ordenados:
        for processo in processos_ordenados:
            if(processo.chegada <= tempo_atual and processo not in fila):
                fila.append(processo)

        if not fila:
            tempo_atual += 1
            continue

        processo_atual = fila.pop(0)
        processos_ordenados.remove(processo_atual)        # Adiciona tempo de troca de contexto se necessário
        if ultimo_processo is not None and ultimo_processo != processo_atual and ctx_time > 0:
            # Apenas o processo que está saindo registra a troca de contexto
            ctx_duracao = ultimo_processo.adicionar_troca_contexto(tempo_atual, tempo_atual + ctx_time)
            tempo_atual += ctx_duracao

        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + quantum)

        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
        else:
            processos_ordenados.append(processo_atual)

        ultimo_processo = processo_atual

    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao, "Round Robin"
