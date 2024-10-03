from collections import Counter
from pathlib import Path

def print_majority_vote(file_names, output_file):
    predictions = []
    
    # Get the absolute path of the directory containing the script
    script_location = Path(__file__).absolute().parent
    
    # Determine the number of samples in the shortest file
    min_num_samples = float('inf')
    for file_name in file_names:
        file_path = script_location / file_name
        num_samples = sum(1 for line in open(file_path))
        min_num_samples = min(min_num_samples, num_samples)
    
    # Read predictions from each file and perform majority vote
    for file_name in file_names:
        file_path = script_location / file_name
        with open(file_path, 'r') as file:
            file_predictions = [next(file).strip() for _ in range(min_num_samples)]
            predictions.append(file_predictions)

    # Majority vote
    majority_vote = [Counter(sample).most_common(1)[0][0] for sample in zip(*predictions)]
    
    # Write majority vote to file
    with open(output_file, 'w') as fout:
        fout.write("Majority Vote:\n")
        for i, prediction in enumerate(majority_vote):
            fout.write("Sample %d: %s\n" % (i+1, prediction))

# Define file names for predictions and output file
file_names = ["RNN_predictions.txt", "CNN_predictions.txt", "MLP_predictions.txt"]
output_file = "majority_vote_results.txt"

# Call the function
print_majority_vote(file_names, output_file)