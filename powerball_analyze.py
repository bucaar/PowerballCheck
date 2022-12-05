
from io import TextIOWrapper
from pprint import pprint
from itertools import combinations

def main():
    history = load_history("history.txt")

    powerball_freq = {}
    for draw in history:
        powerball = draw[6]
        if (powerball,) not in powerball_freq:
            powerball_freq[(powerball,)] = 0

        powerball_freq[(powerball,)] += 1

    powerball_freqs = sort_freq(powerball_freq)
    with open("powerball_freq.txt", "w") as f:
        writelines(powerball_freqs, f)

    for k in range(1, 6):
        number_freq = {}
        number_powerball_freq = {}

        for draw in history:
            numbers = draw[1:6]
            powerball = draw[6]

            subsets = combinations(numbers, k)
            
            for subset in subsets:
                if subset not in number_freq:
                    number_freq[subset] = 0

                number_freq[subset] += 1

                subset_with_powerball = subset + (powerball,)
                if subset_with_powerball not in number_powerball_freq:
                    number_powerball_freq[subset_with_powerball] = 0

                number_powerball_freq[subset_with_powerball] += 1

        number_freqs = sort_freq(number_freq)
        number_powerball_freqs = sort_freq(number_powerball_freq)

        with open("number_freq_%d.txt" % k, "w") as f:
            writelines(number_freqs, f)
            
        with open("number_powerball_freq_%d.txt" % k, "w") as f:
            writelines(number_powerball_freqs, f)

def load_history(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    history = []
    for line in lines:
        date, n1, n2, n3, n4, n5, pb, m, a = line.split("\t")
        n1, n2, n3, n4, n5, pb = [int(x) for x in [n1, n2, n3, n4, n5, pb]]
        history.append([date, n1, n2, n3, n4, n5, pb, m, a])

    return history

def sort_freq(freq: dict):
    # items = list()
    return sorted(freq.items(), key=sorter)

def sorter(items: tuple[tuple, int]):
    # return (6 - len(items[0])) * 1000 + items[1]
    return (-1 * items[1],) + items[0]

def writelines(freqs, file: TextIOWrapper):
    file.writelines(["%s: %d\n" % (" ".join([("%2d" % x) for x in freq]), count) for freq, count in freqs])

if __name__ == "__main__":
    main()