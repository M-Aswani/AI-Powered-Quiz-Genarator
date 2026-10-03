import json

# Load current CS questions dataset
with open("dataset/cs_questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Total questions:", len(data))

all_correct = True

for i, item in enumerate(data, start=1):

    options = item["options"]
    answer_index = item["answer_index"]

    # Check exactly 4 options
    if len(options) != 4:
        print(f"Question {i}: ERROR - {len(options)} options")
        all_correct = False

    # Check answer index
    if answer_index < 0 or answer_index > 3:
        print(
            f"Question {i}: ERROR - answer_index = {answer_index}"
        )
        all_correct = False

if all_correct:
    print("All questions have exactly 4 options.")
    print("All answer indexes are between 0 and 3.")
    print("Dataset is ready for the quiz!")

else:
    print("There is a problem in the dataset.")