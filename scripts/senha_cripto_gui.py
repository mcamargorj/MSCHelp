import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

def criptografar():
    chave = Fernet.generate_key()
    cipher_suite = Fernet(chave)

    senha = senha_entry.get()

    senha_criptografada = cipher_suite.encrypt(senha.encode()).decode()

    messagebox.showinfo("Senha Criptografada", f"Chave: {chave.decode()}\nSenha Criptografada: {senha_criptografada}")

def descriptografar():
    chave = chave_entry.get()
    cipher_suite = Fernet(chave.encode())

    senha_criptografada = senha_entry.get()

    senha = cipher_suite.decrypt(senha_criptografada.encode()).decode()
    messagebox.showinfo("Senha Descriptografada", f"A senha descriptografada é: {senha}")

def mudar_para_criptografar():
    root.title("Criptografar Senha")
    revelar_button.config(text="Criptografar", command=criptografar)

def mudar_para_descriptografar():
    root.title("Descriptografar Senha")
    revelar_button.config(text="Descriptografar", command=descriptografar)

# Criar janela principal
root = tk.Tk()
root.title("Criptografar Senha")

# Frame para os inputs
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Label e Entry para chave de criptografia
chave_label = tk.Label(frame, text="Chave de Criptografia:")
chave_label.grid(row=0, column=0, sticky="w")
chave_entry = tk.Entry(frame)
chave_entry.grid(row=0, column=1)

# Label e Entry para senha criptografada
senha_label = tk.Label(frame, text="Senha:")
senha_label.grid(row=1, column=0, sticky="w")
senha_entry = tk.Entry(frame)
senha_entry.grid(row=1, column=1)

# Botões para selecionar Criptografar/Descriptografar
crip_button = tk.Button(root, text="Criptografar", command=mudar_para_criptografar)
crip_button.pack(side=tk.LEFT, padx=10)
descrip_button = tk.Button(root, text="Descriptografar", command=mudar_para_descriptografar)
descrip_button.pack(side=tk.LEFT, padx=10)

# Botão para executar a ação selecionada
revelar_button = tk.Button(root, text="Criptografar", command=criptografar)
revelar_button.pack()

# Rodar aplicação
root.mainloop()
