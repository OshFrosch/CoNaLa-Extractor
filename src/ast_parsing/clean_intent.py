substrings = ['!', '@', '#', '$', ',', '?', '/', ';', '.', "'", ' - ', '"', '`', '%',
              'how can i ', 'how do i ', 'how to ', 'python: ', 'pandas: ', 'matplotlib: ',
              'is there a way to ', 'how do you ', ':']


def clean_intent(intent):
    intent = intent.lower()
    print(intent)
    for substring in substrings:
        intent = intent.replace(substring, "")
    return intent
