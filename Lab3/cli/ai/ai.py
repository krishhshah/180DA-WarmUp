import random as r

p_win = 0
c_win = 0
tie = 0
choices = ['rock', 'paper', 'scissors']
while True:
    computer = r.randrange(3)
    inp = input('Rock(r) Paper(p) or Scissors(s)? Type q to quit.')
    if inp == 'q':
        break
    elif inp != 'r' and inp != 'p' and inp != 's':
        print("Please enter 'r', 'p','s', or 'q'.")
        continue

    print("Computer played ", choices[computer])

    if inp == 'r':
        player = 0
    elif inp == 'p':
        player = 1
    elif inp == 's':
        player = 2
    
    if computer == player:
        print("Tie: ")
        tie+=1
    elif (computer - player) == 2:
        print("Player wins: ")
        p_win += 1
    elif (computer - player) == -2:
        print("Computer wins: ")
        c_win += 1
    elif computer > player:
        print("Computer wins: ")
        c_win += 1
    elif player > computer:
        print("Player wins: ")
        p_win += 1

    print("Player ", p_win, "  Computer ", c_win, "  Tie ", tie)
