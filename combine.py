import itertools

# Define the list
my_list = ['a', 'b', 'c']

# Generate all unique combinations
unique_combinations = []
for r in range(1, len(my_list) + 1):
    combinations = itertools.combinations(my_list, r)
    unique_combinations.extend(combinations)

# Print the results
for combination in unique_combinations:
    print(list(combination))