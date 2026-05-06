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
        cost = float(cost)
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, cost))
    return graph

def ao_star_search(start_state, goal_state, graph):
    frontier = []
    heapq.heappush(frontier, Node(start_state, None, None, 0, heuristic(start_state, goal_state)))
    explored = {}
    
    while frontier:
        current_node = heapq.heappop(frontier)
        current_state = current_node.state
        
        if current_state == goal_state:
            # Reconstruct the path from the goal node to the start node
            path = []
            while current_node.parent is not None:
                path.append((current_node.action, current_node.state))
                current_node = current_node.parent
            path.reverse()
            return path
        
        if current_state not in explored or current_node.cost < explored[current_state]:
            explored[current_state] = current_node.cost
            
            for neighbor, step_cost in graph.get(current_state, []):
                new_cost = current_node.cost + step_cost
                new_node = Node(neighbor, current_node, f"Move to {neighbor}", new_cost, heuristic(neighbor, goal_state))
                heapq.heappush(frontier, new_node)
    
    return None  # No path found

def heuristic(state, goal_state):
    # Simple heuristic function (e.g., straight-line distance)
    heuristic_values = {'A': 5, 'B': 3, 'C': 2, 'D': 1, 'E': 2, 'G': 0}  # Custom heuristic values based on problem domain
    return heuristic_values.get(state, float('inf'))  # Default to infinity if state not found

if __name__ == "__main__":
    # Get user input to define the graph
    print("Define the graph:")
    graph = parse_graph_input()
    
    start_state = input("Enter the start state: ")
    goal_state = input("Enter the goal state: ")
    
    # Perform AO* search using the defined graph, start state, and goal state
    path = ao_star_search(start_state, goal_state, graph)
    
    # Print the resulting path found by AO* search
    if path:
        print("Path found:")
        for action, state in path:
            print(f"Action: {action}, State: {state}")
    else:
        print("No path found.")




"""
$ p3 04AOstar_search.py 
Define the graph:
Enter the number of edges: 8
Enter an edge (format: u v cost): S A 3
Enter an edge (format: u v cost): S B 2
Enter an edge (format: u v cost): A C 4
Enter an edge (format: u v cost): A D 2
Enter an edge (format: u v cost): B E 3
Enter an edge (format: u v cost): C G 2
Enter an edge (format: u v cost): D G 5
Enter an edge (format: u v cost): E G 4
Enter the start state: S
Enter the goal state: G
Path found:
Action: Move to B, State: B
Action: Move to E, State: E
Action: Move to G, State: G

"""
