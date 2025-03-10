import threading
import time
import os
import platform
import json
import queue
import requests
from SpeakSound import speak
from llama_cpp import Llama
from task_executor import TaskExecutor
from fuzzywuzzy import process

class VoiceAssistant:
    def __init__(self, wake_word="virgil", model_path="/home/pi/models/llama.gguf"):
        self.wake_word = wake_word.lower()
        self.running = True
        
        # Initialize Llama.cpp model
        self.model = Llama(model_path)
        
        self.speak_lock = threading.Lock()
        self.task_queue = queue.Queue()
        self.task_executor = TaskExecutor()
        
        # Identify OS-specific task knowledge file
        self.current_os = platform.system().lower()
        self.knowledge_file = f"{self.current_os}_task_knowledge.json"

        if not os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, "w") as f:
                json.dump({}, f)
    
    def receive_audio_text(self):
        """
        Receives transcribed text from the client device.
        """
        try:
            response = requests.get("http://client_device_ip:5000/get_audio_text")  # Replace with actual client IP
            if response.status_code == 200:
                return response.json().get("text", "").lower()
        except requests.RequestException as e:
            print(f"Error receiving audio text: {e}")
        return ""
    
    def send_response_audio(self, text):
        """
        Sends response text to the client device for TTS output.
        """
        try:
            requests.post("http://client_device_ip:5000/send_response", json={"text": text})  # Replace with actual client IP
        except requests.RequestException as e:
            print(f"Error sending response: {e}")
    
    def is_command(self, text):
        """
        Determines if the given input text is a command.
        """
        command_keywords = {"open", "run", "start", "execute", "launch", "command"}
        words = set(text.lower().split())
        if words & command_keywords:
            return True
        
        query = f"Is the following input a task or a general question? Respond with either 'task' or 'question'. Input: '{text}'"
        response = self.model(query).strip().lower()
        return response == "task"
    
    def respond(self, text):
        print(f"Processing input: {text}")

        if self.is_command(text):
            command_keywords = {"open", "run", "start", "execute", "launch", "command"}
            for keyword in command_keywords:
                if keyword in text:
                    text = text.replace(keyword, "").strip()
            self.process_command(text)
        else:
            response = self.model(text)
            self.send_response_audio(response)
    
    def listen_and_respond(self):
        print("Voice Assistant is running. Say the wake word to activate.")
        while self.running:
            print("Awaiting input...")
            command = self.receive_audio_text()
            if not command:
                continue

            if self.wake_word in command:
                print("Wake word detected! Awaiting command...")
                self.send_response_audio("Yes?")
                command = self.receive_audio_text()
                if command:
                    self.respond(command)
            else:
                print("Wake word not detected, ignoring input.")
    
    def stop(self):
        print("Stopping the assistant...")
        self.running = False

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.send_response_audio("Hello sir")
    try:
        assistant.listen_and_respond()
    except KeyboardInterrupt:
        assistant.stop()
