import json
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)

# 1. Load training data
with open("dataset/academic_training_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    

print("Total training examples:", len(data))

# 2. Convert JSON data into Hugging Face Dataset
dataset = Dataset.from_list(data)

# 3. Load FLAN-T5 model and tokenizer
model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 4. Tokenize the data
def tokenize_function(examples):
    inputs = tokenizer(
        examples["input"],
        max_length=256,
        truncation=True
    )

    targets = tokenizer(
        examples["target"],
        max_length=128,
        truncation=True
    )

    inputs["labels"] = targets["input_ids"]

    return inputs


tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names
)

# 5. Training settings
training_args = TrainingArguments(
    output_dir="./flan_t5_output",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_strategy="epoch",
    logging_steps=10
)

# 6. Data collator
data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model
)

# 7. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

# 8. Start training
trainer.train()

# 9. Save trained model
trainer.save_model("./trained_model")
tokenizer.save_pretrained("./trained_model")

print("FLAN-T5 training completed successfully!")