from queue import PriorityQueue

# Define the state class for the Missionaries and Cannibals Problem
class State:
    def __init__(self, left_m, left_c, boat, right_m, right_c):
        self.left_m = left_m  # Number of missionaries on the left bank
        self.left_c = left_c  # Number of cannibals on the left bank
        self.boat = boat      # 1 if boat is on the left bank, 0 if on the right bank
        self.right_m = right_m  # Number of missionaries on the right bank
        self.right_c = right_c  # Number of cannibals on the right bank
    
    def is_valid(self):
        # Check if the state is valid (no missionaries eaten on either bank)
        if self.left_m < 0 or self.left_c < 0 or self.right_m < 0 or self.right_c < 0:
            return False
        if self.left_m > 0 and self.left_c > self.left_m:
            return False
        if self.right_m > 0 and self.right_c > self.right_m:
            return False
        return True
    
    def is_goal(self):
        # Check if the state is the goal state (all missionaries and cannibals on the right bank)
        return self.left_m == 0 and self.left_c == 0
    
    def __lt__(self, other):
        # Define less-than operator for PriorityQueue comparison (used in Best-First Search)
        return False
    
    def __eq__(self, other):
        # Define equality operator for comparing states
        return self.left_m == other.left_m and self.left_c == other.left_c \
               and self.boat == other.boat and self.right_m == other.right_m \
               and self.right_c == other.right_c
    
    def __hash__(self):
        # Define hash function for storing states in a set
        return hash((self.left_m, self.left_c, self.boat, self.right_m, self.right_c))

def successors(state):
    # Generate all valid successor states from the current state
    succ_states = []
    if state.boat == 1:  # Boat is on the left bank
        for m in range(3):
            for c in range(3):
                if 1 <= m + c <= 2:  # Boat capacity is 2
                    new_state = State(state.left_m - m, state.left_c - c, 0,
                                      state.right_m + m, state.right_c + c)
                    if new_state.is_valid():
                        succ_states.append(new_state)
    else:  # Boat is on the right bank
        for m in range(3):
            for c in range(3):
                if 1 <= m + c <= 2:  # Boat capacity is 2
                    new_state = State(state.left_m + m, state.left_c + c, 1,
                                      state.right_m - m, state.right_c - c)
                    if new_state.is_valid():
                        succ_states.append(new_state)
    return succ_states

def best_first_search():
    start_state = State(3, 3, 1, 0, 0)
    goal_state = State(0, 0, 0, 3, 3)
    
    frontier = PriorityQueue()
    frontier.put((0, start_state))  # Priority queue with (cost, state)
    came_from = {}
    cost_so_far = {}
    came_from[start_state] = None
    cost_so_far[start_state] = 0
    
    while not frontier.empty():
        current_cost, current_state = frontier.get()
        
        if current_state == goal_state:
            # Reconstruct the path from start_state to goal_state
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = came_from[current_state]
            path.reverse()
            return path
        
        for next_state in successors(current_state):
            new_cost = cost_so_far[current_state] + 1  # Uniform cost of 1 for each move
            
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost  # Best-First Search uses cost as priority
                frontier.put((priority, next_state))
                came_from[next_state] = current_state
    
    return None  # No path found

def print_solution(path):
    if path is None:
        print("No solution found.")
    else:
        print("Solution found!")
        for i, state in enumerate(path):
            print(f"Step {i}:")
            print(f"Left Bank: {state.left_m} missionaries, {state.left_c} cannibals")
            print(f"Boat is {'on the left' if state.boat == 1 else 'on the right'} bank")
            print(f"Right Bank: {state.right_m} missionaries, {state.right_c} cannibals")
            print("------------")

# Main function to run the Best-First Search and print the solution
if __name__ == "__main__":
    solution_path = best_first_search()
    print_solution(solution_path)
