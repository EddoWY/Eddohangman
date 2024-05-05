import os

# Define constant variables
import random

HANGMAN_ASCII_ART = """
    Welcome to the game Hangman
      _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/
"""

MAX_TRIES = 6

HANGMAN_PHOTOS = {
    0: """
    x-------x
    """,
    1: """
    x-------x
    |
    |
    |
    |
    |
    """,
    2: """
    x-------x
    |       |
    |       0
    |
    |
    |
    """,
    3: """
    x-------x
    |       |
    |       0
    |       |
    |
    |
    """,
    4: """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
    """,
    5: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
    """,
    6: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
    """
}


def print_out():
    """
    Prints the welcome message and the maximum number of tries.
    """
    print(HANGMAN_ASCII_ART)
    print(MAX_TRIES, "\n")
    print("##############################################################")


def print_hangman(num_of_tries):
    """
    Prints the hangman ASCII art corresponding to the number of incorrect guesses.

    Args:
        num_of_tries (int): The number of incorrect guesses.
    """
    random_colorful_text(HANGMAN_PHOTOS[num_of_tries])


def random_colorful_text(text):
    """
    Prints the given text in a random color.

    Args:
        text (str): The text to be printed.
    """
    colors = [
        '\033[91m',  # Red
        '\033[92m',  # Green
        '\033[93m',  # Yellow
        '\033[94m',  # Blue
        '\033[95m',  # Magenta
        '\033[31m',  # Dark Red
        '\033[32m',  # Dark Green
        '\033[33m',  # Dark Yellow
        '\033[34m',  # Dark Blue
        '\033[35m',  # Dark Magenta
    ]
    end_color = '\033[0m'  # Reset color

    # Choose a random color from the list
    random_color = random.choice(colors)

    # Print text in the random color
    print(random_color + text + end_color)


def print_game_board(word):
    """
    Prints the initial game board with underscores representing hidden letters.

    Args:
        word (str): The secret word.
    """
    game_board = "_ " * len(word)
    print(game_board)


def check_valid_input(letter_guessed, old_letters_guessed):
    """
    Checks if the guessed letter is valid.

    Args:
        letter_guessed (str): The guessed letter.
        old_letters_guessed (list): The list of letters that have already been guessed.

    Returns:
        bool: True if the guessed letter is valid, False otherwise.
    """
    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        print("Not valid letter. Try again.")
        return False
    # Check if the guessed letter has not been guessed before
    elif letter_guessed.lower() in old_letters_guessed:
        print("You already guessed this letter. Try again.")
        return False
    else:
        return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Tries to update the list of guessed letters with the new guessed letter.

    Args:
        letter_guessed (str): The guessed letter.
        old_letters_guessed (list): The list of letters that have already been guessed.

    Returns:
        bool: True if the guessed letter is successfully added to the list, False otherwise.
    """
    if not check_valid_input(letter_guessed, old_letters_guessed):
        random_colorful_text("X")
        random_colorful_text(" -> ".join(sorted(old_letters_guessed)))
        return False
    else:
        old_letters_guessed.append(letter_guessed)
        return True


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Constructs and returns a string representing the current state of the secret word,
    where guessed letters are revealed and unguessed letters are represented by underscores.

    Args:
        secret_word (str): The secret word to be guessed.
        old_letters_guessed (list): A list of letters that have been guessed by the player.

    Returns:
        str: A string representing the current state of the secret word, with guessed letters revealed
             and unguessed letters represented by underscores.
    """
    hidden_word = ""
    for char in secret_word:
        if char.lower() in old_letters_guessed:
            hidden_word += char + " "
        else:
            hidden_word += "_ "
    return hidden_word.strip()


def check_win(secret_word, old_letters_guessed):
    """
    Checks if the player has guessed all the letters in the secret word.

    Args:
        secret_word (str): The secret word.
        old_letters_guessed (list): The list of letters that have already been guessed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    for char in secret_word:
        if char not in old_letters_guessed:
            return False
    return True


def choose_word(file_path, index):
    """
    Chooses a word from the specified file at the given index and writes it to 'found.txt'.

    Args:
        file_path (str): The path to the word file.
        index (int): The index of the word to be chosen.

    Returns:
        tuple: A tuple containing the number of unique words in the file and the chosen word.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # Read words from the file and split them by spaces
    with open(file_path, 'r') as file:
        words = file.read().split()

    # Calculate the number of unique words
    unique_words = len(set(words))

    # Get the word at the specified index (circular indexing)
    word_index = (index - 1) % len(words)
    chosen_word = words[word_index]

    # Write the chosen word to found.txt
    with open('found.txt', 'w') as found_file:
        found_file.write(chosen_word + '\n')

    return unique_words, chosen_word


def main():
    print_out()

    # Test cases
    num_of_tries = MAX_TRIES  # Initialize to MAX_TRIES

    # Choose secret word
    file_path = input("Enter path to word file: ")
    location = int(input("Enter word location: "))  # Convert to integer

    try:
        num_unique_words, secret_word = choose_word(file_path, location)
        print(f"The chosen word contains {num_unique_words} unique letters.")
        print_game_board(secret_word)

        old_letters_guessed = []

        while num_of_tries > 0 and not check_win(secret_word.lower(), old_letters_guessed):
            print("\n")
            print(f"You have {num_of_tries} attempts left.")
            letter_guessed = input("Guess a letter: ").lower()

            # Check if the letter has already been guessed
            if not try_update_letter_guessed(letter_guessed, old_letters_guessed):
                continue

            # Check if the guessed letter is in the secret word
            if letter_guessed not in secret_word:
                print_hangman(MAX_TRIES - num_of_tries + 1)
                print("Incorrect guess!")
                num_of_tries -= 1
            else:
                random_colorful_text(f"Good guess: {show_hidden_word(secret_word, old_letters_guessed)}")

            # Check if the player has won
            if check_win(secret_word, old_letters_guessed):
                print('\033[92m'+"Congratulations! You won!")
                break

        # If all attempts are used and the player hasn't guessed the word, they lose
        if num_of_tries == 0:
            print("Sorry, you ran out of attempts. The word was:", secret_word)

    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
