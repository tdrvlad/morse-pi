print('Initializing.')
import time
# Time needed for Raspberry Pi to initialize
time.sleep(15)

print("Starting Morse Pi.")
from morse_pi.morse import run
run()
