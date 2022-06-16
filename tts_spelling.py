from os import system as execute_command
import pyttsx3
import json

print('Pulling from github...')
execute_command('git pull')

WORD_FILE_PATH = 'spelling_level.json'
tts = pyttsx3.init()
tts.setProperty('rate', 125)


def speak(text):
  tts.say(text)
  tts.runAndWait()


def read_file(file_name):
  with open(file_name, 'r') as f:
    return json.load(f)


def write_file(file_name, data):
  with open(file_name, 'w') as f:
    json.dump(data, f, indent=2)


def get_input_spelling(prompt):
  return input(prompt).strip().lower()


data = read_file(WORD_FILE_PATH)
level_min = min(data.values())

print('Press Ctrl+C anytime to quit')

while True:
  try:
    for word, level in data.items():
      if level == level_min:
        input_spelling = 'r'
        while input_spelling == 'r':
          speak(word)
          input_spelling = get_input_spelling('Input \'r\' to repeat: ')
        if input_spelling == word:
          data[word] += 1
        else:
          data[word] -= 1
          while input_spelling != word:
            input_spelling = get_input_spelling(f'Incorrect spelling. Correct spelling: {word}'
                                                '\nTry again: ')
        input()
    level_min = min(data.values())
  except KeyboardInterrupt:
    break

print()
print('Saving file...')
write_file(WORD_FILE_PATH, data)
print('Done')
print('Pushing to github...')
execute_command('git add .')
execute_command('git commit -m "Update spelling level"')
execute_command('git push')
print('Done')
print('Exiting...')
