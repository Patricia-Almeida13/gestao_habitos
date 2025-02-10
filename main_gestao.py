import pandas as pd # usado para manipulação de DataFrame
from datetime import datetime # permite trabalhar com datas e horas
import matplotlib.pyplot as plt #cração de gráficos e visualizar os dados
import numpy as np

#NECESSITA ADD LIGAÇÃO COM SQL PARA QUE EXISTA UMA BASE DE DADOS ACTUALIZADA. ADD FUNÇÃO DE NOTIFICAR O UTILIZADOR

# Dicionário para armazenar os dados dos usuários
usuarios = {}

# Função para criar um novo usuário
def criar_usuario():
    global usuarios
    print("\nCriar Novo Utilizador")
    
    nome_usuario = input("Digite o nome do usuário: ").strip()
    
    # Verifica se o usuário já existe
    if nome_usuario in usuarios:
        print(f"\nUsuário '{nome_usuario}' já existe!")
        return
    
    # Solicita a criação do DataFrame para o novo usuário
    print(f"\nUsuário '{nome_usuario}' criado com sucesso!")
    usuarios[nome_usuario] = pd.DataFrame(columns=["Hábito", "Categoria", "Frequência", "Data de Inicio", "Status"])
    
    print(f"Agora pode começar a adicionar hábitos para o usuário '{nome_usuario}'.")

# Função para selecionar um usuário
def selecionar_usuario():
    global usuarios
    if not usuarios:
        print("\nNenhum usuário cadastrado!")
        return None
    
    print("\nUsuários disponíveis: ", list(usuarios.keys()))
    nome_usuario = input("Digite o nome do usuário que deseja selecionar: ").strip()
    
    if nome_usuario not in usuarios:
        print("\nUsuário não encontrado!")
        return None
    
    print(f"\nUsuário '{nome_usuario}' selecionado com sucesso!")
    return nome_usuario

# Modificar funções que usam o DataFrame de hábitos para trabalhar com o usuário selecionado

def criar_dataframe():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    data = {
        "Hábito": [],
        "Categoria": [],
        "Frequência": [],
        "Data de Inicio": [],
        "Status": [],
    }
    
    while True:
        habito = input("Nome do Hábito: ")
        categoria = input("Categoria (Saúde, Produtividade, Lazer, etc.): ")
        frequencia = input("Frequência (Diária, Semanal, Mensal): ")
        data_registro = input("Data de Inicio (DD/MM/AAAA): ")
        status = input("Status (Concluído, Pendente, Em progresso): ")
        
        try:
            data["Hábito"].append(habito)
            data["Categoria"].append(categoria)
            data["Frequência"].append(frequencia)
            data["Data de Inicio"].append(pd.to_datetime(data_registro, format="%d/%m/%Y"))
            data["Status"].append(status)
        except ValueError:
            print("\nErro! Certifique-se de seguir os formatos indicados.")
            continue
        
        mais = input("\nDeseja adicionar mais algum hábito? (s/n): ").strip().lower()
        if mais != 's':
            break
    
    # Atualizar o DataFrame do usuário
    usuarios[nome_usuario] = pd.DataFrame(data)
    print(f"\nData Frame criado com sucesso para o usuário '{nome_usuario}'!")
    print(usuarios[nome_usuario])


def consultar_dataframe():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    if df.empty:
        print("\nData Frame vazio!")
    else:
        print(df)

# Função para criar um novo hábito
def adicionar_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    habito = input("Nome do Hábito: ")
    categoria = input("Categoria: ")
    frequencia = input("Frequência: ")
    data_registro = input("Data de Inicio (DD/MM/AAAA): ")
    status = input("Status: ")
    
    try:
        nova_linha = {
            "Hábito": habito,
            "Categoria": categoria,
            "Frequência": frequencia,
            "Data de Inicio": pd.to_datetime(data_registro, format="%d/%m/%Y"),
            "Status": status
        }
        df.loc[len(df)] = nova_linha
        usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
        print("\nHábito adicionado com sucesso!")
    except ValueError:
        print("\nErro ao adicionar! Verifique os dados.")

# Função para filtrar hábitos por categoria
def filtrar_por_categoria():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    categoria = input("\nDigite a categoria que deseja filtrar: ")
    filtro = df[df["Categoria"] == categoria]
    print(f"\nHábitos na categoria '{categoria}':")
    print(filtro if not filtro.empty else "\nNenhum hábito encontrado.")

# Função para atualizar o status de um hábito
def atualizar_status():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print(df)
    try:
        indice = int(input("\nIndique o índice do hábito que deseja atualizar: "))
        novo_status = input("\nNovo status (Concluído, Pendente, Em progresso): ")
        
        if indice not in df.index:
            print("\nErro! Índice inválido.")
            return
        
        df.at[indice, "Status"] = novo_status
        usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
        print("\nStatus atualizado com sucesso!")
    except ValueError:
        print("\nErro! Índice inválido.")

    
def exportar_para_excel():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    if df.empty:
        print("\nNão há dados para exportar!")
        return
    
    # Definir o nome do arquivo Excel
    nome_arquivo = f"\n{nome_usuario}_dados_habitos.xlsx"
    
    # Exportar o DataFrame para Excel
    try:
        df.to_excel(nome_arquivo, index=False, engine="openpyxl")
        print(f"\nArquivo Excel gerado com sucesso! O arquivo está em: {nome_arquivo}")
    except Exception as e:
        print(f"\nErro ao gerar o arquivo Excel: {e}")


