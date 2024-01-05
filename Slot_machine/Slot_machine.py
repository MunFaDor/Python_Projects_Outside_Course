import random

MAX_LINES = 7 #~ 5 lines + 2 diagonals
MAX_BET = 1000
MIN_BET = 5

ROWS = 5
COLS = 5

symbol_count = {
    "A": 10,    # ~ Include the symbol 'A' 10 times in each reel (column)
    "B": 12,    # ~ Include the symbol 'B' 12 times in each reel (column)
    "C": 16,    # ~ Include the symbol 'C' 16 times in each reel (column)
    "D": 20,    # ~ Include the symbol 'D' 20 times in each reel (column)
    "E": 24,    # ~ Include the symbol 'E' 24 times in each reel (column)
    "*": 5,     # ~ Include the symbol '*' 5 times in each reel (column)
    "@": 5      # ~ Include the symbol '@' 5 times in each reel (column)
}

symbol_value = {
    "A": 5,     # ~ Symbol "A" has a value of 5
    "B": 4.5,   # ~ Symbol "B" has a value of 4.5
    "C": 4,     # ~ Symbol "C" has a value of 4
    "D": 3.5,   # ~ Symbol "D" has a value of 3.5
    "E": 3,     # ~ Symbol "E" has a value of 3
    "*": 2,     # ~ Scater '*' = winnings x2
    "@": 2      # ~ Scater '@' = winnings x2
}

def deposit():  #~ we define the DEPOSIT here.
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():     #~ A check if the input is a digit.
            amount = int(amount) #~ converting the input to an INT as it is inputed as a STRING.
            if amount > 0:
                break            #~ If input is digit and is a correct amount break out of the cycle.
            else:
                print("The deposit must be greater than 0$")
        else:
            print("Please enter a number.")

    return amount                #~ returning the deposit amount for future use in the program.

def get_number_of_lines():
    while True:
        Lines = input("Enter the number of lines to bet on: (1-"+str(MAX_LINES) + ")? ")
        if Lines.isdigit(): 
            Lines = int(Lines) #~ converting the input to an INT as it is inputed as a STRING.
            if 1 <= Lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines")
        else:
            print("Please enter a number.")

    return Lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
                                #~ converting the input to an INT as it is inputed as a STRING.
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between {MIN_BET}$ and {MAX_BET}$")
        else:
            print("Please enter a number.")

    return amount

def spin(balance):
    lines = get_number_of_lines()
    bet = get_bet()

    total_bet = bet * lines

    if total_bet > balance:
        print(
            f"You do not have enough to bet that amount. Your current balance is {balance}$")
        return 0

    print(
        f"You are currently betting {bet}$ on {lines} lines. Your total bet is {total_bet}$")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won {winnings}$.")
    print(f"You won on line:", *winning_lines)

    return winnings - total_bet

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns):
    print('\n')
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns)-1:
                print(column[row], end="|")
            else:
                print(column[row], end="")
        print()
    print('\n')

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        if len(columns) > 0 and len(columns[0]) > line:
            symbol = columns[0][line]
        else:
            break

        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            if symbol in ["*", "@"]:                  #~ Check for '*' и '@'
                winnings += values[symbol] * bet * 2  #~ x2 the win on the line if "*/@" is there.
            else:
                winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    diagonal1 = [columns[i][i] for i in range(len(columns))]
    diagonal2 = [columns[i][len(columns)-1-i] for i in range(len(columns))]
    diagonals = [diagonal1, diagonal2]
    for diagonal in diagonals:
        symbol = diagonal[0]
        if all(symbol == d for d in diagonal):
            if symbol in ["*", "@"]:
                winnings += values[symbol] * bet * 2
            else:
                winnings += values[symbol] * bet
            winning_lines.append("Diagonal")
    return winnings, winning_lines #~ Return the winnings and on which line they are for future use.

def main():
    balance = deposit()
    while True:
        print(f"Current balance is {balance}$")
        answer = input(
            "Press enter to play (K to quit or D to deposit additional funds)")

        if answer.lower() == "k":
            break
        elif answer.lower() == "d":
            additional_deposit = deposit()
            balance += additional_deposit
        else:
            balance += spin(balance)

    print(f"You left with {balance}")

main()