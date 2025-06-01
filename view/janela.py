import copy
import tkinter as tk
from tkinter import messagebox, ttk

from control import simular_escalonamento
from model import Processo
from model.prioridade import Prioridade
from view import grafico_processos

processos = []

def adicionar_processo():
    try:
        chegada = int(entrada_chegada.get())
        duracao = int(entrada_duracao.get())
        prioridade_num = int(entrada_prioridade.get())
        
        novo_id = max(processo.id for processo in processos) + 1 if processos else 1

        processo = Processo(novo_id, chegada, duracao, Prioridade(prioridade_num))
        processos.append(processo)

        lista_processos.insert(tk.END, f"ID: {novo_id}, Chegada: {chegada}, Duração: {duracao}, Prioridade: {prioridade_num}")

        entrada_chegada.delete(0, tk.END)
        entrada_duracao.delete(0, tk.END)
        entrada_prioridade.delete(0, tk.END)
    except ValueError as e:
        messagebox.showerror("Erro", "Valores inválidos. Use apenas números inteiros positivos.")

def remover_processo():
    if len(lista_processos.curselection()):
        index_selecionado = lista_processos.curselection()[0]
        lista_processos.delete(index_selecionado)

        processo_selecionado = processos[index_selecionado]
        processos.remove(processo_selecionado)
    elif processos:
        processos.pop()
        lista_processos.delete(lista_processos.size() - 1)

def editar_processo():
    if len(lista_processos.curselection()):
        index_selecionado = lista_processos.curselection()[0]
        processo_selecionado = processos[index_selecionado]

        entrada_chegada.delete(0, tk.END)
        entrada_chegada.insert(0, processo_selecionado.chegada)
        entrada_duracao.delete(0, tk.END)
        entrada_duracao.insert(0, processo_selecionado.duracao)
        entrada_prioridade.delete(0, tk.END)
        entrada_prioridade.insert(0, processo_selecionado.prioridade.numero)

        lista_processos.delete(index_selecionado)
        processos.pop(index_selecionado)

def form_submit():
    try:
        processos_submit = copy.deepcopy(processos)
        algoritmo = algoritmo_var.get()
        quantum = quantum_entry.get()
        ctx_time = float(ctx_entry.get())

        media_execucao, media_espera, nome_processo = simular_escalonamento(processos_submit, algoritmo, quantum, ctx_time)

        grafico_processos(processos_submit, media_execucao, media_espera, nome_processo)
    except Exception as e:
        messagebox.showerror("Erro", e)

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    janela.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')

def habilitar_quantum():
    if algoritmo_var.get() == 3:
        quantum_label.pack(padx=20, pady=5)
        quantum_entry.pack(padx=20, pady=5)
    else:
        quantum_label.pack_forget()
        quantum_entry.pack_forget()

