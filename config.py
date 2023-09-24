
# Morse Code Convention
TIME_UNIT = 1.0  # 1 second time unit
DOT_DURATION = TIME_UNIT  # Duration for 'dot'
DASH_DURATION = 3 * TIME_UNIT  # Duration for 'dash'
LETTER_SPACE_DURATION = 3 * TIME_UNIT  # Space between letters
WORD_SPACE_DURATION = 7 * TIME_UNIT  # Space between words
DEBOUNCE_TIME = 0.05

# MORSE CODE DICTIONARY
MORSE_CODE_DICT = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----'
}

# GPIO Wiring
MORSE_INPUT_PIN = 27

