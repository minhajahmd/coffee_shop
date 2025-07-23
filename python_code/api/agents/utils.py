# Contains reusable helper functions.
# Keeps common utilities separate from agent logic to avoid code duplication.

def get_chatbot_response(client, model_name, messages, temperature=0):
    input_messages = []     # Store conversation history
    # Copy user messages to input_messages in the required format
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    # Send a request to the model to generate a response
    response = client.chat.completions.create(
    model=model_name,
    messages=input_messages,
    # Temperature controls the creativity of the response
    # Lower values give more predictable answers, higher values give more creative answers
    temperature=temperature,  # 0.0 = factual, no randomness

    # top_p controls the diversity of responses. It looks at the most probable tokens
    # Lower values make the response more focused, higher values allow more randomness
    top_p=0.8,  # 0.8 = consider 80% of the most probable tokens for the response

    # max_tokens limits how long the model’s response can be
    # 2000 tokens is a large number, allowing long responses
    max_tokens=2000,  # Maximum length of the model's response (in tokens)
    ).choices[0].message.content
    return response

def get_embedding(embedding_client, model_name, text_input):
    output = embedding_client.embeddings.create(
        input=text_input,
        model=model_name
    )

    embeddings = []
    for embedding_object in output.data:
        embeddings.append(embedding_object.embedding)
    return embeddings

def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is already correct just return it.

    If there is any text before or after the json string, remove it.
    Do NOT return a single letter outside of the json string.
    The first thing you write should be the opening curly brace of the json string and the last thing you write should be the closing curly brace of the json string.

    You should check the json string for the following text:
    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]        #That's a clear task, so it fits the "user" role.

    response = get_chatbot_response(client,model_name,messages)
    response = response.replace("\\n", "").replace("\n", "").strip()     # Remove any newlines or extra spaces

    return response
