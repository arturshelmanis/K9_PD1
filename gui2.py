import tkinter as tk
import time

from game import Node

root = tk.Tk()
root.geometry("900x700")
root.title("Stone game")
root.resizable(width=False, height=False)

menu_frame = tk.Frame(root, bg="grey")
rules_frame = tk.Frame(root, bg="grey")
game_frame = tk.Frame(root, bg="grey")
approve_frame = tk.Frame(root, bg="grey")

stats_frame = tk.Frame(game_frame, bg="grey")
stats_frame.pack(pady=40)

menu_frame.pack(fill="both", expand=True)

def start_game():
    reset_game()  # pārliecinamies, ka sāksies pilnīgi jauna spēle - restartējam spēli to sākot.
    menu_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    start_node = Node(0, 0, int(stones_entry.get()), 0, 0)

    if (first_player.get() == "computer"): # ja dators iet pirmais, tad viņš šeit izdara gājienu
        computer_turn()

def game_rules():
    menu_frame.pack_forget()
    rules_frame.pack(fill="both", expand=True)

def back_from_rules():
    rules_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)

def back_from_game():
    game_frame.pack_forget()
    approve_frame.pack(fill="both", expand=True)

def approve_exit():
    reset_game() # izejot no spēles atgriežam spēli sākuma stāvoklī
    approve_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)

def decline_exit():
    approve_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

def reset_game():
    # atgriežam spēles vērtības uz sākuma stāvokli
    table_stones.set(int(stones_entry.get()))
    pl_stones.set(0)
    pl_points.set(0)

    comp_stones.set(0)
    comp_points.set(0)

    comp_taken_stones.set(0)

    winner_label.config(text="") # noņemam uzvarētāja izvadi
    computer_time.set("") # noņemam laika izvadi
    play_again_btn.place_forget() # noņemam play again poga izvadi


def take_stones(n):
    if table_stones.get() >= n:
        table_stones.set(table_stones.get() - n)
        pl_stones.set(pl_stones.get() + n)

        if table_stones.get() % 2 == 0:
            pl_points.set(pl_points.get() + 2)
        else:
            pl_points.set(pl_points.get() - 2)

        # check game end
        if table_stones.get() == 0 or table_stones.get() == 1:
            get_winner()
            return

        root.after(100, lambda:computer_turn()) # pirms datora gājiena pagaidam 100 ms, lai var saprast, kas notiek

        if table_stones.get() == 0 or table_stones.get() == 1:
            get_winner()
            return



def computer_turn():
    # sākam laika atskaiti
    start = time.perf_counter()

    current_node = Node(pl_stones.get(), pl_points.get(), table_stones.get(), comp_stones.get(), comp_points.get())
    best_move = Node.getBestMove(current_node, algorithm.get())

    if best_move is None:
        print("Computer cannot move.")
        return

    update_stats(best_move)
    # beidzam laika atskaiti
    end = time.perf_counter()

    computer_think_time = end - start

    computer_time.set(f"Computer thinks time: {computer_think_time:.6f} s")

    # parbauda vai spēle beigusies, ja dators uzsāk spēli
    if table_stones.get() == 0 or table_stones.get() == 1:
        get_winner()
        return
    comp_taken_stones.set(current_node.stones - best_move.stones)

    computer_taken_stones.grid()
    computer_taken_stones_value.grid()

    #Varbut nevajag dzest viņus, lai vienmēr būtu info
    #root.after(1000, lambda:computer_taken_stones.grid_remove())
    #root.after(1000, lambda:computer_taken_stones_value.grid_remove())


def get_winner():
    player_score = pl_points.get() + pl_stones.get()
    computer_score = comp_points.get() + comp_stones.get()

    if player_score > computer_score:
        text = "Spēlētājs uzvar!"
    elif computer_score > player_score:
        text = "Dators uzvar!"
    else:
        text = "Neizšķirts!"

    winner_label.config(text=text)
    play_again_btn.place(relx=0.0, rely=1.0, anchor="s", x=450, y=-10)

