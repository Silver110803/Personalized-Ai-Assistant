from openai import OpenAI

client = OpenAI(
    api_key = "sk-x11jUhhrDC4c3wGqch7869y8PxrMmt-rf7jAqzUI8dT3BlbkFJTWF-75Qm38FylRqcH3rGLAkk4WGRNuHAAqW5w9uWUA",
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like alexa and Goofle loud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)