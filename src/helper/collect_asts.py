import json

def collect_asts(json_file):
    asts = []
    with open(json_file, 'r', encoding='utf-8') as f:
        for line in f:
            ast = json.loads(line.strip())
            asts.append(ast)

    return asts
