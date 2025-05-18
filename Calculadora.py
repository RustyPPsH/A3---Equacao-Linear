from ast import Import

import tkinter as tk
from tkinter import messagebox

# === Função principal de eliminação de Gauss com pivoteamento parcial ===
def gauss_elimination(A, B):
    """
    Resolve o sistema Ax = B aplicando eliminação de Gauss
    com pivoteamento parcial.
    A: matriz de coeficientes (lista de listas)
    B: vetor de termos independentes (lista)
    Retorna lista X com a solução, ou None se o sistema for singular.
    """
    n = len(A)  # número de equações/variáveis

    # ===== Etapa de eliminação (forma de matriz triangular superior) =====
    for i in range(n):
        # 1) Pivoteamento parcial: escolhe a linha com maior valor absoluto
        #    na coluna i para evitar divisão por valores muito pequenos.
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]  # troca de linhas em A
        B[i], B[max_row] = B[max_row], B[i]  # troca correspondente em B

        # 2) Se o pivô for zero (ou muito próximo), não há solução única
        if abs(A[i][i]) < 1e-12:
            return None

        # 3) Para cada linha abaixo da i-ésima, elimina o coeficiente A[j][i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]  # fator de eliminação
            # Subtrai factor * linha i da linha j, para todas as colunas
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            B[j] -= factor * B[i]  # ajusta também o termo independente

    # ===== Etapa de retro-substituição (back-substitution) =====
    X = [0 for _ in range(n)]  # vetor solução inicializado
    # Começa da última linha até a primeira
    for i in range(n-1, -1, -1):
        # calcula soma dos A[i][j]*X[j] para j > i
        sum_ax = sum(A[i][j] * X[j] for j in range(i+1, n))
        # resolve X[i] = (B[i] - soma) / pivô A[i][i]
        X[i] = (B[i] - sum_ax) / A[i][i]

    return X  # retorna o vetor solução


# === Função que faz a interface reagir ao botão "Resolver Sistema" ===
def solve():
    try:
        # 1) Lê o tamanho do sistema (n)
        size = int(entry_size.get())
        # 2) Lê os coeficientes A[i][j] de cada entrada na interface
        coefficients = [
            [float(entries[i][j].get()) for j in range(size)]
            for i in range(size)
        ]
        # 3) Lê o vetor de termos independentes B[i]
        independent_terms = [
            float(entry_b[i].get())
            for i in range(size)
        ]

        # 4) Chama a função de Gauss para calcular a solução
        result = gauss_elimination(coefficients, independent_terms)

        # 5) Exibe resultado ou erro, conforme retorno
        if result is None:
            messagebox.showerror(
                "Erro",
                "O sistema não possui solução única (é singular ou indeterminado)."
            )
        else:
            # Formata a solução com 4 casas decimais
            solution = "\n".join(
                f"x{i+1} = {result[i]:.4f}" for i in range(size)
            )
            messagebox.showinfo("Solução", solution)

    except ValueError:
        # Tratamento de erro caso algum campo não tenha sido preenchido corretamente
        messagebox.showerror(
            "Erro",
            "Verifique se todos os campos estão preenchidos corretamente."
        )


# === Função que gera dinamicamente os campos de entrada na interface ===
def create_matrix_entries():
    global entries, entry_b

    # 1) Limpa quaisquer widgets antigos dentro do frame
    for widget in frame_entries.winfo_children():
        widget.destroy()

    # 2) Inicializa as listas que armazenarão os Entry widgets
    entries = []   # para coeficientes A
    entry_b = []   # para termos independentes B

    # 3) Lê quantas variáveis/equações o usuário quer
    size = int(entry_size.get())

    # --- Cabeçalho das colunas ---
    # Rótulos x1, x2, ..., xn
    for j in range(size):
        tk.Label(
            frame_entries,
            text=f"x{j+1}",
            font=('Arial', 10, 'bold'),
            width=5
        ).grid(row=0, column=j+1, padx=2, pady=2)
    # Rótulo para o termo independente 'b'
    tk.Label(
        frame_entries,
        text="b",
        font=('Arial', 10, 'bold'),
        width=5
    ).grid(row=0, column=size+1, padx=2, pady=2)

    # --- Linhas de entradas das equações ---
    for i in range(size):
        # Rótulo Eq1, Eq2, ..., Eqn
        tk.Label(
            frame_entries,
            text=f"Eq{i+1}",
            font=('Arial', 10, 'bold'),
            width=5
        ).grid(row=i+1, column=0, padx=2, pady=2)

        # Campos de entrada para coeficientes A[i][j]
        row_entries = []
        for j in range(size):
            e = tk.Entry(
                frame_entries,
                width=5,
                justify='center'
            )
            e.grid(row=i+1, column=j+1, padx=2, pady=2)
            row_entries.append(e)
        entries.append(row_entries)  # guarda a linha de coeficientes

        # Campo de entrada para termo independente B[i]
        e_b = tk.Entry(
            frame_entries,
            width=5,
            justify='center'
        )
        e_b.grid(row=i+1, column=size+1, padx=2, pady=2)
        entry_b.append(e_b)  # guarda o campo de B


# === Configuração da janela principal (Tkinter) ===
root = tk.Tk()
root.title("Resolução de Sistemas Lineares")

# Rótulo e campo para tamanho do sistema
tk.Label(root, text="Número de incógnitas/equações:").pack()
entry_size = tk.Entry(root)
entry_size.pack()

# Botão que gera os campos de entrada
tk.Button(root, text="Criar Sistema", command=create_matrix_entries).pack()

# Frame que conterá dinamicamente os campos das equações
frame_entries = tk.Frame(root)
frame_entries.pack()

# Botão que executa a resolução via Gauss
tk.Button(root, text="Resolver Sistema", command=solve).pack()

# Rodapé
tk.Label(root, text="Calculadora de Equações Lineares por Erick Vieira / Rafael Sonoki").pack(pady=10)
tk.Label(root, text="Aplica-se formula de Eliminação de Gauss").pack(pady=10)
tk.Label(root, text="A3 - Estruturas Matemáticas").pack(pady=10)

# Inicia o loop de evento da interface
root.mainloop()
# Fim do código
