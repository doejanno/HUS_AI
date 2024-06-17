import torch

# Create a tensor from a list
tensor_data = torch.tensor([1, 2, 3])

# Create a matrix (2D tensor)
matrix_data = torch.tensor([[1, 2], [3, 4]])

# Get the size of a tensor
print(tensor_data.size())  # Output: torch.Size([3])
print(matrix_data.size())  # Output: torch.Size([2, 2])
