import os
from importlib import import_module

import numpy as np

from dltools.detector import ObjectDetector


def main(filename):
    X_train = np.load("./data/train_blends_mini.npy")
    Y_train = np.load("./data/train_target_masks_mini.npy")

    X_test = np.load("./data/train_blends_mini.npy")
    Y_test = np.load("./data/train_target_masks_mini.npy")

    module = os.path.splitext(filename)[0]

    binome, submission = module.split('_')
    print("\n\n\n")
    print(f"Training submission {submission} by {binome}...")
    print("\n\n\n")

    custom_lib = import_module(module)
    model = custom_lib.model()

    obj = ObjectDetector(model)

    print("Training...")
    obj.fit(X_train, Y_train)

    print("Testing...")
    score = obj.predict_score(X_test.squeeze(), Y_test)
    print(f"Score: {score:.2f}")

    if not os.path.exists('results.txt'):
        with open('results.txt', 'w') as f:
            print(f"binome    \tsubmission\tscore", file=f)
            print(f"------    \t----------\t-----", file=f)

    with open('results.txt', 'a') as f:
        print(f"{binome}\t{submission}\t{score:.3f}".format(binome, submission, score), file=f)
    

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    main(filename)
