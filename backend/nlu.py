import rasa_nlu

# Load the training data
training_data = rasa_nlu.load_data("data.json")

# Train the model
interpreter = rasa_nlu.train(training_data)

# Save the model
rasa_nlu.persist(interpreter, "models")

# Define a function to process user input
async def process_input(input):
    # Parse the input using Rasa NLU
    result = await interpreter.parse(input)

    # Extract the intent and entities
    intent = result.intent
    entities = result.entities

    # Generate a response based on the intent and entities
    response = ""
    if intent == "greet":
        response = f"Hello, {entities['name']}!"
    else:
        response = "I didn't understand that."

    # Return the response
    return response
