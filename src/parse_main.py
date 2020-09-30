import jsonlines
from tqdm import tqdm
from sklearn import model_selection as sklearn_model_selection
from src.ast_parsing.parse_python import parse_code_string
from src.ast_parsing.clean_intent import clean_intent
from src.helper.file_len import file_len

dataset = "../res/dataset/conala-corpus/conala-mined.jsonl"
output_train = "../res/created/parsed/python_small.json"
create_ast = True
valid_p = 0.2


def main():
    total_lines = file_len(dataset)

    python_small = []

    progress_bar_parse = tqdm(total=total_lines, desc="Parsing Python snippets")

    with jsonlines.open(dataset) as infile:

        for line in infile.iter():
            progress_bar_parse.update(n=1)
            snippet = line['snippet']
            intent = line['intent']
            try:
                cleaned_intent = clean_intent(intent)
                ast_line = parse_code_string(snippet)

                python_small.append([cleaned_intent, ast_line])

            except (AttributeError, TypeError, SyntaxError):
                pass

    infile.close()

    # train/eval split

    train, eval = sklearn_model_selection.train_test_split(
        python_small,
        test_size=valid_p,
    )

    progress_bar_split = tqdm(total=total_lines, desc="Creating train/eval", position=0, leave=True)

    for split_name, split in zip(
            ('train', 'eval'),
            (train, eval),
    ):
        out_ast = f'../res/created/parsed/python_small_{split_name}.json'
        with open(out_ast, 'w') as f:
            for example in split:
                try:
                    progress_bar_split.update(n=1)
                    f.write(example[0] + '\n')
                    f.write(example[1] + '\n')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass


if __name__ == '__main__':
    main()
