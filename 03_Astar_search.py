import heapq

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state      # Current state in the search space
        self.parent = parent    # Parent node
        self.action = action    # Action that led to this node from the parent node
        self.cost = cost        # Cost to reach this node from the start node
        self.heuristic = heuristic  # Heuristic estimate of the cost to reach the goal
    
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def parse_graph_input():
    graph = {}
    num_edges = int(input("Enter the number of edges: "))
    for _ in range(num_edges):
        u, v, cost = input("Enter an edge (format: u v cost): ").split()
        cost = int(cost)
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, cost))
        graph[v].append((u, cost))
    return graph

def astar_search(start_state, goal_test, successors, heuristic):
    # Priority queue to store nodes ordered by f = g + h
    frontier = []
    heapq.heappush(frontier, Node(start_state, None, None, 0, heuristic(start_state)))
    explored = set()
    
    while frontier:
        current_node = heapq.heappop(frontier)
        current_state = current_node.state
        
        if goal_test(current_state):
            # Reconstruct the path from the goal node to the start node
            path = []
            while current_node.parent is not None:
                path.append((current_node.action, current_node.state))
                current_node = current_node.parent
            path.reverse()
            return path
        
        explored.add(current_state)
        
        # Generate successors for the current state using the `successors` function
        for action, successor_state, step_cost in successors(current_state):
            if successor_state not in explored:
                new_cost = current_node.cost + step_cost
                new_node = Node(successor_state, current_node, action, new_cost, heuristic(successor_state))
                heapq.heappush(frontier, new_node)
    
    return None  # No path found

if __name__ == "__main__":
    # Get user input to define the graph
    print("Define the graph:")
    graph = parse_graph_input()
    
    start_state = input("Enter the start state: ")
    goal_state = input("Enter the goal state: ")
    
    def goal_test(state):
        return state == goal_state
    
    def successors(state):
        # Generate successor states from the current state based on the graph
        successors_list = []
        for neighbor, cost in graph.get(state, []):
            action = f"Move to {neighbor}"  # Default action (e.g., "Move to B")
            successor_state = neighbor
            step_cost = cost
            successors_list.append((action, successor_state, step_cost))
        return successors_list
    
    def heuristic(state):
        # Define a simple heuristic function (e.g., straight-line distance)
        heuristic_values = {key: abs(ord(key) - ord(goal_state)) for key in graph.keys()}
        return heuristic_values.get(state, float('inf'))  # Default to infinity if state not found
    
    # Perform A* search using custom successors function
    path = astar_search(start_state, goal_test, successors, heuristic)
    
    # Print the resulting path found by A* search
    if path:
        print("Path found:")
        for action, state in path:
            print(f"Action: {action}, State: {state}")
    else:
        print("No path found.")



"""
$ p3 03Astar_search.py 
Define the graph:
Enter the number of edges: 7
Enter an edge (format: u v cost): A B 1	     
Enter an edge (format: u v cost): A C 3
Enter an edge (format: u v cost): B C 1
Enter an edge (format: u v cost): B D 2
Enter an edge (format: u v cost): C D 1
Enter an edge (format: u v cost): D E 4
Enter an edge (format: u v cost): E G 3
Enter the start state: A
Enter the goal state: G
Path found:
Action: Move to B, State: B
Action: Move to D, State: D
Action: Move to E, State: E
Action: Move to G, State: G

"""
