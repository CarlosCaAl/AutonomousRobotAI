# Prompt strategy in this code is a modification of https://github.com/garagesteve1155/chatgpt_robot
# Here, the AI is asked for a Python code rather than a dictionary

from Thread import Run #Function to run threads
from System import read, PATH

import datetime
import time
from groq import Groq # Import Groq for AI model interaction
import base64

API_KEY = read("data.json")["api"]

def encode_image(image_path): # Function to encode an image to base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
class ArtificialIntelligence:
    def __init__(self):
        self.log = [] # Log to keep track of conversations
        self.summary = "No summary yet." # Initialize summary
        self.code_state = "No code runned."
        self.remember_info = [] # List to remember information
        self.summarized = True # Flag to check if summary is ready and no information is being summarized
        self.client = Groq(api_key=API_KEY) # Groq client
        self.system_prompt = read("ai/system_prompt.txt") # Read system.txt for system instructions
        self.python_errors = read("ai/python_errors.txt")
        self.autonomous = read("ai/autonomous_small.txt")

    def close(self): self.client.aclose() # Close the Groq client connection
    def completion(self,question): # Function to get a completion from the AI model
        return self.client.chat.completions.create(model="meta-llama/llama-4-scout-17b-16e-instruct",messages=question,temperature=0.5).choices[0].message

    def auto(self, prompt, image=None, distance = None): # Function to complete autonomously a task
        question = []
        question.append({"role": "system", "content": self.autonomous})
        question.append({"role": "user", "content": f"**YOUR PROMPT:** {prompt}"})
        for info in self.remember_info[-6:]:
            question.append({"role": "user", "content": "Remember information: " + info})
        question.append({"role": "user", "content": f"Distance sensor: {distance}cm\n"})
        if image is not None:
            question.append({"role": "user", "content":[{"type": "text", "text": f"Robot's camera image."},{"type": "image_url","image_url": {"url": "data:image/jpeg;base64,{}".format(encode_image(PATH+"cam/Foto{}.jpg".format(image)))}}]})

        ans = self.completion(question)
        self.log.append({"role": "user", "content": prompt})
        self.log.append({"role": "assistant", "content": ans.content})
        answer = ans.content
        return answer # Python code

    def answer(self, prompt, image=None, name = "Nobody", ip = None, distance = None): # Function to process the user's prompt, return an AI response and run Python code
        if prompt == False or prompt == "": prompt = "**No mic input**"
        while not self.summarized: time.sleep(0.1) # Wait until summary is ready

        question = []
        question += self.log[-6:]
        #question.append({"role": "user", "content": self.summary})
        #question.append({"role": "user", "content": "Remember Info: " + str(self.remember_info[-6:])})
        question.append({"role": "system", "content": self.system_prompt})
        question.append({"role": "user", "content": "Past python code errors: " + self.python_errors})
        question.append({"role": "user", "content": f" - Date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n - Distance sensor (metres): {distance}\n - App ip: {ip}\n - Python code state: {self.code_state}"})
        if image is not None:
            question.append({"role": "user", "content":[{"type": "text", "text": f"Person in the image: {name}. Use this information to respond appropriately."},{"type": "image_url","image_url": {"url": "data:image/jpeg;base64,{}".format(encode_image(PATH+"cam/Photo{}.jpg".format(image)))}}]})
        question.append({"role": "user", "content": f"Mic Input ({name}): {prompt}"})
        
        ans = self.completion(question)
        self.log.append({"role": "user", "content": prompt})
        self.log.append({"role": "assistant", "content": ans.content})
        answer = ans.content
        #Run(self.summarize)
        return answer # Python code

    def remember_information(self, info): # Function to remember information
        self.remember_info.append(info)
    def summarize(self): # Function to summarize the conversation
        self.summarized = False
        question = []
        question.append({"role": "user", "content": "Current Conversation: " + str(self.log[-10:])})
        summary = self.completion([{"role": "user", "content": "Make a four sentence summary of this conversation history so you know what we talked about in previous conversations (These summaries will be included in the normal prompts). The summary must be worded in first person from Robot's point of view. Mic input is what Robot hears people say. All other user role messages are your sensor, camera, and internal data. Assistant responses are your command choices at those moments in time."}]+question)
        self.summary = summary.content
        self.summarized = True
        
if __name__ == "__main__":
    
    ai = ArtificialIntelligence()
    while True:
        code = ai.answer(input("USER: "))
        Run(exec(code))
        time.sleep(0.1)