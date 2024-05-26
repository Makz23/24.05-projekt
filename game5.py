import random

def display_hangman(tries):
    stages = [
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / 
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |    
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |    
           -
        """,
        """
           ------
           |    |
           |    O
           |    |
           |    
           -
        """,
        """
           ------
           |    |
           |    O
           |    
           |    
           -
        """,
        """
           ------
           |    |
           |    
           |    
           |    
           -
        """
    ]
    return stages[tries]

def main():
    word_list = ["python", "java", "swift", "javascript"]
    word = random.choice(word_list)
    word_letters = set(word)
    guessed_letters = set()
    tries = 6

    while tries > 0 and word_letters:
        print(display_hangman(tries))
        print("Word: ", " ".join([letter if letter in guessed_letters else "_" for letter in word]))
        print("Guessed letters: ", " ".join(guessed_letters))
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter.")
        elif guess in word_letters:
            word_letters.remove(guess)
            guessed_letters.add(guess)
        else:
            tries -= 1
            guessed_letters.add(guess)
            print(f"Incorrect! You have {tries} tries left.")

    if word_letters:
        print(display_hangman(0))
        print(f"Sorry, you lost! The word was '{word}'.")
    else:
        print(f"Congratulations! You guessed the word '{word}'!")

if __name__ == "__main__":
    main()
