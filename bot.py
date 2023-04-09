import random

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

def check_win(secret_word, word, guessed):
    if word == secret_word:
        guessed = True
        print("GANASTE!😃")

    return guessed

def filter_words(secret_word, word, words):
    for i, character in enumerate(word):
        # Filtra las palabras que contienen las letras correctas en la misma posición.
        if character == secret_word[i]:
            words = list(filter(lambda x: x[i] == character, words))

        # Elimina las palabras que tengan letras que no estén en la palabra secreta.
        elif character not in secret_word:
            words = list(filter(lambda x: character not in x, words))

        # Elimina las palabras que no tengan letras que están en la palabra secreta y que estén en diferente posición.
        elif character in secret_word:
            words = list(filter(lambda x: character in x and x[i] != character, words))

    return words

def start_game():
    chances = 6
    guessed = False
    words = add_words()
    secret_word = choose_random_word(words)
    print(f"Secret word: {secret_word.upper()}\n")
    while chances > 0 and not guessed:
        print(f"Palabras restantes: {len(words)} - Intentos restantes: {chances}")
        word = choose_random_word(words)
        print(f"Palabra elegida: {word.upper()}\n")  
        guessed = check_win(secret_word, word, guessed)
        words = filter_words(secret_word, word, words)
        chances -= 1
    
    if not guessed: 
        print("PERDISTE!😭")

    
if __name__ == "__main__":
    start_game()