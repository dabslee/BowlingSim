from engine import Game

# Create the game and run the simulation
game = Game()
game.runGame()

# Print out the frames of the game
print(game.display)

# Print the formatted scorecard
printcard = "Scorecard:\nFrame:\t"
for i in range(10):
    printcard += "%d\t" % (i + 1)
printcard += "\nScore:\t"
for i in range(9):
    printcard += game.scorecard[i] + "\t"
printcard += game.scorecard[9] + " "
if len(game.scorecard) == 11:
    printcard += game.scorecard[10]
printcard += "\n"
printcard = printcard.replace("   ", " ")
printcard = printcard.replace("  ", " ")
print(printcard)

# Print the final score of the game
print("Final score:", game.totalscore)