def update_stats(node):
    table_stones.set(node.stones)
    pl_stones.set(node.p_stones)
    pl_points.set(node.p_points)
    comp_stones.set(node.c_stones)
    comp_points.set(node.c_points)

rules_text = """
Uz galda atrodas tik daudz akmentiņu, cik spēlētajs izvēlējās  diapazonā no 50 līdz 70. 
Katram spēlētājam spēles sākumā ir 0 akmentiņu un 0 punktu. 

Spēlētāji izpilda gājienus pēc kārtas. Spēlētājs savā gājienā drīkst 
paņemt sev 2 vai 3 akmentiņus.

Ja pēc akmentiņu paņemšanas uz galda ir palicis pāra akmentiņu skaits,
tad spēlētāja punktiem tiek pieskaitīti 2 punkti, bet ja nepāra skaits,
tad tiek atņemti 2 punkti.

Spēle beidzas, kad uz galda nepaliek neviens akmentiņš.

Spēlētāju punktu skaitam tiek pieskaitīts spēlētājam esošo akmentiņu
skaits.

Ja spēlētāju punktu skaits ir vienāds, tad rezultāts ir neizšķirts.
Pretējā gadījumā uzvar spēlētājs, kam ir vairāk punktu.
"""

tk.Label(menu_frame, text="Main menu", font=("Arial", 18), bg="grey").pack(pady=5)

tk.Label(menu_frame, text="Sākuma akmentiņu skaits (50–70)", font=("Arial", 16), bg="grey").pack(pady=10)
stones_entry = tk.Spinbox(menu_frame, from_=50, to=70, font=("Arial", 14), width=8)
stones_entry.pack(pady=5)

table_stones = tk.IntVar(value=int(stones_entry.get()))

pl_stones = tk.IntVar(value=0)
pl_points = tk.IntVar(value=0)

comp_stones = tk.IntVar(value=0)
comp_points = tk.IntVar(value=0)

comp_taken_stones = tk.IntVar(value=0)

computer_time = tk.StringVar(value="Computer thinking time: 0.000000 s")

title = tk.Label(stats_frame, text="Atlikušie akmentiņi:", font=("Arial", 16), bg="grey")
title.grid(row=0, column=0, pady=10)

table_stones_label = tk.Label(stats_frame, textvariable=table_stones, font=("Arial", 16), bg="grey")
table_stones_label.grid(row=0, column=1, pady=10)

player_stats = tk.Label(stats_frame, text="Cilvēks", font=("Arial", 14), bg="grey")
player_stats.grid(row=1, column=0, padx=50)

computer_stats = tk.Label(stats_frame, text="Dators", font=("Arial", 14), bg="grey")
computer_stats.grid(row=1, column=1, padx=50)

player_stones = tk.Label(stats_frame, text="Akmentiņu skaits:", font=("Arial", 14), bg="grey")
player_stones.grid(row=2, column=0, pady=5)

computer_stones = tk.Label(stats_frame, text="Akmentiņu skaits:", font=("Arial", 14), bg="grey")
computer_stones.grid(row=2, column=1, pady=5)

player_stones_value = tk.Label(stats_frame, textvariable=pl_stones, font=("Arial", 14), bg="grey")
player_stones_value.grid(row=3, column=0)

computer_stones_value = tk.Label(stats_frame, textvariable=comp_stones, font=("Arial", 14), bg="grey")
computer_stones_value.grid(row=3, column=1)

player_points = tk.Label(stats_frame, text="Punktu skaits:", font=("Arial", 14), bg="grey")
player_points.grid(row=4, column=0, pady=5)

computer_points = tk.Label(stats_frame, text="Punktu skaits:", font=("Arial", 14), bg="grey")
computer_points.grid(row=4, column=1, pady=5)

player_points_value = tk.Label(stats_frame, textvariable=pl_points, font=("Arial", 14), bg="grey")
player_points_value.grid(row=5, column=0)

computer_points_value = tk.Label(stats_frame, textvariable=comp_points, font=("Arial", 14), bg="grey")
computer_points_value.grid(row=5, column=1)

