def print_fixed_width_list(list_data, width=56):
  """Prints a list with varying length items in a fixed-width field.

  Args:
    list_data: The list of items to print.
    width: The desired width of the output field.
  """
  print(f'"{str(list_data)}"')
  list_str = str(list_data)
  padding = width - len(list_str)
  return list_str + " " * padding

# Example usage:
my_list = [1, 2, 3]
print(f'{print_fixed_width_list(my_list,width=30)}  fred')