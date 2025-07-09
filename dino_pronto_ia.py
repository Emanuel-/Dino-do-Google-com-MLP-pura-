import pandas as pd
import time
import pyautogui
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from dino_game import setup_driver, dino_morreu, wait_for_game_to_load, collect_game_data

def executar_acao(acao):
    if acao == 1:
        pyautogui.press('space')
    elif acao == -1:
        pyautogui.keyDown('down')
        time.sleep(0.3)
        pyautogui.keyUp('down')

# === ETAPA 1: Treinamento ===

# 1. Carregar e tratar os dados
df = pd.read_csv("dados_gerados.csv", sep=";")
df = df.replace(',', '.', regex=True).astype(float)

X = df[['distancia', 'altura', 'velocidade', 'tipo']]
y = df['acao']

# 2. Normalizar
scaler = StandardScaler()
X_normalizado = scaler.fit_transform(X)

# 3. Dividir e treinar
X_train, X_test, y_train, y_test = train_test_split(X_normalizado, y, test_size=0.2, random_state=42)

modelo = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=500, random_state=42)
modelo.fit(X_train, y_train)

# 4. Avaliar
y_pred = modelo.predict(X_test)

print("\n📑 Relatório de classificação:")
print(classification_report(y_test, y_pred, zero_division=0))
print("📈 Acurácia:", f"{accuracy_score(y_test, y_pred):.2%}")
print("📉 Matriz de confusão:")
print(confusion_matrix(y_test, y_pred))

# 5. Perguntar se pode prosseguir
resposta = input("\n🚀 Deseja iniciar o jogo com este modelo? (sim/não): ").strip().lower()
if resposta != "sim":
    print("❌ Execução interrompida.")
    exit()

# === ETAPA 2: Jogar com a IA ===

def main():
    driver = setup_driver()
    wait_for_game_to_load(driver)
    time.sleep(2)

    print("🎮 Iniciando jogo controlado pela IA...")
    pyautogui.press('space')
    time.sleep(0.5)

    try:
        while True:
            if dino_morreu(driver):
                print("\n💀 O Dino morreu!")
                time.sleep(5)

            _, velocidade, obstaculo = collect_game_data(driver)
            distancia = obstaculo['position'] if obstaculo['position'] is not None else 0
            altura = obstaculo['height'] if obstaculo['height'] is not None else 0
            tipo = obstaculo['type']

            entrada = pd.DataFrame([[distancia, altura, velocidade, tipo]],
                                   columns=['distancia', 'altura', 'velocidade', 'tipo'])

            entrada_normalizada = scaler.transform(entrada)
            acao = int(modelo.predict(entrada_normalizada)[0])

            executar_acao(acao)
            time.sleep(0.001)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
