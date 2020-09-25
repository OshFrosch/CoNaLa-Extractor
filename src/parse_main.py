import jsonlines
from tqdm import tqdm

from src.ast_parsing.parse_python import parse_code_string
from src.ast_parsing.clean_intent import clean_intent
from src.helper.file_len import file_len

total_lines = file_len('../res/conala-corpus/conala-mined.jsonl')

progress_bar = tqdm(total=total_lines, desc="Parsing Python snippets")

with open("../res/created/parsed/python_small.json", "w") as outfile_0:

    with open("../res/created/parsed/python_small_target.json", "w") as outfile_1:

        with jsonlines.open('../res/dataset/conala-corpus/conala-mined.jsonl') as infile:

            for line in infile.iter():
                progress_bar.update(n=1)
                snippet = line['snippet']
                intent = line['intent']
                try:
                    cleaned_intent = clean_intent(intent)
                    ast_line = parse_code_string(snippet)
                except (AttributeError, TypeError, SyntaxError) as e:
                    pass
                try:
                    outfile_0.write(ast_line + '\n')
                    outfile_1.write(cleaned_intent + '\n')
                except (UnicodeEncodeError, UnicodeDecodeError) as e:
                    pass

        infile.close()

    outfile_0.close()

outfile_1.close()
