import random
import sys

# Function to generate a random tree
# This function creates a tree by iteratively adding nodes.
# For each node 'i' from 2 to 'n', it connects 'i' to a randomly chosen node
# 'j' from the already existing nodes (1 to i-1). This guarantees a tree structure.
def generate_random_tree(n):
    if n == 1:
        return []  # A single node tree has no edges
    edges = []
    for i in range(2, n + 1):
        # Pick a random node from 1 to i-1 to connect to node i
        u = random.randint(1, i - 1)
        v = i
        edges.append((u, v))
    
    # Randomly shuffle the order of edges to make the output less predictable
    random.shuffle(edges)
    return edges

# --- Main Test Case Generator Logic ---

# Constraints from the problem statement:
MAX_T = 100
MAX_N_SUM = 2000  # Sum of 'n' over all test cases
MAX_N_SINGLE = 2000 # Maximum 'n' for a single test case
MAX_A_VALUE = 10**9 # Maximum value for a_i

# Optional: Uncomment the following line to make the generated output deterministic.
# This is useful for debugging the generator itself or for creating consistent test files.
# random.seed(42)

# Determine the total number of test cases
t = random.randint(1, MAX_T)

# List to store the 'n' value for each individual test case
test_case_ns = []
current_n_sum = 0 # Tracks the cumulative sum of 'n' values generated so far

# Distribute 'n' values among 't' test cases
# This logic ensures that:
# 1. Each 'n' is between 1 and MAX_N_SINGLE.
# 2. The total sum of 'n' across all test cases does not exceed MAX_N_SUM.
for i in range(t):
    # 'remaining_n_for_total' is the total 'n' capacity still available from MAX_N_SUM
    # that can be used by the current and all subsequent test cases.
    remaining_n_for_total = MAX_N_SUM - current_n_sum

    # 'min_n_needed_for_future_tests' is the minimum 'n' that must be reserved
    # for the remaining (t - (i + 1)) test cases, where each must have at least 1 node.
    min_n_needed_for_future_tests = (t - (i + 1))

    # Calculate the upper bound for 'n' for the current test case.
    # It must not exceed MAX_N_SINGLE, and it must leave enough 'n'
    # for future test cases to meet their minimum requirements.
    upper_bound_n = min(MAX_N_SINGLE, remaining_n_for_total - min_n_needed_for_future_tests)

    # Ensure the lower bound for 'n' is always at least 1.
    # This guards against cases where 'upper_bound_n' might become 0 or negative
    # if `remaining_n_for_total - min_n_needed_for_future_tests` is very small.
    if upper_bound_n < 1:
        current_n = 1
    else:
        current_n = random.randint(1, upper_bound_n)

    test_case_ns.append(current_n)
    current_n_sum += current_n

# Print the total number of test cases as the first line of the output
print(t)

# Generate and print the detailed input for each test case
for n_val in test_case_ns:
    n = n_val
    x = random.randint(1, n) # Root node, 1-indexed as per problem

    # Print n and x for the current test case
    print(f"{n} {x}")

    # Generate and print initial node values a_i (0-indexed list, but 1-indexed in problem)
    # The '*' operator unpacks the list 'a' so its elements are passed as separate arguments
    # to print(), which prints them space-separated by default.
    a = [random.randint(0, MAX_A_VALUE) for _ in range(n)]
    print(*(a))

    # Generate and print tree edges
    edges = generate_random_tree(n)
    for u, v in edges:
        print(f"{u} {v}")