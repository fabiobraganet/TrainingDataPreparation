import os

# Caminho inicial
base_path = '/home/fabio/dev/repos/TrainingDataPreparation'

# Função para imprimir a estrutura de diretórios e arquivos
def print_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_path = os.path.join(root, f)
            if f.endswith('.py'):
                print('\n\n', end='')  # Pula duas linhas antes
                print(f'{subindent}{f}')
                with open(file_path, 'r') as file:
                    print(file.read())
                print('\n\n', end='')

# Imprimir a estrutura de diretórios e arquivos a partir do caminho base
print_directory_structure(base_path)
