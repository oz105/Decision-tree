import pandas as pnd

from BruteForceTree import brute_force, calculate_err_brute_force
from EntropyTree import create_entropy, calculate_err_entropy

if __name__ == '__main__':
    vectors = pnd.read_csv('vectors.txt', sep=" ", header=None)
    labels = {}
    vec = {}
    for index in vectors.itertuples():
        temp = {}
        line = vectors.iloc[[index.Index]]
        labels[index.Index] = line.iloc[0][8]
        vec[index.Index] = temp
        for i in range(8):
            vec[index.Index][i] = line.iloc[0][i]

    # 1a
    print("1a:")
    print("Brute Force Tree: \n")
    t = brute_force(3, vec, labels)
    err = calculate_err_brute_force(t, vec, labels, [])
    print("The ERROR is : " + str(1 - (err / 150)))
    print("draw of Tree:")
    t.display()

    # 1b

    print("\n1b:")
    print("Binary Entropy Tree:\n")
    t = create_entropy(3, vec, labels)
    err = calculate_err_entropy(vec, labels, t)
    print("The ERROR is : " + str(err))
    print("draw of Tree:")
    t.display()
