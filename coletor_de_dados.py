import csv
import time
import keyboard  # pip install keyboard
from dino_game import setup_driver, wait_for_game_to_load, collect_game_data, perform_jump

def main():
    x = input("Digite o número para nomear o arquivo dados_para_treino_x.csv: ").strip()
    nome_arquivo = f'dados_para_treino_{x}.csv'

    driver = setup_driver()
    wait_for_game_to_load(driver)
    time.sleep(3)  # Tempo para o jogador se preparar

    abaixado = False  # Estado de abaixado

    with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv, delimiter=';')
        writer.writerow(['distancia', 'altura', 'velocidade', 'tipo', 'acao'])

        print(">> Captura iniciada.")
        print(">> Use SPACE ou SETA ↑ para pular, SETA ↓ para abaixar, SETA ↑ (após abaixar) para voltar ao normal.")
        print(">> Pressione ESC para encerrar.")

        try:
            while True:
                if keyboard.is_pressed('esc'):
                    print("\n>> Encerrando captura...")
                    break

                distancia, velocidade, obstaculo = collect_game_data(driver)
                altura = obstaculo['height'] if obstaculo['height'] is not None else 0
                
                # Pega o tipo do obstáculo e converte em número (0 se nenhum)
                tipo_str = obstaculo.get('type', None)
                tipo_num = 0
                if tipo_str is not None:
                    # Exemplo simples: converte string em hash numérico pequeno
                    tipo_num = abs(hash(tipo_str)) % 1000

                acao = 0  # padrão: nada

                # Captura imediata ao abaixar (se ainda não estava abaixado)
                if keyboard.is_pressed('down') and not abaixado:
                    abaixado = True
                    acao = -1
                    writer.writerow([
                        f"{distancia:.3f}".replace('.', ','),
                        f"{altura}".replace('.', ','),
                        f"{velocidade:.3f}".replace('.', ','),
                        tipo_num,
                        acao
                    ])
                    print(f"\r(ABAIXAR) Dist: {distancia:.3f} Alt: {altura} Vel: {velocidade:.3f} Tipo: {tipo_num} Ação: {acao}    ", end='')
                    time.sleep(0.1)  # evitar múltiplos registros instantâneos

                # Soltar abaixar (seta ↑ após abaixado)
                elif keyboard.is_pressed('up') and abaixado:
                    abaixado = False
                    acao = 0
                    writer.writerow([
                        f"{distancia:.3f}".replace('.', ','),
                        f"{altura}".replace('.', ','),
                        f"{velocidade:.3f}".replace('.', ','),
                        tipo_num,
                        acao
                    ])
                    print(f"\r(SOLTAR ABAIXAR) Dist: {distancia:.3f} Alt: {altura} Vel: {velocidade:.3f} Tipo: {tipo_num} Ação: {acao}    ", end='')
                    time.sleep(0.1)

                # Captura imediata ao pular (se não estiver abaixado)
                elif (keyboard.is_pressed('space') or keyboard.is_pressed('up')) and not abaixado:
                    acao = 1
                    perform_jump(driver)
                    writer.writerow([
                        f"{distancia:.3f}".replace('.', ','),
                        f"{altura}".replace('.', ','),
                        f"{velocidade:.3f}".replace('.', ','),
                        tipo_num,
                        acao
                    ])
                    print(f"\r(PULO) Dist: {distancia:.3f} Alt: {altura} Vel: {velocidade:.3f} Tipo: {tipo_num} Ação: {acao}    ", end='')
                    time.sleep(0.1)

                else:
                    # Estado normal (não abaixado, não pulando)
                    if abaixado:
                        acao = -1
                    else:
                        acao = 0
                    writer.writerow([
                        f"{distancia:.3f}".replace('.', ','),
                        f"{altura}".replace('.', ','),
                        f"{velocidade:.3f}".replace('.', ','),
                        tipo_num,
                        acao
                    ])
                    print(f"\rDist: {distancia:.3f} Alt: {altura} Vel: {velocidade:.3f} Tipo: {tipo_num} Ação: {acao}    ", end='')

                time.sleep(0.5)  # espera maior para reduzir excesso de dados 0

        finally:
            driver.quit()

if __name__ == "__main__":
    main()
