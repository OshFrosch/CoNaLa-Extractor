import argparse
import re
import multiprocessing
import itertools
import tqdm
import joblib


METHOD_NAME, NUM = 'METHODNAME', 'NUM'

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', required=True, type=str)
parser.add_argument('--valid_p', type=float, default=0.2)
parser.add_argument('--max_path_length', type=int, default=8)
parser.add_argument('--max_path_width', type=int, default=2)
parser.add_argument('--use_method_name', type=bool, default=True)
parser.add_argument('--use_nums', type=bool, default=True)
parser.add_argument('--output_dir', required=True, type=str)
parser.add_argument('--n_jobs', type=int, default=multiprocessing.cpu_count())
parser.add_argument('--seed', type=int, default=239)

max_path_length = 8
max_path_width = 2
use_method_name = True
use_nums = True
n_jobs = multiprocessing.cpu_count()


def terminals(ast, node_index):
    stack, paths = [], []

    def dfs(v):
        stack.append(v)

        v_node = ast[v]

        if 'value' in v_node:
            if v == node_index:  # Top-level func def node.
                if use_method_name:
                    paths.append((stack.copy(), METHOD_NAME))
            else:
                v_type = v_node['type']

                if v_type.startswith('Name'):
                    paths.append((stack.copy(), v_node['value']))
                elif use_nums and v_type == 'Num':
                    paths.append((stack.copy(), NUM))
                else:
                    pass

        if 'children' in v_node:
            for child in v_node['children']:
                dfs(child)

        stack.pop()

    dfs(node_index)

    return paths


def merge_terminals2_paths(v_path, u_path):
    s, n, m = 0, len(v_path), len(u_path)
    while s < min(n, m) and v_path[s] == u_path[s]:
        s += 1

    prefix = list(reversed(v_path[s:]))
    lca = v_path[s - 1]
    suffix = u_path[s:]

    return prefix, lca, suffix


def raw_tree_paths(ast, node_index):
    tnodes = terminals(ast, node_index)

    tree_paths = []
    for (v_path, v_value), (u_path, u_value) in itertools.combinations(
            iterable=tnodes,
            r=2,
    ):
        prefix, lca, suffix = merge_terminals2_paths(v_path, u_path)
        if (len(prefix) + 1 + len(suffix) <= max_path_length) \
                and (abs(len(prefix) - len(suffix)) <= max_path_width):
            path = prefix + [lca] + suffix
            tree_path = v_value, path, u_value
            tree_paths.append(tree_path)

    return tree_paths


def delim_name(name):
    if name in {METHOD_NAME, NUM}:
        return name

    def camel_case_split(identifier):
        matches = re.finditer(
            '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)',
            identifier,
        )
        return [m.group(0) for m in matches]

    blocks = []
    for underscore_block in name.split('_'):
        blocks.extend(camel_case_split(underscore_block))

    return '|'.join(block.lower() for block in blocks)


def collect_sample(ast, fd_index):
    root = ast[fd_index]
    if root['type'] != 'FunctionDef':
        raise ValueError('Wrong node type.')

    target = root['value']

    tree_paths = raw_tree_paths(ast, fd_index)
    contexts = []
    for tree_path in tree_paths:
        start, connector, finish = tree_path

        start, finish = delim_name(start), delim_name(finish)
        connector = '|'.join(ast[v]['type'] for v in connector)

        context = f'{start},{connector},{finish}'
        contexts.append(context)

    if len(contexts) == 0:
        return None

    target = delim_name(target)
    context = ' '.join(contexts)

    return f'{target} {context}'


def collect_samples(ast):
    samples = []
    for node_index, node in enumerate(ast):
        if node['type'] == 'FunctionDef':
            sample = collect_sample(ast, node_index)
            if sample is not None:
                samples.append(sample)

    return samples


def collect_all_and_save(asts, output_file):
    parallel = joblib.Parallel(n_jobs=n_jobs)
    func = joblib.delayed(collect_samples)

    samples = parallel(func(ast) for ast in tqdm.tqdm(asts))
    samples = list(itertools.chain.from_iterable(samples))

    with open(output_file, 'w') as f:
        for line_index, line in enumerate(samples):
            f.write(line + ('' if line_index == len(samples) - 1 else '\n'))
