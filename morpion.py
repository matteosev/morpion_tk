from tkinter import *
from tkinter.font import *
from tkinter.messagebox import *
from datetime import *
import os
import webbrowser

def creer_quadrillage():
    # crée un carré
    canva.create_line(100,100,400,100)
    canva.create_line(400,100,400,400)
    canva.create_line(400,400,100,400)
    canva.create_line(100,100,100,400)
    # crée un quadrillage dans ce carré
    canva.create_line(100,200,400,200)
    canva.create_line(100,300,400,300)
    canva.create_line(200,100,200,400)
    canva.create_line(300,100,300,400)

def verif():
    for ligne in range(0,9,3):
        if liste_cases[ligne][2] == liste_cases[ligne + 1][2] == liste_cases[ligne + 2][2] == "o":
            return "o"
        elif liste_cases[ligne][2] == liste_cases[ligne + 1][2] == liste_cases[ligne + 2][2] == "x":
            return "x"
    for colonne in range(3):
        if liste_cases[colonne][2] == liste_cases[colonne + 3][2] == liste_cases[colonne + 6][2] == "o":
            return "o"
        elif liste_cases[colonne][2] == liste_cases[colonne + 3][2] == liste_cases[colonne + 6][2] == "x":
            return "x"
    if liste_cases[0][2] == liste_cases[4][2] == liste_cases[8][2] == "o":
        return "o"
    elif liste_cases[0][2] == liste_cases[4][2] == liste_cases[8][2] == "x":
        return "x"
    elif liste_cases[2][2] == liste_cases[4][2] == liste_cases[6][2] == "o":
        return "o"
    elif liste_cases[2][2] == liste_cases[4][2] == liste_cases[6][2] == "x":
        return "x"
    return ""

def clic(event):
    global tour
    #print(tour)
    global winner
    global score_player1
    global score_player2
    global root
    x = event.x
    y = event.y
    if x > 100 and x < 400 and y > 100 and y < 400:
        if tour % 2 == 0:
            signe = "o"
        else:
            signe = "x"
        for case in range(9):
            if liste_cases[case][0] == round(x // 100) and liste_cases[case][1] == round(y // 100):
                if liste_cases[case][2] == "":
                    liste_cases[case][2] = signe
                    if signe == "o":
                        x = round(x//100) * 100
                        y = round(y//100) * 100
                        canva.create_oval(x + 20, y + 20, x + 80 , y + 80,outline ="red", width = 5)
                    else:
                        x = round(x//100) * 100
                        y = round(y//100) * 100
                        canva.create_line(x + 20 ,y + 20,x + 80, y + 80, fill = "blue", width = 5)
                        canva.create_line(x + 80 ,y + 20,x + 20, y + 80, fill = "blue", width = 5)
                else:
                    return 
        tour += 1
        #print(liste_cases)
        rempli = True
        winner = verif()
        for case in range(9):
            if liste_cases[case][2] == "" and winner == "":
                rempli = False
        if rempli == True:
            showinfo("Grille remplie !", "Fermez cette fenêtre et cliquez sur \"nouvelle manche\".")
        if winner == "o":
            score_p1.set(score_p1.get() + 1)
            canva.bind('<Button-1>',func=NONE)
        elif winner == "x":
            score_p2.set(score_p2.get() + 1)
            canva.bind('<Button-1>',func=NONE)
			

def creer_cases():
    global liste_cases
    liste_cases = []
    for y in range(1,4):
        for x in range(1,4):
            liste_cases.append([x,y,""])

def new_game():
    global tour
    canva.delete(ALL)
    creer_quadrillage()
    creer_cases()
    canva.bind("<Button-1>",clic)
    tour = 0

def recup_noms():
    global p1
    lbl_p1.config(text = p1.get())
    lbl_p2.config(text = p2.get())

def score_0():
    global score_p1
    global score_p2
    score_p1.set(0)
    score_p2.set(0)

if ".cache" in os.listdir():
    pass
else :
    os.mkdir(".cache")

if sys.platform == "linux" :
	donnees = open(".cache/donnee.txt","a")
elif sys.platform == "win32" or "win64":
	donnees = open(".cache\donnee.txt","a")

def open_source():
    webbrowser.open("https://github.com/matteosev/morpion_tk")
    
donnees.write("\nPartie commencée le " + str(datetime.now().day) + "/" + str(datetime.now().month) + "/" + str(datetime.now().year) + " à " + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) + " par " + os.getenv("USERNAME"))
donnees.close()

root = Tk()
root.resizable(width = FALSE, height = FALSE)
root.title("Morpion")

menu = Menu()
menu.add_command(label = "code source", command = open_source)
root.config(menu = menu)

top_frame = Frame(root)
top_frame.pack(side = TOP)

left_frame = Frame(top_frame)
left_frame.pack(side = LEFT, padx = 10)

bigbottom_frame = Frame(root, bg = "ghost white")
bottom_frame = Frame(bigbottom_frame, bg = "ghost white")

p1 = StringVar()
p2 = StringVar()
p1.set("joueur 1")
p2.set("joueur 2")
score_p1 = IntVar()
score_p2 = IntVar()

Label(left_frame, text = "Joueur 1 :").grid(row = 0,pady = 5)
entry_p1 = Entry(left_frame, textvariable = p1)
Label(left_frame, text = "Joueur 2 :").grid(row = 2,pady = 5)
entry_p2 = Entry(left_frame, textvariable = p2)

lbl_p1 = Label(bottom_frame,text = "joueur 1", bg = "ghost white")
lbl_p2 = Label(bottom_frame, text = "joueur 2", bg = "ghost white")

Button(left_frame,text = "Valider", command = recup_noms).grid(row = 5, pady = 10)
Button(left_frame,text = "nouvelle manche", command = new_game).grid(row = 6,pady = 10)
Button(left_frame, text = "remise des scores à zéro", command = score_0).grid(row = 7)

entry_p1.grid(row = 1,pady = 5)
entry_p2.grid(row = 4, pady = 5)

tour = 0
canva = Canvas(top_frame, width=500, height = 500, bg = "white")

new_game()

canva.bind("<Button-1>",clic)

canva.pack(side = RIGHT)

big = Font(root,name = "bold",size = 12)
resultat = Frame(bigbottom_frame, bg = "ghost white")
Label(resultat, text = "Résultats", bg ="ghost white", font = big, anchor = "center").pack(expand = 1, fill = BOTH)
resultat.pack(pady = 10,fill = X)


lbl_p1.grid()
Label(bottom_frame, text = "a gagné", bg = "ghost white").grid(row = 0,column = 1)
Label(bottom_frame, textvariable = score_p1, bg = "ghost white").grid(row = 0,column = 2)
Label(bottom_frame, text = "manches", bg = "ghost white").grid(row = 0,column = 3)

lbl_p2.grid()
Label(bottom_frame, text = "a gagné", bg = "ghost white").grid(row = 1,column = 1)
Label(bottom_frame, textvariable = score_p2, bg = "ghost white").grid(row = 1,column = 2)
Label(bottom_frame, text = "manches", bg = "ghost white").grid(row = 1,column = 3)

bottom_frame.pack(pady = 10)

bigbottom_frame.pack(fill = X)

root.mainloop()
