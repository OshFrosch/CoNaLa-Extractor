import json


def collect_examples(json_file):
    examples = []
    target_line = True
    with open(json_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                if target_line:
                    target = line.strip()
                    target_line = False
                    print(type(target))
                else:
                    ast = json.loads(line.strip())
                    print(type(ast))
                    examples.append([target, ast])
                    target_line = True
            except:
                pass

    return examples