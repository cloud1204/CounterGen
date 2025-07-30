import sys

def validate_input():
    input_lines = sys.stdin.readlines()
    line_idx = 0

    # Helper to read a line safely
    def read_line():
        nonlocal line_idx
        if line_idx >= len(input_lines):
            return None # End of input
        line = input_lines[line_idx].strip()
        line_idx += 1
        return line

    # Helper to parse space-separated integers from a string
    def parse_ints(s):
        try:
            # Handle empty lines or lines with only whitespace
            if not s:
                return []
            return [int(x) for x in s.split()]
        except ValueError:
            return None # Indicates non-integer content

    # --- Start Validation ---

    # 1. Read t (number of test cases)
    line = read_line()
    if line is None:
        print("invalid: Missing number of test cases (t).")
        return
    
    t_list = parse_ints(line)
    if t_list is None or len(t_list) != 1:
        print("invalid: Invalid format for t (expected a single integer).")
        return
    
    t = t_list[0]
    if not (1 <= t <= 100):
        print(f"invalid: t ({t}) is not within the allowed range [1, 100].")
        return

    total_n_sum = 0 # To track sum of n over all test cases

    for test_case_num in range(1, t + 1):
        # 2. Read n and x for current test case
        line = read_line()
        if line is None:
            print(f"invalid: Test case {test_case_num}: Missing n and x.")
            return
        
        nx_list = parse_ints(line)
        if nx_list is None or len(nx_list) != 2:
            print(f"invalid: Test case {test_case_num}: Invalid format for n and x (expected two integers).")
            return
        
        n, x = nx_list[0], nx_list[1]
        
        if not (1 <= n <= 2000):
            print(f"invalid: Test case {test_case_num}: n ({n}) is not within the allowed range [1, 2000].")
            return
        if not (1 <= x <= n):
            print(f"invalid: Test case {test_case_num}: x ({x}) is not within the allowed range [1, n].")
            return
        
        total_n_sum += n

        # 3. Read a_i values
        line = read_line()
        if line is None:
            print(f"invalid: Test case {test_case_num}: Missing a_i values.")
            return
        
        a_values = parse_ints(line)
        if a_values is None or len(a_values) != n:
            print(f"invalid: Test case {test_case_num}: Incorrect number of a_i values (expected {n}, got {len(a_values) if a_values is not None else 'N/A'}).")
            return
        
        for i, val in enumerate(a_values):
            if not (0 <= val <= 10**9):
                print(f"invalid: Test case {test_case_num}: a_{i+1} ({val}) is not within the allowed range [0, 10^9].")
                return
        
        # 4. Read edges and build adjacency list for tree structure validation
        adj = [[] for _ in range(n + 1)] # 1-indexed adjacency list
        
        for edge_num in range(n - 1):
            line = read_line()
            if line is None:
                # If n > 1, n-1 edges are expected. If input ends prematurely, it's invalid.
                print(f"invalid: Test case {test_case_num}: Missing edge line {edge_num + 1} (expected {n-1} edges).")
                return
            
            uv_list = parse_ints(line)
            if uv_list is None or len(uv_list) != 2:
                print(f"invalid: Test case {test_case_num}: Invalid format for edge {edge_num + 1} (expected two integers u v).")
                return
            
            u, v = uv_list[0], uv_list[1]
            
            if not (1 <= u <= n and 1 <= v <= n):
                print(f"invalid: Test case {test_case_num}: Edge node ({u} or {v}) out of range [1, {n}].")
                return
            if u == v:
                print(f"invalid: Test case {test_case_num}: Edge connects same node (u=v={u}).")
                return
            
            # Add edge to adjacency list (undirected)
            adj[u].append(v)
            adj[v].append(u)
        
        # Validate tree structure: For n nodes and n-1 edges, it's a tree if and only if it's connected.
        if n > 0: # n is guaranteed to be >= 1 by constraints, but defensive programming
            # Use BFS to check connectivity
            visited = [False] * (n + 1)
            q = [1] # Start BFS from node 1 (any node would work)
            if n >= 1: # Only try to visit if there's at least one node
                visited[1] = True
            visited_count = 1
            
            head = 0
            while head < len(q):
                curr = q[head]
                head += 1
                
                for neighbor in adj[curr]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        visited_count += 1
                        q.append(neighbor)
            
            if visited_count != n:
                print(f"invalid: Test case {test_case_num}: Graph is not connected, hence not a tree (visited {visited_count} out of {n} nodes).")
                return
        # If n=0, this block would be skipped, but problem constraints say n >= 1.

    # 5. Check sum of n over all test cases
    if total_n_sum > 2000:
        print(f"invalid: Sum of n over all test cases ({total_n_sum}) exceeds the limit of 2000.")
        return

    # 6. Ensure no extra lines remain in input
    remaining_line = read_line()
    if remaining_line is not None:
        print(f"invalid: Extra data found after all test cases: '{remaining_line}'.")
        return

    # If all checks pass
    print("valid")

# Call the validator function when the script is executed
if __name__ == "__main__":
    validate_input()
