
from itertools import combinations

def main():
    while True:
        numbers = get_numbers(5, 69)
        if not numbers:
            print("Goodbye!")
            return

        powerball = get_numbers(1, 26)
        if not powerball:
            print("Goodbye!")
            return

        check_numbers(numbers, powerball)

def check_numbers(numbers: "tuple[int]", powerball: tuple[int]):
    powerball_number = powerball[0]
    powerball_string = ", ".join([str(x) for x in numbers])
    powerball_powerball_string = "%s - %d" % (powerball_string, powerball_number)

    print("Your powerball numbers: %s" % powerball_powerball_string)

    powerball_freqs = load_freq("powerball_freq.txt")
    powerball_freq = powerball_freqs.get(powerball, 0)
    print("Powerball %d: %d" % (powerball_number, powerball_freq))

    for k in range(1, 6):
        number_freqs = load_freq("number_freq_%d.txt" % k)
        number_powerball_freqs = load_freq("number_powerball_freq_%d.txt" % k)

        print()
        print("K = %d" % k)

        subsets = combinations(numbers, k)
        for subset in subsets:
            numbers_string = ", ".join([str(x) for x in subset])
            numbers_powerball_string = "%s - %d" % (numbers_string, powerball_number)

            number_freq = number_freqs.get(subset, 0)
            print("Numbers %s: %d" % (numbers_string, number_freq))

            subset_with_powerball = subset + powerball
            number_powerball_freq = number_powerball_freqs.get(subset_with_powerball, 0)
            print("Numbers + powerball %s: %d" % (numbers_powerball_string, number_powerball_freq))

def get_numbers(count, max_value):
    while True:
        print("Enter %d numbers" % count)
        value = input(" > ")
        if not value:
            return None

        try:
            numbers = [int(x) for x in value.split()]
        except:
            print("Invalid numbers, please try again")
            continue

        if len(set(numbers)) != len(numbers):
            print("Please do not repeat numbers")
            continue

        if len(numbers) != count:
            print("Please enter %d numbers" % count)
            continue

        if min(numbers) < 1:
            print("Pleases only enter numbers >= 1")
            continue

        if max(numbers) > max_value:
            print("Pleases only enter numbers <= %d" % max_value)
            continue

        return tuple(sorted(numbers))

def load_freq(filename) -> "dict[tuple[int], int]":
    with open(filename) as f:
        lines = f.readlines()

    freq = {}
    for line in lines:
        # 39: 17
        numbers, count = line.split(":")
        numbers = tuple(sorted([int(x) for x in numbers.split()]))
        count = int(count)

        freq[numbers] = count

    return freq

if __name__ == "__main__":
    main()