from enum import Enum

class Order(Enum):
    PLAYER = 0
    COMPUTER = 1

class Node:
    # klases mainīgie, kuriem var piekļūt šajā klasē, jebkurā instancē un visās instancēs vērtība ir vienāda
    generated_nodes_count = 0
    evaluated_nodes_count = 0

    def __init__(self, p_stones, p_points, stones, c_stones, c_points):
        self.p_stones = p_stones # spēlētāja akmentiņu skaits
        self.p_points = p_points # spēlētāja punktu skaits
        self.stones = stones # akmentiņu skaits uz galda
        self.c_stones = c_stones # datora akmentiņu skaits
        self.c_points = c_points # datora punktu skaits
        self.left = None
        self.right = None
        self.alphabeta_value = None

    def add_children(self, order, n):
        Node.generated_nodes_count += 1

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

    def computerWin(self):
        return (self.c_points + self.c_stones) > (self.p_points + self.p_stones)

    def heuristicFunction(self):
        # Šeit varat pamainīt heiristiskā novērtējuma funkciju un paspēlēties, kura ir labāka
        # Šobrīd heiristiskā funkcija f(n) = punktu starpība + 5(ja akmentiņu skaits ir pāra, citādi 0)
        return (self.c_points + self.c_stones) - (self.p_points + self.p_stones) + 5 * ((self.stones + 1) % 2)

    def minimax(node, isMaximizingPlayer):
        Node.evaluated_nodes_count += 1

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

    def alphabeta(node, parent_node = None, isMaximizingPlayer = True):
        Node.evaluated_nodes_count += 1
        # ja nav pēcteču tad aprēķinam heiristiskā novērtējuma funkciju
        if (node.left == None and node.right == None):
            return node.heuristicFunction(), node
        
        if isMaximizingPlayer:
            best_score = float("-inf")
            best_node = None

            for child in [node.left, node.right]:
                if child:
                    score, _ = Node.alphabeta(child, node, False)
                    if (score > best_score):
                        best_score = score
                        best_node = child
                    node.alphabeta_value = max(node.alphabeta_value, best_score) if node.alphabeta_value is not None else best_score
                    if parent_node is not None and parent_node.alphabeta_value is not None and parent_node.alphabeta_value <= node.alphabeta_value:
                        break
            return best_score, best_node
    
        else:
            best_score = float("inf")
            best_node = None

            for child in [node.left, node.right]:
                if child:
                    score, _ = Node.alphabeta(child, node, True)
                    if score < best_score:
                        best_score = score
                        best_node = child
                    node.alphabeta_value = min(node.alphabeta_value, best_score) if node.alphabeta_value is not None else best_score
                    if parent_node is not None and parent_node.alphabeta_value is not None and parent_node.alphabeta_value >= node.alphabeta_value and child is node.left:
                        break
            return best_score, best_node


    def getBestMove(node, algorithm):
        # šeit mums vajag rēķināt ģenērētās un novērtētās virsotnes
        node.generate_tree_to_n(5)

        if (algorithm == "minimax"):
            left_score = Node.minimax(node.left, False) if node.left else float("-inf")
            right_score = Node.minimax(node.right, False) if node.right else float("-inf")
            Node.evaluated_nodes_count += 1 

            if left_score > right_score:
                return node.left       
            else:
                return node.right
        elif (algorithm == "alphabeta"):
            best_move = Node.alphabeta(node,None, True)[1]
            return best_move

    def generate_tree_to_n(self, n):
        Node.evaluated_nodes_count = 0
        Node.generated_nodes_count = 0
        self.add_children(Order.COMPUTER, n)