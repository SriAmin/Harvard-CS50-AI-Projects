import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            #Create a temporary list and append values based on .csv files
            #print(row)
            tempEvidence = []
            
            tempEvidence.append(int(row[0]))

            tempEvidence.append(float(row[1]))

            tempEvidence.append(int(row[2]))

            tempEvidence.append(float(row[3]))

            tempEvidence.append(int(row[4]))

            tempEvidence.append(float(row[5]))

            tempEvidence.append(float(row[6]))

            tempEvidence.append(float(row[7]))

            tempEvidence.append(float(row[8]))

            tempEvidence.append(float(row[9]))

            #Based on row["Month"] it'll append number 0-11, December by default
            if (row[10] is "Jan"):
                tempEvidence.append(0)
            elif (row[10] is "Feb"):
                tempEvidence.append(1)
            elif (row[10] is "Mar"):
                tempEvidence.append(2)
            elif (row[10] is "Apr"):
                tempEvidence.append(3)
            elif (row[10] is "May"):
                tempEvidence.append(4)
            elif (row[10] is "June"):
                tempEvidence.append(5)
            elif (row[10] is "Jul"):
                tempEvidence.append(6)
            elif (row[10] is "Aug"):
                tempEvidence.append(7)
            elif (row[10] is "Sep"):
                tempEvidence.append(8)
            elif (row[10] is "Oct"):
                tempEvidence.append(9)
            elif (row[10] is "Nov"):
                tempEvidence.append(10)
            else:
                tempEvidence.append(11)    
            

            tempEvidence.append(int(row[11]))

            tempEvidence.append(int(row[12]))

            tempEvidence.append(int(row[13]))

            tempEvidence.append(int(row[14]))

            #Use VisitorType to append either 1 or 0 representing that field
            if (row[15] is "Returning_Visitor"):
                tempEvidence.append(1)
            else:
                tempEvidence.append(0)
            #Depending on Weekend value, it'll append either 1 for True and 0 for False
            if (row[16] is True):
                tempEvidence.append(1)
            else:
                tempEvidence.append(0)

            #Appends tempEvidence list in evidence list and row["Revenue"] in labels list
            evidence.append(tempEvidence)

            if (row[17] == "TRUE"):
                labels.append(1)
            else:
                labels.append(0)
                
        return (evidence, labels)                        


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    #Intiate a model, train it with evidence and labels, and return that trained model
    model = KNeighborsClassifier()
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0.0
    specificity = 0.0
    numPos = 0
    numNeg = 0

    #Get the number of positive values and negative values
    for label in labels:
        if label == 1:
            numPos = numPos + 1
        elif label == 0:
            numNeg = numNeg + 1
        else:
            continue
    
    #Go through labels and predictions to calculate sentivity and specificity
    for label, prediction in zip(labels, predictions):
        if prediction == label and label is 1:
            sensitivity = sensitivity + 1
        elif prediction == label and label is 0:
            specificity = specificity + 1
        else:
            continue

    #Divide by length so both sensitivty and specificty are between 0 to 1
    sensitivity = sensitivity / numPos
    specificity = specificity / numNeg            

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
