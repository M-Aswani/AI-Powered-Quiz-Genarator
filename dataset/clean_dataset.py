import json

# Load our 100 CS questions
with open("dataset/cs_questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Total questions:", len(data))

# Check missing questions
missing_questions = [
    item for item in data
    if not item.get("question")
]

# Check missing answers
missing_answers = [
    item for item in data
    if not item.get("answer")
]

# Check missing options
missing_options = [
    item for item in data
    if not item.get("options")
]

# Check duplicate questions
questions = [item["question"].strip() for item in data]

duplicates = set(
    question for question in questions
    if questions.count(question) > 1
)

print("\n--- Cleaning Report ---")
print("Missing questions:", len(missing_questions))
print("Missing answers:", len(missing_answers))
print("Missing options:", len(missing_options))
print("Duplicate questions:", len(duplicates))

if (
    len(missing_questions) == 0
    and len(missing_answers) == 0
    and len(missing_options) == 0
    and len(duplicates) == 0
):
    print("\nDataset is clean!")
else:
    print("\nSome issues need to be checked.")