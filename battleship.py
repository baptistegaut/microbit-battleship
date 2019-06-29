# Add your Python code here. E.g.
from microbit import *
import random
import radio


maze = "00000:00000:00000:00000:00000"
win = False
boatsPart = 5
listMaze = list(maze) 
droite = 1
gauche = -1
haut = -6
bas = 6
limits = [-5, -4, -3, -2, -1, 5, 11, 17, 23, 29, 30, 31, 32, 33, 34]
#on place le premier bateau de longueur 1
boat1 = random.choice([idx for idx,e in enumerate(listMaze) if e == "0"])
listMaze[boat1] = "9"
#On place le deuxième bateau de longueur 2
boat21 = random.choice([idx for idx,e in enumerate(listMaze) if e == "0"])
listMaze[boat21] = "9"
if boat21 + gauche not in limits and listMaze[boat21 + gauche] == "0":
    boat22 = boat21 + gauche
else:
    boat22 = boat21 + droite
listMaze[boat22] = "9"
#On place le troisième bateau de longueur 2
boat31 = random.choice([idx for idx,e in enumerate(listMaze) if e == "0"])
listMaze[boat31] = "9"
if boat31 + haut  not in limits and listMaze[boat31 + haut] == "0":
    boat32 = boat31 + haut
else:
    boat32 = boat31 + bas
listMaze[boat32] = "9"

#on affiche la position des bateaux du joueurs
maze = "".join(listMaze)
display.show(Image(maze))
#on prend un nombre au hasard entre 1 et 100 qu'on va échanger avec l'adversaire pour définir qui va commencer
playerTurnNumber = random.randint(100, 200)
radio.on()
radio.send(str(playerTurnNumber))


#Cette fonction permet de choisir et d'envoyer à l'adversaire la case qu'on vise
def play():
    choosingMaze = "90000:00000:00000:00000:00000"
    choosingIdx = 0
    listChoosingMaze = list(choosingMaze)
    maze = "".join(listChoosingMaze)
    display.show(Image(maze))
    while button_b.get_presses() == 0:
        a = button_a.get_presses()
        sleep(500)
        if  a < button_a.get_presses():
            if listChoosingMaze[choosingIdx+1] == "0":
                listChoosingMaze[choosingIdx] = "0"
                choosingIdx +=1
                listChoosingMaze[choosingIdx] = "9"
            else:
                listChoosingMaze[choosingIdx] = "0"
                choosingIdx +=2
                listChoosingMaze[choosingIdx] = "9"
            maze = "".join(listChoosingMaze)
            display.show(Image(maze))
    radio.send(str(choosingIdx))


# Event loop.
# La partie continue tant que tous les bateaux ne sont pas touchés
while boatsPart > 0 and win == False:
    incoming = radio.receive()
    if incoming != None:
        incoming = int(incoming)
        if incoming >= 100:
            if playerTurnNumber > incoming:
                display.scroll("your turn")
                play()
        # Si on reçoit -1 on a touché l'adversaire 
        if incoming == -1:
            display.show("HIT")
        
        #Si on reçoit -2 on a pas touché l'adversaire
        if incoming == -2:
            display.scroll("SEA")
        if incoming == -3:
            win = True
        # On reçoit une attaque, on la traite puis on joue
        if incoming >= 0 and incoming <=30:
            # Si on est touché on perd un bout de bateau et on signal l'adversaire
            if listMaze[incoming] == "9":
                radio.send("-1")
                listMaze[incoming] = "0"
                boatsPart += -1
                display.scroll("HIT")
                maze = "".join(listMaze)
                display.show(Image(maze))
                sleep(2000)
                if boatsPart == 0:
                    radio.send("-3")
                    break
            # Si on est pas touché on signal l'adversaire
            else:
                radio.send("-2")
            play()
        maze = "".join(listMaze)
        display.show(Image(maze))

if win == True:
    display.scroll("You Win!")
else:
    display.scroll("Game Over")

            
            
        




    



