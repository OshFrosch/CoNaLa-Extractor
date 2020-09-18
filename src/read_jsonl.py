import jsonlines
from tqdm import tqdm

from src.parse_python import parse_code_string
from src.file_len import file_len

total_lines = file_len('../res/conala-corpus/conala-mined.jsonl')
substrings = ['!', '@', '#', '$', ':', ',', '?', '/', ';', '.', "'", ' - ', '"', '`', '%',
              'how can i ', 'how do i ', 'how to ', 'python: ', 'pandas: ', 'matplotlib: ',
              'is there a way to ', 'how do you ']

progress_bar = tqdm(total=total_lines, desc="Parsing Python snippets")

with open("../res/created/python_small.json", "w") as outfile_0:

    with open("../res/created/python_small_target.json", "w") as outfile_1:

        with jsonlines.open('../res/conala-corpus/conala-mined.jsonl') as infile:

            for line in infile.iter():
                progress_bar.update(n=1)
                snippet = line['snippet']
                intent = line['intent']
                try:
                    intent = intent.lower()
                    for substring in substrings:
                        intent = intent.replace(substring, "")
                    ast_line = parse_code_string(snippet)
                except (AttributeError, TypeError, SyntaxError) as e:
                    pass
                try:
                    outfile_0.write(ast_line + '\n')
                    outfile_1.write(intent + '\n')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass

        infile.close()

    outfile_0.close()

outfile_1.close()
