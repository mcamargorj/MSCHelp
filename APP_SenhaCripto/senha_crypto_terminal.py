# Este código foi escrito por [MSCHelp]
# Data: [19/05/23]
# Descrição: Criptografar uma palavra ou senha, irá criar uma chave e uma senha criptografada e depois a opção para descriptografar.
from cryptography.fernet import Fernet

def criptografar():
    chave = Fernet.generate_key()
    cipher_suite = Fernet(chave)

    senha = input("Digite a senha que deseja criptografar: ")

    senha_criptografada = cipher_suite.encrypt(senha.encode()).decode()

    print(f"Chave: {chave.decode()}")
    print(f"Senha Criptografada: {senha_criptografada}")

def descriptografar():
    chave = input("Digite a chave de criptografia: ")
    cipher_suite = Fernet(chave.encode())

    senha_criptografada = input("Digite a senha criptografada: ")

    senha = cipher_suite.decrypt(senha_criptografada.encode()).decode()
    print(f"A senha descriptografada é: {senha}")

def main():
    escolha = input("Digite '1' para criptografar ou '2' para descriptografar: ")

    if escolha == '1':
        criptografar()
    elif escolha == '2':
        descriptografar()
    else:
        print("Escolha inválida. Digite '1' para criptografar ou '2' para descriptografar.")

if __name__ == "__main__":
    main()
