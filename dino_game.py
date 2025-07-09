from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# Mapeamento dos tipos de obstáculo para números
# Você pode ajustar conforme os valores que aparecerem na execução
TIPOS_OBSTACULO = {
    "CACTUS_SMALL": 0,
    "CACTUS_LARGE": 1,
    "PTERODACTYL": 2,
    # Se aparecer mais tipos, pode adicionar aqui
}
def dino_morreu(driver):
    """Retorna True se o Dino colidiu (morreu), False caso contrário."""
    return driver.execute_script("return Runner.instance_.crashed;")

def setup_driver():
    """Configura o WebDriver e abre o jogo."""
    driver = webdriver.Firefox()
    driver.get("https://trex-runner.com/")
    return driver

def wait_for_game_to_load(driver):
    """Espera o jogo carregar completamente."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "runner-canvas"))
    )

def perform_jump(driver):
    """Simula um pulo no jogo do Dino."""
    driver.execute_script("Runner.instance_.tRex.startJump();")

def collect_game_data(driver):
    """Coleta dados do jogo como pontuação, velocidade e informações do obstáculo."""
    score = driver.execute_script("return Runner.instance_.distanceMeter.getActualDistance(Runner.instance_.distanceRan);")
    obstacles = driver.execute_script("return Runner.instance_.horizon.obstacles;")
    current_speed = float(driver.execute_script("return Runner.instance_.currentSpeed;"))
    
    obstacle_info = {"position": None, "height": None, "type": -1}
    
    if obstacles:
        closest_obstacle = obstacles[0]
        obstacle_info["position"] = closest_obstacle['xPos']
        obstacle_info["height"] = closest_obstacle['yPos']
        
        # Capturar o tipo do obstáculo
        tipo_js = None
        
        # Tente pegar o tipo do obstáculo pelo JS (pode ser 'type' ou 'typeConfig.type')
        if 'type' in closest_obstacle:
            tipo_js = closest_obstacle['type']
        elif 'typeConfig' in closest_obstacle and 'type' in closest_obstacle['typeConfig']:
            tipo_js = closest_obstacle['typeConfig']['type']
        
        if tipo_js is not None:
            # Mapear para número, default -1 se não encontrado
            obstacle_info["type"] = TIPOS_OBSTACULO.get(tipo_js.upper(), -1)
    
    return score, current_speed, obstacle_info

def main():
    driver = setup_driver()
    
    try:
        wait_for_game_to_load(driver)
        time.sleep(5)  # Espera antes de começar
        
        perform_jump(driver)
        
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            score, current_speed, obstacle_info = collect_game_data(driver)
            
            sys.stdout.write("\r" +
                             f"Pontuação: {score:.2f} | " +
                             f"Velocidade atual do Dino: {current_speed:.2f} | " +
                             f"Posição do obstáculo mais próximo: {obstacle_info['position']} | " +
                             f"Altura do obstáculo mais próximo: {obstacle_info['height']} | " +
                             f"Tipo do obstáculo: {obstacle_info['type']} | " +
                             f"Tempo decorrido: {elapsed_time:.1f}s")
            sys.stdout.flush()
            
            time.sleep(0.1)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
