import jsonlines
import ast

i = 0

with jsonlines.open('../res/conala-corpus/conala-mined.jsonl') as f:
    for line in f.iter():
        snip = line['snippet']
        node = ast.parse(snip, mode='exec')
        compiled = compile(node, '<sting>', mode='exec')
        print(ast.dump(node))
        print('\n _______________________\n')

        if i == 10:
            break
        i += 1
