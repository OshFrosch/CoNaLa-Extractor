import jsonlines
import json
from tqdm import tqdm
from sklearn import model_selection as sklearn_model_selection
from src.ast_parsing.parse_python import parse_code_string
from src.ast_parsing.clean_intent import clean_intent
from src.helper.file_len import file_len
from src.helper.collect_asts import collect_asts

dataset = "../res/dataset/conala-corpus/conala-mined.jsonl"
output_target = "../res/created/parsed/python_small_target.json"
output_train = "../res/created/parsed/python_small.json"
create_ast = False
valid_p = 0.2


def main():
    total_lines = file_len(dataset)

    if create_ast:

        progress_bar_parse = tqdm(total=total_lines, desc="Parsing Python snippets")

        with open(output_train, "w") as outfile_train:

            with open(output_target, "w") as outfile_target:

                with jsonlines.open(dataset) as infile:

                    for line in infile.iter():
                        progress_bar_parse.update(n=1)
                        snippet = line['snippet']
                        intent = line['intent']
                        try:
                            cleaned_intent = clean_intent(intent)
                            ast_line = parse_code_string(snippet)
                        except (AttributeError, TypeError, SyntaxError) as e:
                            pass
                        try:
                            outfile_train.write(ast_line + '\n')
                            outfile_target.write(cleaned_intent + '\n')
                        except (UnicodeEncodeError, UnicodeDecodeError) as e:
                            pass

                infile.close()

            outfile_train.close()

        outfile_target.close()

    # train/eval split

    python_small = collect_asts(output_train)

    train, eval = sklearn_model_selection.train_test_split(
        python_small,
        test_size=valid_p,
    )

    progress_bar_split = tqdm(total=total_lines, desc="Creating train/eval")

    for split_name, split in zip(
            ('train', 'eval'),
            (train, eval),
    ):
        out = f'../res/created/parsed/python_small_{split_name}.json'
        with open(out, 'w') as f:
            for line in split:
                progress_bar_split.update(n=1)
                f.write(json.dumps(line) + '\n')


if __name__ == '__main__':
    main()
