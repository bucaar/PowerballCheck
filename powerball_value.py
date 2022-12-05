

payouts = {
    (5, 1): 999999999,
    (5, 0): 1000000,
    (4, 1): 50000,
    (4, 0): 100,
    (3, 1): 100,
    (3, 0): 7,
    (2, 1): 7,
    (2, 0): 0,
    (1, 1): 4,
    (1, 0): 0,
    (0, 1): 4,
    (0, 0): 0
}

def main():
    history = load_history("history.txt")
    process_file("our_numbers.txt", history[:7])

def process_file(filename, history):
    print("Results for %s" % filename)

    numbers = loadfile(filename)

    total_payout = 0
    total_wins = 0
    max_payout = 0

    for number in numbers: 
        payout, wins, max_p = check_number(number, history)
        total_payout += payout
        total_wins += wins
        max_payout = max(max_p, max_payout)

    print()
    print("Payout: $%d, Wins: %d, Largest: $%d" % (total_payout, total_wins, max_payout))

def check_number(number, history):
    number_set = set(number[:-2])
    powerball = set([number[-2]])
    power_play = number[-1] == "Y"

    total_payout = 0
    total_wins = 0
    max_payout = 0

    for hist in history:
        hist_set = set(hist[1:6])
        hist_pb = set([hist[6]])
        hist_mult = int(hist[7][:-1])

        # print()
        # print(number_set, powerball, power_play)
        # print(hist_set, hist_pb, hist_mult)

        intersect_numbers = number_set.intersection(hist_set)
        intersect_powerball = powerball.intersection(hist_pb)
        multiplier = 1 if not power_play else hist_mult

        # print(intersect_numbers, intersect_powerball, multiplier)
        
        white_matches = len(intersect_numbers)
        red_matches = len(intersect_powerball)
        payout = payouts[(white_matches, red_matches)]

        payout_mult = multiplier
        if payout == 1000000 and multiplier > 2:
            payout_mult = 2

        payout *= payout_mult
        total_payout += payout
        total_wins += 1
        max_payout = max(payout, max_payout)
        
        if payout:
            print()
            print("$%d won on %s" % (payout, hist[0]))
            print("  Your pick: %s - %d" % (", ".join([str(x) for x in sorted(number_set)]), list(powerball)[0]))
            print("  Drawing: %s - %d" % (", ".join([str(x) for x in sorted(hist_set)]), list(hist_pb)[0]))
            print("  Matches: %d - %d" % (white_matches, red_matches))
            print("  Multiplier: %sX" % multiplier)
            print("  Powerplay? %s" % ("Yes" if power_play else "No"))

    return total_payout, total_wins, max_payout

def loadfile(filename):
    with open(filename) as f:
        lines = f.readlines()

    numbers = [[int(x) for x in line.split()[:-1]] + [line.split()[-1]] for line in lines]
    return numbers

def load_history(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    history = []
    for line in lines:
        date, n1, n2, n3, n4, n5, pb, m, a = line.split("\t")
        n1, n2, n3, n4, n5, pb = [int(x) for x in [n1, n2, n3, n4, n5, pb]]
        history.append([date, n1, n2, n3, n4, n5, pb, m, a])

    return history

if __name__ == "__main__":
    main()