def criar_janela():
    global entrada_chegada, entrada_duracao, entrada_prioridade, lista_processos, algoritmo_var, quantum_label, quantum_entry, ctx_label, ctx_entry
    janela = tk.Tk()
    janela.title("Simulador de Escalonamento")
    janela.configure(bg="#FFFFFF")
    janela.resizable(False, False)

    centralizar_janela(janela, 750, 750)

    algoritmo_var = tk.IntVar()

    processos_label = tk.Label(janela, text="Defina os processos", 
                    font=("Calibri Light", 18, "bold"),
                    fg="#0D0D0D", 
                    bg="#FFFFFF")
    processos_label.pack()

    input_form_frame = tk.Frame(janela, bg="#FFFFFF")
    input_form_frame.pack(pady=10)

    tk.Label(input_form_frame, text="Chegada:", font=("Calibri", 12), bg="#FFFFFF").grid(row=0, column=0, padx=5)
    entrada_chegada = tk.Entry(input_form_frame, bd=2, highlightbackground="#2C2C2C", highlightcolor="#2C2C2C", font=("Calibri", 12), justify="center")
    entrada_chegada.grid(row=1, column=0, padx=5, pady=5)

    tk.Label(input_form_frame, text="Duração:", font=("Calibri", 12), bg="#FFFFFF").grid(row=0, column=1, padx=5)
    entrada_duracao = tk.Entry(input_form_frame, bd=2, highlightbackground="#2C2C2C", highlightcolor="#2C2C2C", font=("Calibri", 12), justify="center")
    entrada_duracao.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_form_frame, text="Prioridade:", font=("Calibri", 12), bg="#FFFFFF").grid(row=0, column=2, padx=5)
    entrada_prioridade = tk.Entry(input_form_frame, bd=2, highlightbackground="#2C2C2C", highlightcolor="#2C2C2C", font=("Calibri", 12), justify="center")
    entrada_prioridade.grid(row=1, column=2, padx=5, pady=5)

    buttons_form_frame = tk.Frame(janela, bg="#FFFFFF")
    buttons_form_frame.pack(pady=10)

    tk.Button(buttons_form_frame, text="Adicionar Processo", command=adicionar_processo, font=("Calibri", 12), fg="#FFFFFF", bg="#4682B4", activeforeground="#FFFFFF", activebackground="#375579").grid(row=0, column=0, padx=5)
    tk.Button(buttons_form_frame, text="Remover Processo", command=remover_processo, font=("Calibri", 12), fg="#FFFFFF", bg="#B74343", activeforeground="#FFFFFF", activebackground="#934B4B").grid(row=0, column=1, padx=5)
    tk.Button(buttons_form_frame, text="Editar Processo", command=editar_processo, font=("Calibri", 12), fg="#FFFFFF", bg="#44B649", activeforeground="#FFFFFF", activebackground="#3E8E40").grid(row=0, column=2, padx=5)

    lista_processos = tk.Listbox(janela, width=50, height=5, bd=2, highlightbackground="#2C2C2C", highlightcolor="#2C2C2C", font=("Calibri", 12), justify="center")
    lista_processos.pack(padx=10, pady=10)

    algoritmo_label = tk.Label(janela, text="Escolha o algoritmo de escalonamento", 
                    font=("Calibri Light", 18, "bold"),
                    fg="#0D0D0D", 
                    bg="#FFFFFF")
    algoritmo_label.pack()

    radio_frame = tk.Frame(janela, bg="#FFFFFF")
    radio_frame.pack(pady=10)

    tk.Radiobutton(radio_frame, text="1. FCFS", variable=algoritmo_var, value=1, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=0, column=0, padx=40)
    tk.Radiobutton(radio_frame, text="2. SJF", variable=algoritmo_var, value=2, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=1, column=0, padx=40)
    tk.Radiobutton(radio_frame, text="3. Round Robin", variable=algoritmo_var, value=3, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=2, column=0, padx=40)
    tk.Radiobutton(radio_frame, text="4. SRTF", variable=algoritmo_var, value=4, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=3, column=0, padx=40)
    tk.Radiobutton(radio_frame, text="5. Prioridade cooperativo", variable=algoritmo_var, value=5, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=0, column=1, padx=40)
    tk.Radiobutton(radio_frame, text="6. Prioridade preemptivo", variable=algoritmo_var, value=6, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=1, column=1, padx=40)
    tk.Radiobutton(radio_frame, text="7. Inversão de prioridade", variable=algoritmo_var, value=7, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=2, column=1, padx=40)
    tk.Radiobutton(radio_frame, text="8. Herança de prioridade", variable=algoritmo_var, value=8, command=habilitar_quantum, font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF").grid(row=3, column=1, padx=40)
    
    quantum_label = tk.Label(janela, text="Informe o quantum para Round Robin:", font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF")
    quantum_entry = tk.Entry(janela, bd=2, highlightbackground="#2C2C2C", highlightcolor="#2C2C2C", font=("Calibri", 12), justify="center")
    quantum_entry.insert(0, "2")

    ctx_label = tk.Label(janela, text="Tempo de troca de contexto (s):", font=("Calibri", 14), fg="#2C2C2C", bg="#FFFFFF")
    ctx_entry = tk.Entry(janela, bd=2, highlightbackground="#2C2C2C", highlightcolor="#2C2C2C", font=("Calibri", 12), justify="center")
    ctx_entry.insert(0, "0.5")
    ctx_label.pack(padx=20, pady=5)
    ctx_entry.pack(padx=20, pady=5)

    tk.Button(janela, text="Simular", command=form_submit, font=("Calibri", 16), fg="#FFFFFF", bg="#FFA500", activeforeground="#FFFFFF", activebackground="#CC8400").pack(padx=20, pady=20)

    janela.mainloop()