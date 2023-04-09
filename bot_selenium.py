from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random

driver = webdriver.Chrome()
driver.get("https://lapalabradeldia.com")

button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div/div[2]/div[1]/button")))
button.click()

words = []

def add_words():
    try:
        file = open("words.txt", "r", encoding="utf-8")
    except IOError:
        print("Ocurrió un error al abrir el archivo")
    else:
        for linea in file:
            word = linea.strip()
            words.append(word)
        return words
    finally:
        file.close() 

def choose_random_word(array):
    return random.choice(array)

def type_word(word):
    actions = ActionChains(driver)
    for c in word:
        actions.send_keys(c)
    time.sleep(2)
    actions.perform()
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)

def check_win(colors, guessed):
    if colors.count("green") == 5:
        guessed = True
        print("GANASTE!😃")

    return guessed

def filter_words(colors, word, words):
    for i, character in enumerate(word):
        # Filtra las palabras que contienen las letras correctas en la misma posición.
        if colors[i] == "green":
            words = list(filter(lambda x: x[i] == character, words))

        # Elimina las palabras que tengan letras que no estén en la palabra secreta.
        elif colors[i] == "gray":
            words = list(filter(lambda x: character not in x, words))

        # Elimina las palabras que no tengan letras que están en la palabra secreta y que estén en diferente posición.
        elif colors[i] == "yellow":
            words = list(filter(lambda x: character in x and x[i] != character, words))

    return words

def start_game():
    chances = 6
    guessed = False
    words = add_words()
    i = 0
    while chances > 0 and not guessed:
        colors = []
        print(f"Palabras restantes: {len(words)} - Intentos restantes: {chances}")
        word = choose_random_word(words)
        type_word(word)
        # tablero
        board = driver.find_element(By.ID, "board")
        # todas las palabras
        rows = board.find_elements(By.CLASS_NAME, "mui-style-e8rekw")
        # palabra
        palabra = rows[i].find_elements(By.CLASS_NAME, "react-card-flip")
        i += 1
        # color de la letra
        for letra in palabra:
            z = letra.find_element(By.CLASS_NAME, "react-card-flipper")
            x = z.find_element(By.CLASS_NAME, "react-card-back")
            j = x.find_element(By.CLASS_NAME, "MuiBox-root")
            color = j.get_attribute("class").split(" ")[2]
            if color == "mui-style-19klofl":
                color = "gray"
            elif color == "mui-style-1s62ug5":
                color = "yellow"
            else:
                color = "green"
            colors.append(color)

        guessed = check_win(colors, guessed)
        words = filter_words(colors, word, words)
        chances -= 1

    if not guessed: 
        print("PERDISTE!😭")

if __name__ == "__main__":
    start_game()

time.sleep(60)