import numpy as np
from pathlib import Path
from sklearn import model_selection as sklearn_model_selection
from src.preprocessing.preprocess_python import collect_all_and_save
from src.helper.collect_asts import collect_asts

seed = 239
valid_p = 0.2
in_dir = '/Users/joshuakraft/documents/studium/informatik/[4]-SS-20/MloSc/' \
         'code-captioning-with-conala/res/created/parsed'
out_dir = '/Users/joshuakraft/documents/studium/informatik/[4]-SS-20/MloSc/' \
         'code-captioning-with-conala/res/created/preprocessed'


def main():

    np.random.seed(seed)

    data_dir = Path(in_dir)
    trains = collect_asts(data_dir / 'python_small_train.json')
    evals = collect_asts(data_dir / 'python_small_eval.json')

    train, valid = sklearn_model_selection.train_test_split(
        trains,
        test_size=valid_p,
    )
    test = evals

    output_dir = Path(out_dir)
    output_dir.mkdir(exist_ok=True)
    for split_name, split in zip(
            ('train', 'valid', 'test'),
            (train, valid, test),
    ):
        output_file = output_dir / f'{split_name}_output_file.txt'
        collect_all_and_save(split, output_file)


if __name__ == '__main__':
    main()