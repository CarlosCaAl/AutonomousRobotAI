**AUTONOMOUS ROBOT POWERED BY GENERATIVE AI**

``Numbers move the world project: Robot based on Raspberry Pi 4``


**Configuration**
- Run ``Config.py`` to register email and ip
- Run ``Config.py`` to complete the speed Callibration (run this as many times you need)
- Write down BT address of your devices ``files/bt.json``
- Write down tuya API keys and IDs ``files/tuya.json``

**Language**
- Install the respective vosk model ``files/audio/vosk-model-X``
- Modify ``Assistant.py`` with your language

**Additional devices**
- USB mic input
- BT speaker
- PlayStation wireless controller (optional)
- BT arduino device (optional)

**Run code**
- Robot's rpi (sudo is required for ws281x) --> ``sudo python3 /path/to/main.py``
- Another computer connected to the same WiFi --> ``python3 /path/to/App.py``

**Wiring**
- Ultrasonic sensor
- Motor controller
- Servo controller
- Neopixel 8x8 matrix
- Power Bank supply

**APIs needed**
- Groq API: It gives access to completely free generative AIs (Ollama is a great alternative for 32-bit os)
- Tuya API: Control smart plugs remotely
- Berserk API: Play lichess games from python

**Sources**
- Prompt strategy in this code is a modification of https://github.com/garagesteve1155/chatgpt_robot
- Project development (in spanish) https://carloscaal.eu.pythonanywhere.com/

**Requirements**
- Libraries (depend on rpi version)
- Python 3 installed
- Raspberry Pi 4 software (Raspbian)