# Função para remover um hábito
def remover_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return

    global usuarios
    df = usuarios[nome_usuario]
    
    print("\nLista de hábitos disponíveis: ")
    print(df["Hábito"].to_string(index=False))

    habito = input("\nDigite o nome do hábito que deseja remover: ").strip()

    if habito not in df["Hábito"].values:
        print(f"\nErro! O hábito '{habito}' não consta no Data Frame!")
        return

    df.drop(df[df["Hábito"] == habito].index, inplace=True)
    usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
    print(f"\nHábito '{habito}' removido com sucesso!")
    print()

# Função para atualizar um hábito
def atualizar_habito():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print("\nLista de hábitos disponíveis: ")
    print(df["Hábito"].to_string(index=False))

    habito = input("\nDigite o nome do hábito que deseja atualizar: ").strip()

    if habito not in df["Hábito"].values:
        print(f"Erro! O hábito '{habito}' não consta no Data Frame!")
        return

    index_habito = df[df["Hábito"] == habito].index[0]

    print("\nColunas disponíveis para edição:", ", ".join(df.columns))
    coluna = input("\nDigite o nome da coluna que deseja atualizar: ").strip()

    if coluna not in df.columns:
        print(f"\nErro! A coluna '{coluna}' não existe!")
        return

    novo_valor = input(f"\nDigite o novo valor para '{coluna}' no hábito '{habito}': ").strip()

    try:
        tipo_dado = df[coluna].dtype.type
        df.at[index_habito, coluna] = tipo_dado(novo_valor)
        usuarios[nome_usuario] = df  # Atualiza o DataFrame do usuário
        print(f"\nHábito '{habito}' atualizado com sucesso na coluna '{coluna}'!")
    except ValueError:
        print("\nErro! O valor inserido não corresponde ao tipo de dado da coluna.")


# Função para calcular estatísticas personalizadas
def calcular_estatistica_personalizada():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print("Colunas disponíveis:", ", ".join(df.columns))
    coluna = input("Digite o nome da coluna para calcular estatísticas: ").strip()

    if coluna not in df.columns:
        print(f"Erro! A coluna '{coluna}' não existe!")
        return

    print("Opções de Estatística:")
    print("1. Média")
    print("2. Mediana")
    print("3. Desvio Padrão")
    print("4. Mínimo")
    print("5. Máximo")
    escolha = input("Escolha o tipo de estatística (1-5): ").strip()

    try:
        if df[coluna].dtype in ['int64', 'float64']:
            if escolha == "1":
                resultado = df[coluna].mean()
                print(f"Média de {coluna}: {resultado:.2f}")
            elif escolha == "2":
                resultado = df[coluna].median()
                print(f"Mediana de {coluna}: {resultado:.2f}")
            elif escolha == "3":
                resultado = df[coluna].std()
                print(f"Desvio Padrão de {coluna}: {resultado:.2f}")
            elif escolha == "4":
                resultado = df[coluna].min()
                print(f"Valor Mínimo de {coluna}: {resultado}")
            elif escolha == "5":
                resultado = df[coluna].max()
                print(f"Valor Máximo de {coluna}: {resultado}")

    except Exception as e:
        print(f"Erro ao calcular estatística: {e}")
        
def validar_colunas(colunas):
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return False
    
    global usuarios
    df = usuarios[nome_usuario]
    
    for col in colunas:
        if col not in df.columns:
            print(f"\nErro! A coluna '{col}' não existe no DataFrame!")
            return False
    return True

# Função para gerar gráfico de barra
def grafico_barra():
    nome_usuario = selecionar_usuario()
    if nome_usuario is None:
        return
    
    global usuarios
    df = usuarios[nome_usuario]
    
    print("\nColunas do DataFrame: ", list(df.columns))
    x_col = input("Indique a coluna categórica para contagem: ").strip()
    
    if validar_colunas([x_col]):
        contagem = df[x_col].value_counts()  # Conta a frequência de cada categoria
        
        plt.figure(figsize=(10, 6))
        contagem.plot(kind="bar", color="royalblue", edgecolor="black")
        plt.xlabel(x_col)
        plt.ylabel("Frequência")
        plt.title(f"Distribuição de {x_col}")
        plt.xticks(rotation=45)  # Inclina os rótulos para melhor visualização
        plt.grid(axis="y", linestyle="--", alpha=0.7)  # Adiciona linhas de grade no eixo Y
        
        plt.show()
        
while True:
    print("Gestão de Hábitos Pessoais")
    print("\n1. Criar Utilizador")
    print("2. Criar Hábito")
    print("3. Consultar Hábitos")
    print("4. Adicionar Hábito")
    print("5. Filtrar por Categoria")
    print("6. Atualizar Status")
    print("7. Estatísticas")
    print("8. Remover Hábito")
    print("9. Atualizar Hábito")
    print("10. Gráfico de Barra")
    print("11. Exportar Dados para Excel")
    print("12. Sair")
    
    escolha = input("Escolha uma opção: ")
    
    if escolha == "1":
        criar_usuario()
    elif escolha == "2":
        criar_dataframe()
    elif escolha == "3":
        consultar_dataframe()
    elif escolha == "4":
        adicionar_habito()
    elif escolha == "5":
        filtrar_por_categoria()
    elif escolha == "6":
        atualizar_status()
    elif escolha == "7":
        calcular_estatistica_personalizada()
    elif escolha == "8":
        remover_habito() 
    elif escolha == "9":
        atualizar_habito()
    elif escolha == "10":
        grafico_barra()
    elif escolha == "11":  
        exportar_para_excel() 
    elif escolha == "12":
        print("\nObrigado por usar o gestor de hábitos, até logo!")
        break
    else:
        print("\nOpção inválida, tente novamente!")