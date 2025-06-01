def srtf(processos, ctx_time=0.5):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    ultimo_processo = None

    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.tempo_restante))

    while processos_ordenados:
        processo_atual = processos_ordenados[0]

        if processo_atual.chegada > tempo_atual:
            tempo_atual += processo_atual.chegada

        for processo in processos_ordenados:
            if processo.chegada <= tempo_atual and processo.tempo_restante < processo_atual.tempo_restante:
                processo_atual = processo        # Adiciona tempo de troca de contexto se necessário e se houve mudança de processo
        if ultimo_processo is not None and ultimo_processo != processo_atual and ctx_time > 0:
            # Apenas o processo que está saindo registra a troca de contexto
            ctx_duracao = ultimo_processo.adicionar_troca_contexto(tempo_atual, tempo_atual + ctx_time)
            tempo_atual += ctx_duracao

        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)

        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
            processos_ordenados.remove(processo_atual)

        ultimo_processo = processo_atual

    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao, "SRTF"
