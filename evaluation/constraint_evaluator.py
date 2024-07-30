import csv

def calculate_correctness(ground_truth, found, alpha):
    """
    Calculate the correctness of found constraints against ground-truth constraints.
    
    Parameters:
    - ground_truth: Dictionary of ground-truth constraints.
    - found: Dictionary of found constraints.
    - alpha: Weighting factor for template errors.
    
    Returns:
    - List of correctness scores (precision, recall, F1) for each sentence.
    """
    global no_of_samples
    global template_errors
    template_errors = 0
    no_of_samples = 0

    correctness_scores = []
    for sentence, ground_constraint in ground_truth.items():
        no_of_samples += 1
        if sentence in found:
            found_constraint = found[sentence]
            if(found_constraint == ""): #if found constraint is empty
                correctness_scores.append((0,0,0))
                template_errors +=1
                continue
            TP = 0
            FP = 0
            FN = 0
            # Check if constraint type is correct
            if ground_constraint.split('(')[0] == found_constraint.split('(')[0]:
                TP = TP + alpha*1
                if(len(ground_constraint.split('(')[1].split(',')) == 1):
                    #we have unary ground truth constraint
                    if(len(found_constraint.split('(')[1].split(',')) == 1):
                        #we have unary found constraint
                        if ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0]: #check activity (only one)
                            TP = TP + 1
                        else:
                            FP = FP +1
                            FN = FN +1
                    elif(len(found_constraint.split('(')[1].split(',')) == 2):
                        #we have binary found constraint
                        #Check if one activity of the found constraint corresponds to the one of the ground truth constraint
                        if(ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0] or ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[1]):
                            TP = TP +1
                        else:
                            FN = FN +1 
                elif(len(ground_constraint.split('(')[1].split(',')) == 2):
                    #we have binary ground truth constraint
                    if(len(found_constraint.split('(')[1].split(',')) == 2):
                        #we have binary found constraint
                        # Check if first activity is correct
                        if ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0]:
                            TP = TP +1
                        else:
                            FP = FP +1
                            FN = FN +1
                        # Check if second activity is correct
                        if ground_constraint.split('(')[1].split(',')[1][:-1] == found_constraint.split('(')[1].split(',')[1][:-1]:
                            TP = TP +1
                        else:
                            FP = FP +1
                            FN = FN +1
                    elif(len(found_constraint.split('(')[1].split(',')) == 1):
                        #we have unary found constraint
                        #check the one activity of the found unary constraint occurs in the binary ground truth constraint
                        if(ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0] or ground_constraint.split('(')[1].split(',')[1] == found_constraint.split('(')[1].split(',')[0]):
                            TP = TP +1
                        else:
                            FP = FP +1

            else:
                template_errors += 1
                FP = FP + alpha*1
                FN = FN + alpha*1
                print("Template error in sentence:\n", sentence, "\n Found:", found_constraint, "Is: ", ground_constraint)
                
                if(len(ground_constraint.split('(')[1].split(',')) == 1): 
                    #we have unary ground truth constraint
                    if(len(found_constraint.split('(')[1].split(',')) == 1):
                        #we have unary found constraint
                        # Check if only activity is correct
                        if ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0]:
                            TP = TP +1
                        else:
                            FP = FP +1 
                            FN = FN + 1
                    elif(len(found_constraint.split('(')[1].split(',')) == 2):
                        #we have binary found constraint
                        #Check if one activity of the found constraint corresponds to the one of the ground truth constraint
                        if(ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0] or ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[1]):
                            TP = TP +1
                        else:
                            FN = FN +1
                elif(len(ground_constraint.split('(')[1].split(',')) == 2):
                    #we have binary ground truth constraint
                    if(len(found_constraint.split('(')[1].split(',')) == 1):
                        #we have unary found constraint
                        #check the one activity of the found unary constraint occurs in the binary ground truth constraint
                        if(ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0] or ground_constraint.split('(')[1].split(',')[1] == found_constraint.split('(')[1].split(',')[0]):
                            TP = TP +1
                        else:
                            FP = FP +1
                    elif(len(found_constraint.split('(')[1].split(',')) == 2):
                        #we have binary found constraint
                        #check both activities
                        # Check if first activity is correct
                        if ground_constraint.split('(')[1].split(',')[0] == found_constraint.split('(')[1].split(',')[0]:
                            TP = TP +1
                        else:
                            FP = FP +1 
                            FN = FN + 1

                        # Check if second activity is correct
                        if ground_constraint.split('(')[1].split(',')[1][:-1] == found_constraint.split('(')[1].split(',')[1][:-1]:
                            TP = TP +1
                        else:
                            FP = FP +1 
                            FN = FN + 1       
            if(TP+FP == 0):
                precision = 0
            else:
                precision = TP / (TP+FP)
            if(TP+FN == 0):
                recall = 0
            else:
                recall = TP / (TP+FN)
            if(precision + recall == 0):
                F1 = 0
            else:
                F1 = (2*precision*recall) / (precision+recall)
            correctness_scores.append((precision, recall, F1))
    return correctness_scores

def compute_overall_accuracy(correctness_scores):
    """
    Compute the overall accuracy from correctness scores.
    
    Parameters:
    - correctness_scores: List of tuples containing (precision, recall, F1).
    
    Returns:
    - Tuple of overall (precision, recall, F1) scores.
    """
    overall_precision = 0
    overall_recall = 0
    overall_F1 = 0
    if len(correctness_scores) == 0:
        return 0.0
    else:
        for (precision, recall, F1) in correctness_scores:
            overall_precision += precision
            overall_recall += recall
            overall_F1 += F1
        return overall_precision / len(correctness_scores), overall_recall / len(correctness_scores), overall_F1 / len(correctness_scores)

def evaluate(ground_truth_file, found_file):
    """
    Evaluate the constraints by comparing found constraints against ground-truth data.
    
    Parameters:
    - ground_truth_file: Path to the ground-truth CSV file.
    - found_file: Path to the found constraints CSV file.
    
    Returns:
    - Overall accuracy as a tuple (precision, recall, F1).
    """
    ground_truth = {}
    with open(ground_truth_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            ground_truth[row[0]] = row[1]

    found = {}
    with open(found_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            found[row[0]] = row[1]

    correctness_scores = calculate_correctness(ground_truth, found, ALPHA)
    overall_accuracy = compute_overall_accuracy(correctness_scores)
    return overall_accuracy

# Paths to CSV files
GROUND_TRUTH_FILE = 'path/to/ground_truth.csv'
FOUND_FILE = 'path/to/found_results.csv'


# weighting coefficient alpha, determines how mch the template slot should be weighted. The higher alpha, the smaller the penalty for activity errors. 
ALPHA = 2

# Evaluate and print overall accuracy
accuracy = evaluate(GROUND_TRUTH_FILE, FOUND_FILE)
print("Overall precision:", accuracy[0])
print("Overall recall:", accuracy[1])
print("Overall F1:", accuracy[2])
print("No. of sentences/constraints in test dataset:", no_of_samples)
print("No. of template errors:", template_errors)
print("Template accuracy:", 1-(template_errors/no_of_samples))