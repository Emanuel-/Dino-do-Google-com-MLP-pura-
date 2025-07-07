import numpy as np
import copy

# Funções de ativação
def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivadas das funções de ativação
def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# MLP com 3 entradas e 3 saídas
class MLP:
    def __init__(self):
        self.W1 = np.random.randn(4, 3)  # 4 neurônios na camada oculta
        self.b1 = np.zeros((4, 1))
        self.W2 = np.random.randn(3, 4)  # 3 neurônios na saída
        self.b2 = np.zeros((3, 1))
    
    def forward(self, X):
        self.z1 = np.dot(self.W1, X) + self.b1
        self.a1 = relu(self.z1)
        
        self.z2 = np.dot(self.W2, self.a1) + self.b2
        self.a2 = sigmoid(self.z2)
        
        return self.a2
    
    def mutate(self, mutation_rate=0.01):
        mutation_matrix_W1 = np.random.uniform(-2, 2, self.W1.shape) * mutation_rate
        mutation_matrix_W2 = np.random.uniform(-2, 2, self.W2.shape) * mutation_rate
        self.W1 += mutation_matrix_W1
        self.W2 += mutation_matrix_W2

# Função para executar a iteração
def evolutionary_step(mlps, X):
    # Avaliar as 4 MLPs
    outputs = [mlp.forward(X) for mlp in mlps]
    
    for i, output in enumerate(outputs):
        print(f"MLP {i+1} - Saída: \n{output}\n")
    
    # Pontuar as MLPs sem limite superior
    scores = []
    for i in range(4):
        score = float(input(f"Pontue a MLP {i+1} (sem limite): "))
        scores.append(score)
    
    # Selecionar a MLP com maior pontuação
    best_mlp_index = np.argmax(scores)
    best_mlp = mlps[best_mlp_index]
    
    # Clonar e mutar
    new_mlps = [copy.deepcopy(best_mlp) for _ in range(4)]
    for mlp in new_mlps:
        mlp.mutate()
    
    return new_mlps

# Função para obter entradas do usuário
def get_user_input():
    X = []
    print("Digite as entradas (cada entrada separada por espaço):")
    for i in range(3):
        line = input(f"Entrada {i+1}: ").strip()
        values = list(map(float, line.split()))
        if len(values) != 1:
            raise ValueError("Por favor, forneça exatamente uma entrada por linha.")
        X.append(values[0])
    return np.array(X).reshape(3, 1)

# Inicializar 4 MLPs
mlps = [MLP() for _ in range(4)]

# Obter entradas do usuário
X = get_user_input()

# Processo evolutivo
while True:
    mlps = evolutionary_step(mlps, X)
    
    # Perguntar ao usuário se deseja continuar
    continuar = input("Deseja continuar? (s/n): ")
    if continuar.lower() != 's':
        break
