import tkinter as tk
from tkinter import filedialog, messagebox
from functions import process_stellar_spectrum

def selecionar_imagem():
    """Abre um seletor de arquivos para escolher a imagem."""
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione a imagem do espectro",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png"), ("Todos os arquivos", "*.*")]
    )
    if caminho_arquivo:
        lbl_caminho_imagem.config(text=caminho_arquivo)
        janela.caminho_imagem = caminho_arquivo

def executar_processamento():
    """Coleta os dados da interface e chama a função de processamento."""
    if not hasattr(janela, 'caminho_imagem') or not janela.caminho_imagem:
        messagebox.showwarning("Aviso", "Por favor, selecione uma imagem primeiro.")
        return
    
    try:
        # Coletando e convertendo os valores dos campos de texto
        p1 = float(entry_p1.get())
        l1 = float(entry_l1.get())
        p2 = float(entry_p2.get())
        l2 = float(entry_l2.get())
        
        # Chamando a função do seu arquivo functions.py
        process_stellar_spectrum(janela.caminho_imagem, p1, l1, p2, l2)
        
    except ValueError:
        messagebox.showerror("Erro de Entrada", "Certifique-se de que todos os valores de P1, L1, P2 e L2 são números válidos.")
    except Exception as e:
        messagebox.showerror("Erro na Execução", f"Ocorreu um erro ao processar o espectro:\n{e}")

# --- Configuração da Interface Gráfica (Tkinter) ---

janela = tk.Tk()
janela.title("Analisador de Espectro Estelar")
janela.geometry("450x350")
janela.resizable(False, False)

# Padding padrão para os elementos
pad_options = {'padx': 10, 'pady': 5}

# 1. Seleção de Imagem
frame_imagem = tk.LabelFrame(janela, text="1. Imagem do Espectro")
frame_imagem.pack(fill="x", **pad_options)

btn_selecionar = tk.Button(frame_imagem, text="Procurar Imagem", command=selecionar_imagem)
btn_selecionar.pack(pady=5)

lbl_caminho_imagem = tk.Label(frame_imagem, text="Nenhuma imagem selecionada", fg="gray", wraplength=400)
lbl_caminho_imagem.pack(pady=5)

# 2. Dados de Calibração
frame_calibracao = tk.LabelFrame(janela, text="2. Dados de Calibração")
frame_calibracao.pack(fill="x", **pad_options)

# Grid para organizar os inputs de calibração
tk.Label(frame_calibracao, text="Ponto 1 (Pixel - P1):").grid(row=0, column=0, sticky="e", **pad_options)
entry_p1 = tk.Entry(frame_calibracao, width=10)
entry_p1.grid(row=0, column=1, **pad_options)

tk.Label(frame_calibracao, text="Comprimento 1 (nm - L1):").grid(row=0, column=2, sticky="e", **pad_options)
entry_l1 = tk.Entry(frame_calibracao, width=10)
entry_l1.grid(row=0, column=3, **pad_options)

tk.Label(frame_calibracao, text="Ponto 2 (Pixel - P2):").grid(row=1, column=0, sticky="e", **pad_options)
entry_p2 = tk.Entry(frame_calibracao, width=10)
entry_p2.grid(row=1, column=1, **pad_options)

tk.Label(frame_calibracao, text="Comprimento 2 (nm - L2):").grid(row=1, column=2, sticky="e", **pad_options)
entry_l2 = tk.Entry(frame_calibracao, width=10)
entry_l2.grid(row=1, column=3, **pad_options)

# Valores padrão de exemplo (opcional, facilita os testes)
entry_p1.insert(0, "420")
entry_l1.insert(0, "435.8")
entry_p2.insert(0, "815")
entry_l2.insert(0, "546.1")

# 3. Botão de Execução
btn_executar = tk.Button(janela, text="Processar Espectro", command=executar_processamento, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_executar.pack(pady=20)

# Iniciar o loop da interface
janela.mainloop()