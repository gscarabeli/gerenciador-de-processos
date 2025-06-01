import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk

def centralizar_grafico(fig):
    janela_temporaria = tk.Tk()
    janela_temporaria.withdraw()

    largura_tela = janela_temporaria.winfo_screenwidth()
    altura_tela = janela_temporaria.winfo_screenheight()

    largura_janela = fig.canvas.manager.window.winfo_width()
    altura_janela = fig.canvas.manager.window.winfo_height()

    pos_x = (largura_tela // 2) - int(1.5 * largura_janela)
    pos_y = (altura_tela // 2) - int(1.5 * altura_janela)

    fig.canvas.manager.window.wm_geometry(f"+{pos_x}+{pos_y}")

    janela_temporaria.destroy()

def grafico_processos(processos, media_execucao, media_espera, nome_processo):
    fig, ax = plt.subplots(figsize=(14, 6))  # Set larger figure size
    plt.subplots_adjust(left=0.1, right=0.85, bottom=0.1, top=0.9)  # Adjust margins
    
    fig.canvas.manager.set_window_title('Gráfico de Escalonamento')
    tempo_maximo = max([max([p.fim for p in processo.processamentos]) for processo in processos if processo.processamentos])
    ax.set_xlim(0, tempo_maximo)
    # Usar mais pontos no eixo x para mostrar períodos de 0.5s
    ticks = [i/2 for i in range(int(tempo_maximo * 2) + 1)]
    ax.set_xticks(ticks)
    # Formatar os números para não mostrar .0 em números inteiros
    ax.set_xticklabels([str(int(x)) if x.is_integer() else f"{x:.1f}" for x in ticks])
    ax.set_yticks(range(1, len(processos) + 1))
    ax.set_yticklabels([f"Processo {i}" for i in range(1, len(processos) + 1)])

    for processo in processos:
        # Para cada processo, desenhar seus períodos de execução, contexto e espera
        for periodo in processo.processamentos:
            duracao = periodo.fim - periodo.inicio
            if periodo.tipo == "Execução":
                ax.barh(processo.id, duracao, left=periodo.inicio, color='#1E90FF', edgecolor='#1E90FF')
            elif periodo.tipo == "CTX":
                ax.barh(processo.id, duracao, left=periodo.inicio, color='#FFD700', edgecolor='#FFD700')
                ax.text(periodo.inicio + duracao/2, processo.id, 'CTX', ha='center', va='center', fontsize=8)
            
        # Preencher períodos de espera
        if processo.processamentos:
            tempo_atual = processo.chegada
            for periodo in processo.processamentos:
                if periodo.inicio > tempo_atual:
                    # Período de espera
                    duracao_espera = periodo.inicio - tempo_atual
                    ax.barh(processo.id, duracao_espera, left=tempo_atual, color='#FF6347', edgecolor='#FF6347')
                tempo_atual = periodo.fim

        espera = processo.get_espera()
        turnaround = processo.get_turnaround()
        ax.text(tempo_maximo + 0.5, processo.id, f"Execução: {turnaround:.1f}\nEspera: {espera:.1f}", va='center')

    ax.set_xlabel('Tempo')
    ax.set_title(nome_processo)

    execucao_patch = mpatches.Patch(color='#1E90FF', label=f'Execução: Média Execução = {media_execucao:.2f}')
    espera_patch = mpatches.Patch(color='#FF6347', label=f'Espera: Média Espera = {media_espera:.2f}')
    ctx_patch = mpatches.Patch(color='#FFD700', label='Troca de Contexto')
    ax.legend(handles=[execucao_patch, espera_patch, ctx_patch], loc='lower right', bbox_to_anchor=(1, -0.35))

    centralizar_grafico(fig)
    plt.show()