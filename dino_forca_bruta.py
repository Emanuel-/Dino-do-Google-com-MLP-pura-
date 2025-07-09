import random
import time
import pyautogui
from dino_game import setup_driver, dino_morreu, wait_for_game_to_load, collect_game_data, perform_jump

def executar_acao(acao):
    if acao == 1:
        pyautogui.press('space')
    elif acao == -1:
        pyautogui.keyDown('down')
        time.sleep(0.3)
        pyautogui.keyUp('down')


def main():
    driver = setup_driver()
    wait_for_game_to_load(driver)
    time.sleep(2)

    print("🎮 Iniciando jogo com lógica proporcional à velocidade...")
    pyautogui.press('space')  # inicia o jogo
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

            acao = 0  # padrão

            # Fator de antecipação ajustável
            fator_cacto_pequeno = 24
            fator_cacto_grande = 21
            fator_pulo_pterodactilo_alto = 18
            fator_abaixar_pterodactilo_medio = 18

            if int(altura) != 0:
                if tipo == 0:  # Cacto pequeno
                    if distancia < fator_cacto_pequeno * velocidade:
                        acao = 1
                elif tipo == 1:  # Cacto grande
                    if distancia < fator_cacto_grande * velocidade:
                        acao = 1
                elif tipo == 2:  # Pterodáctilo
                    if altura >= 75:  # Pterodáctilo voando baixo
                        if distancia < fator_pulo_pterodactilo_alto * velocidade:
                            acao = 1
                    elif 40 < altura <= 75:  # Pterodáctilo médio
                        if distancia < fator_abaixar_pterodactilo_medio * velocidade:
                            acao = -1
                    else:
                        acao = 0  # Pterodáctilo alto demais, ignora

            executar_acao(acao)

            time.sleep(0.001)  # loop rápido

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
 