import json
import random

# Load CS questions
with open("dataset/cs_questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

training_data = []

for item in data:

    question = item["question"]
    options = item["options"]
    answer_index = int(item["answer_index"])

    # Find the correct answer
    correct_answer = options[answer_index]

    # Get wrong answers
    wrong_options = [
        option
        for i, option in enumerate(options)
        if i != answer_index
    ]

    # Select 3 wrong answers
    selected_wrong = random.sample(
        wrong_options,
        3
    )

    # Create exactly 4 options
    new_options = [
        correct_answer,
        selected_wrong[0],
        selected_wrong[1],
        selected_wrong[2]
    ]

    # Shuffle the 4 options
    random.shuffle(new_options)

    # Find new correct answer index
    new_answer_index = new_options.index(correct_answer)

    # Update the question data
    item["options"] = new_options
    item["answer_index"] = new_answer_index

    # Correct answer letter
    correct_letter = chr(65 + new_answer_index)

    item["answer"] = correct_letter

    # Create options text for FLAN-T5
    options_text = ""

    for i, option in enumerate(new_options):

        letter = chr(65 + i)

        options_text += (
            f"{letter}. {option}\n"
        )

    # Input for FLAN-T5
    input_text = (
        "Question:\n"
        + question
        + "\n\nOptions:\n"
        + options_text
        + "\nAnswer:"
    )

    # Training target
    target_text = correct_answer

    record = {
        "input": input_text,
        "target": target_text
    }

    training_data.append(record)


# Save the corrected 4-option dataset
with open(
    "dataset/cs_questions.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        data,
        file,
        indent=2,
        ensure_ascii=False
    )


# Save FLAN-T5 training data
with open(
    "dataset/academic_training_data.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        training_data,
        file,
        indent=2,
        ensure_ascii=False
    )


print("Dataset converted successfully!")
print("Every question now has exactly 4 options.")
print("Total questions:", len(data))
print("FLAN-T5 training data created successfully!")