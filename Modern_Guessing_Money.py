import csv
import os
import random

# File to store user credentials and scores
database_file = "users_db.csv"
# File to log game results and bets
game_log_file = "game_log.csv"

# Function to initialize the CSV files if they don't exist
def initialize_db():
    if not os.path.exists(database_file):
        with open(database_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "score"])  # Header for user database

    if not os.path.exists(game_log_file):
        with open(game_log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["player", "attempts", "number_guessed", "bet_amount", "payout"])  # Header for game logs

# Function to register a new user
def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    if username_exists(username):
        print("Username already exists!")
    else:
        with open(database_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, 0])  # Initialize score as 0
        print("User registered successfully!")

# Function to check if a username exists
def username_exists(username):
    with open(database_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if row[0] == username:
                return True
    return False

# Function to login a user
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    with open(database_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if row[0] == username and row[1] == password:
                print("Login successful!")
                return username  # Return the username for later use
    print("Invalid username or password!")
    return None

# Function to play the guessing game for one player
def play_game_for_one_player(username, number_to_guess):
    print(f"\n{username}, it's your turn.")
    attempts = 0
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            if guess < number_to_guess:
                print("Higher...")
            elif guess > number_to_guess:
                print("Lower...")
            else:
                print(f"Congratulations, {username}! You guessed the number in {attempts} attempts.")
                return attempts, number_to_guess
        except ValueError:
            print("Please enter a valid integer.")

# Function to confront two players
def confront_players(player1, player2):
    print("Welcome both players to the guessing game!")
    number_to_guess = random.randint(1, 100)
    bets = take_bets([player1, player2])  # Handle bets before starting the game

    attempts_player1, guessed_number1 = play_game_for_one_player(player1, number_to_guess)
    log_game(player1, attempts_player1, guessed_number1, bets.get(player1, 0))

    number_to_guess = random.randint(1, 100)  # Change number for player 2
    attempts_player2, guessed_number2 = play_game_for_one_player(player2, number_to_guess)
    log_game(player2, attempts_player2, guessed_number2, bets.get(player2, 0))

    determine_winner(player1, player2, attempts_player1, attempts_player2, bets)

# Function to log game results and bets to the CSV
def log_game(player, attempts, number_guessed, bet_amount):
    with open(game_log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player, attempts, number_guessed, bet_amount, 0])  # Payouts updated later

# Function to take bets
def take_bets(players):
    print("\nBetting Section: ")
    num_bettors = int(input("How many people are betting? "))
    bets = {}
    for _ in range(num_bettors):
        bettor = input("Enter bettor's name: ")
        chosen_player = input(f"Who is {bettor} betting on? ({players[0]} or {players[1]}): ")
        amount = float(input(f"How much is {bettor} betting on {chosen_player}? $"))
        if chosen_player in bets:
            bets[chosen_player] += amount
        else:
            bets[chosen_player] = amount
    return bets

# Function to determine and announce the winner
def determine_winner(player1, player2, attempts_player1, attempts_player2, bets):
    total_pool = sum(bets.values())
    if attempts_player1 < attempts_player2:
        print(f"{player1} wins the game with fewer attempts!")
        handle_payouts(player1, bets, total_pool)
    elif attempts_player2 < attempts_player1:
        print(f"{player2} wins the game with fewer attempts!")
        handle_payouts(player2, bets, total_pool)
    else:
        print("It's a tie!")
        handle_payouts(None, bets, total_pool)  # No winner in the case of a tie

# Function to handle payouts
def handle_payouts(winner, bets, total_pool):
    if winner and winner in bets:
        winner_bet = bets[winner]
        payout = total_pool  # Assuming winner takes all for simplicity
        print(f"\n{winner} wins the betting pool of ${total_pool}!")
        for bettor in bets:
            if bettor == winner:
                print(f"Bet on {winner} wins ${payout}!")
                update_payouts(winner, payout)
            else:
                print(f"Bet on {bettor} loses ${bets[bettor]}.")
    else:
        print("No bets were placed on the winner or it was a tie. No payouts.")

# Function to update payouts in the game log
def update_payouts(winner, payout):
    rows = []
    with open(game_log_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == winner:
                row[4] = str(payout)  # Update payout for the winner
            rows.append(row)
    with open(game_log_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Main function
def main():
    initialize_db()  # Ensure the CSV files exist

    while True:
        choice = input("\n1. Register\n2. Confront Players\n3. Exit\nChoose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            player1 = login()
            player2 = login()
            if player1 and player2:
                confront_players(player1, player2)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
