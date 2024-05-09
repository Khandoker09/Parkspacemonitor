import pickle

# Path to your pickle file
pickle_file_path = 'area.pkl'

# Open the pickle file and load data
with open(pickle_file_path, 'rb') as file:
    data = pickle.load(file)

# Print the data loaded from the pickle file
print(data)

# Optionally, print the type of the loaded data
print(type(data))
