from enum import Enum

class Order(Enum):
    PLAYER = 0
    COMPUTER = 1

class Node:
    def __init__(self, p_stones, p_points, stones, c_stones, c_points):
        self.p_stones = p_stones # spēlētāja akmentiņu skaits
        self.p_points = p_points # spēlētāja punktu skaits
        self.stones = stones # akmentiņu skaits uz galda
        self.c_stones = c_stones # datora akmentiņu skaits
        self.c_points = c_points # datora punktu skaits
        self.left = None
        self.right = None

    def add_children(self, order, n):

        # n šajā gadījumā ir, lai koks tiktu ģenerēts tikai līdz noteiktam dziļumam, tas tiek panākts ar rekursijas palīdzību
        if n == 0:
            return

        # take 2 stones
        if self.stones - 2 >= 0:
            left = Node(self.p_stones, self.p_points, self.stones - 2, self.c_stones, self.c_points)

            if order == Order.PLAYER:
                left.p_stones += 2
                if left.stones % 2 == 0:
                    left.p_points += 2
                else:
                    left.p_points -= 2
            else:
                left.c_stones += 2
                if left.stones % 2 == 0:
                    left.c_points += 2
                else:
                    left.c_points -= 2

            self.left = left

        # take 3 stones
        if self.stones - 3 >= 0:
            right = Node(self.p_stones, self.p_points, self.stones - 3, self.c_stones, self.c_points)

            if order == Order.PLAYER:
                right.p_stones += 3
                if right.stones % 2 == 0:
                    right.p_points += 2
                else:
                    right.p_points -= 2
            else:
                right.c_stones += 3
                if right.stones % 2 == 0:
                    right.c_points += 2
                else:
                    right.c_points -= 2

            self.right = right

        if self.left:
            self.left.add_children(Order((order.value + 1) % 2), n - 1) #šeit tiek izmantota rekursija
        if self.right:
            self.right.add_children(Order((order.value + 1) % 2), n - 1)

    def game_end(self):
        return self.stones <= 1

    def computerWin(self):
        return (self.c_points + self.c_stones) > (self.p_points + self.p_stones)

    def heuristicFunction(self):
        # Šeit varat pamainīt heiristiskā novērtējuma funkciju un paspēlēties, kura ir labāka
        # Šobrīd heiristiskā funkcija f(n) = punktu starpība + 5(ja akmentiņu skaits ir pāra, citādi 0)
        return (self.c_points + self.c_stones) - (self.p_points + self.p_stones) + 5 * ((self.stones + 1) % 2)



    def minimax(node, isMaximizingPlayer):
        # if node.game_end():
        #     return 1 if node.computerWin() else -1

        # ja nav pēcteču tad aprēķinam heiristiskā novērtējuma funkciju
        if (node.left == None and node.right == None):
            return node.heuristicFunction()


        if isMaximizingPlayer:
            best_score = float("-inf")

            if node.left:
                best_score = max(best_score, Node.minimax(node.left, False))
            if node.right:
                best_score = max(best_score, Node.minimax(node.right, False))

            return best_score

        else:
            best_score = float("inf")

            if node.left:
                best_score = min(best_score, Node.minimax(node.left, True))
            if node.right:
                best_score = min(best_score, Node.minimax(node.right, True))

            return best_score
    


    def getBestMove(node, algorithm):
        tree = Tree(node, Order.COMPUTER)
        tree.generate_tree_to_n(2)

        if (algorithm == "minimax"):
            left_score = Node.minimax(node.left, False) if node.left else float("-inf")
            right_score = Node.minimax(node.right, False) if node.right else float("-inf")

            if left_score > right_score:
                return node.left
            else:
                return node.right
        elif (algorithm == "alphabeta"):
            # alpha-beta algoritms nav implementēts
            return 0


class Tree:
    def __init__(self, node, order):
        self.root = node
        self.order = order

    def generate_tree_to_n(self, n):
        self.root.add_children(self.order, n)

    def print_tree(self, node=None, prefix="", is_left=True):
        if node is None:
            node = self.root

        print(prefix + ("├─ " if is_left else "└─ ") +
              f"Node(stones={node.stones}, p_stones={node.p_stones}, p_points={node.p_points}, "
              f"c_stones={node.c_stones}, c_points={node.c_points})")

        if node.left:
            self.print_tree(node.left, prefix + ("│  " if is_left else "   "), True)
        if node.right:
            self.print_tree(node.right, prefix + ("│  " if is_left else "   "), False)


class Game:
    def __init__(self, node):
        self.current_position = node

    def make_move(self, node):
        self.current_position = node


def main():
    total_stones = 50

    node = Node(0, 0, total_stones, 0, 0)
    # tree = Tree(node, 1)  # computer starts
    # tree.generate_tree_to_n(20)

    game = Game(node)

    print(f"Welcome to the Stone Game! There are {total_stones} stones on the table.")
    print("Computer will start now")

    while not game.current_position.game_end():

        print(f"\nStones left: {game.current_position.stones}")
        print(f"Your stones: {game.current_position.p_stones}, Your points: {game.current_position.p_points}")
        print(f"Computer stones: {game.current_position.c_stones}, Computer points: {game.current_position.c_points}")

        # --- Computer move ---
        best_move = Node.getBestMove(game.current_position)

        if best_move is None:
            print("Computer cannot move.")
            break

        taken = game.current_position.stones - best_move.stones
        game.make_move(best_move)

        print(f"Computer takes {taken} stones.")
        
        print(f"\nStones left: {game.current_position.stones}")
        print(f"Your stones: {game.current_position.p_stones}, Your points: {game.current_position.p_points}")
        print(f"Computer stones: {game.current_position.c_stones}, Computer points: {game.current_position.c_points}")

        if game.current_position.game_end():
            break

        # --- Player move ---
        while True:
            try:
                player_take = int(input("Pick 2 or 3 stones: "))
                if player_take in [2, 3] and player_take <= game.current_position.stones:
                    break
                else:
                    print("Invalid move.")
            except ValueError:
                print("Enter a number.")

        if player_take == 2 and game.current_position.left:
            game.make_move(game.current_position.left)
        elif player_take == 3 and game.current_position.right:
            game.make_move(game.current_position.right)
        else:
            print("Move not possible.")
            break

    print("\nGame Over!")

    print(f"Your stones: {game.current_position.p_stones}, Your points: {game.current_position.p_points}")
    print(f"Computer stones: {game.current_position.c_stones}, Computer points: {game.current_position.c_points}")

    if game.current_position.computerWin():
        print("Computer wins!")
    else:
        print("You win!")

if (__name__ == "__main__"):
    main()