import random

CHOICES = {1: "rock", 2: "paper", 3: "scissors"}

def get_user_choice():
    """Loops until the user enters a valid number (1, 2, or 3)."""
    while True:
        try:
            index = int(input("\nEnter your choice (1-3): "))
            if index in CHOICES:
                return CHOICES[index]
            print("Invalid number. Please choose 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("=" * 60)
    print("Welcome to Rock, Paper, Scissors Game")
    print("=" * 60)
    print("1) Rock\n2) Paper\n3) Scissors")
    
    cpu_score = 0
    user_score = 0
    rounds = 3
    
    for current_round in range(rounds):
        user_choice = get_user_choice()
        cpu_choice = random.choice(list(CHOICES.values()))
        
        print(f"Your Choice: {user_choice} vs CPU Choice: {cpu_choice}")
        

        if user_choice == cpu_choice:
            print("This round is a tie!")

        elif (user_choice == "rock" and cpu_choice == "scissors") or \
             (user_choice == "paper" and cpu_choice == "rock") or \
             (user_choice == "scissors" and cpu_choice == "paper"):
            print("You win this round!")
            user_score += 1
            
        else:
            print("CPU wins this round!")
            cpu_score += 1
            
        print(f"Score -> You: {user_score} | CPU: {cpu_score}")

    print("=" * 60)
    if user_score > cpu_score:
        print(f"You Won the Game!!! ({user_score} vs {cpu_score})")
    elif user_score < cpu_score:
        print(f"You Lose the Game! ({user_score} vs {cpu_score})")
    else:
        print(f"The Game is a Draw! ({user_score} vs {cpu_score})")
    print("=" * 60)

if __name__ == "__main__":
    main()