computer_taken_stones = tk.Label(stats_frame, text="Dators paņēma: ", font=("Arial", 14), bg="grey")
computer_taken_stones.grid(row=6, column=0, pady=10)
#computer_taken_stones.grid_remove()

computer_taken_stones_value = tk.Label(stats_frame, textvariable=comp_taken_stones, font=("Arial", 14), bg="grey")
computer_taken_stones_value.grid(row=6, column=1)
#computer_taken_stones_value.grid_remove()

computer_taken_stones = tk.Label(stats_frame, textvariable=computer_time, font=("Arial", 14), bg="grey")
computer_taken_stones.grid(row=7, column=0, columnspan=2, pady=10)

tk.Label(menu_frame, text="Izvēlieties kurš sāks spēli:", font=("Arial", 16), bg="grey").pack(pady=10)
first_player = tk.StringVar(value="human")
tk.Radiobutton(menu_frame, text="Cilvēks", bg="grey", font=("Arial", 14), variable=first_player, value="human").pack()
tk.Radiobutton(menu_frame, text="Dators", bg="grey", font=("Arial", 14), variable=first_player, value="computer").pack()

tk.Label(menu_frame, text="Izvēlieties spēles algoritmu:", font=("Arial", 16), bg="grey").pack(pady=10)
algorithm = tk.StringVar(value="minimax")
tk.Radiobutton(menu_frame, text="Minimax", bg="grey", font=("Arial", 14), variable=algorithm, value="minimax").pack()
tk.Radiobutton(menu_frame, text="Alpha-Beta", bg="grey", font=("Arial", 14), variable=algorithm,
               value="alphabeta").pack()

tk.Label(rules_frame, text=rules_text, font=("Arial", 16), wraplength=500, justify="center", bg="grey").pack(pady=20)
tk.Label(approve_frame, text="You really want to exit", font=("Arial", 16), wraplength=500, justify="center", bg="grey").pack(pady=20)

# izvades vieta uzvarētāja tekstam - formatējusm ārpus klases get_winnner, lai tekstu var noņemt, kad sākas jauna spēle
winner_label = tk.Label(game_frame, text="", font=("Arial", 16), bg="grey")
winner_label.place(relx=0.5, rely=1.0, anchor="s", y=-100)


exit_btn = tk.Button(menu_frame, text="Exit",bg="white",
                     activebackground="black",activeforeground="black", width=15, height=4, command=root.destroy)
game_btn = tk.Button(menu_frame, text="Start game",bg="white",
                     activebackground="black",activeforeground="black", width=15, height=4, command=start_game)
rules_btn = tk.Button(menu_frame, text="Game rules",bg="white",
                      activebackground="black",activeforeground="black", width=15, height=4, command=game_rules)
back_from_rules_btn = tk.Button(rules_frame, text="Back",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command=back_from_rules)
exit_from_game_btn = tk.Button(game_frame, text="Exit",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command=back_from_game)
take_two_game_btn = tk.Button(game_frame, text="Take 2 stones",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command= lambda:take_stones(2))
take_three_game_btn = tk.Button(game_frame, text="Take 3 stones",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command= lambda:take_stones(3))
approve_exit_btn = tk.Button(approve_frame, text="Yes",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command=approve_exit)
decline_exit_btn = tk.Button(approve_frame, text="No",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command=decline_exit)
play_again_btn = tk.Button(game_frame, text="Play again",bg="white",
                                activebackground="black",activeforeground="black", width=15, height=4, command=start_game)

approve_exit_btn.pack(pady=10)
decline_exit_btn.pack(pady=10)
game_btn.pack(pady=10)
rules_btn.pack(pady=10)
exit_btn.pack(pady=10)
back_from_rules_btn.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
exit_from_game_btn.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)
take_two_game_btn.place(relx=0.0, rely=1.0, anchor="s", x=350, y=-250)
take_three_game_btn.place(relx=0.0, rely=1.0, anchor="s", x=550, y=-250)

root.mainloop()
