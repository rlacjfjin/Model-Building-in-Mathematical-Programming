input = ['staff', 'showRoom', 'Population1', 'Population2', 'alphaEnquiries', 'betaEnquiries']
output = ['alphaSales', 'BetaSales', 'profit']

dmus = ['Winchester', 'Andover', 'Basingstoke', 'Poole', 'Woking', 'Newbury', 'Portsmouth', 'Alresford',
            'Salisbury', 'Guildford', 'Alton', 'Weybridge', 'Dorchester', 'Bridport', 'Weymouth', 'Portland',
            'Chichester', 'Petersfield', 'Petworth', 'Midhurst', 'Reading', 'Southampton', 'Bournemouth', 'Henley',
            'Maidenhead', 'Fareham', 'Romsey', 'Ringwood']


invalue = {
    'Winchester':{'staff': 7, 'showRoom': 8, 'Population1': 10, 'Population2': 12, 'alphaEnquiries': 8.5, 'betaEnquiries': 4},
    'Andover': {'staff': 6, 'showRoom': 6, 'Population1': 20, 'Population2': 30, 'alphaEnquiries': 9, 'betaEnquiries': 4.5},
    'Basingstoke': {'staff': 2, 'showRoom': 3, 'Population1': 40, 'Population2': 40, 'alphaEnquiries': 2, 'betaEnquiries': 1.5},
    'Poole':
        {'staff': 14, 'showRoom': 9, 'Population1': 20, 'Population2': 25, 'alphaEnquiries': 10, 'betaEnquiries': 6},
    'Woking':
        {'staff': 10, 'showRoom': 9, 'Population1': 10, 'Population2': 10, 'alphaEnquiries': 11, 'betaEnquiries': 5},
    'Newbury':
        {'staff': 24, 'showRoom': 15, 'Population1': 15, 'Population2': 13, 'alphaEnquiries': 25, 'betaEnquiries': 1.9},
    'Portsmouth':
        {'staff': 6, 'showRoom': 7, 'Population1': 50, 'Population2': 40, 'alphaEnquiries': 8.5, 'betaEnquiries': 3},
    'Alresford':
        {'staff': 8, 'showRoom': 7.5, 'Population1': 5, 'Population2': 8, 'alphaEnquiries': 9, 'betaEnquiries': 4},
    'Salisbury':
        {'staff': 5, 'showRoom': 5, 'Population1': 10, 'Population2': 10, 'alphaEnquiries': 5, 'betaEnquiries': 2.5},
    'Guildford':
        {'staff': 8, 'showRoom': 10, 'Population1': 30, 'Population2': 35, 'alphaEnquiries': 9.5, 'betaEnquiries': 4.5},
    'Alton': {'staff': 7, 'showRoom': 8, 'Population1': 7, 'Population2': 8, 'alphaEnquiries': 3, 'betaEnquiries': 2},
    'Weybridge':
        {'staff': 5, 'showRoom': 6.5, 'Population1': 9, 'Population2': 12, 'alphaEnquiries': 8, 'betaEnquiries': 4.5},
    'Dorchester':
        {'staff': 6, 'showRoom': 7.5, 'Population1': 10, 'Population2': 10, 'alphaEnquiries': 7.5, 'betaEnquiries': 4},
    'Bridport':
        {'staff': 11, 'showRoom': 8, 'Population1': 8, 'Population2': 10, 'alphaEnquiries': 10, 'betaEnquiries': 6},
    'Weymouth':
        {'staff': 4, 'showRoom': 5, 'Population1': 10, 'Population2': 10, 'alphaEnquiries': 7.5, 'betaEnquiries': 3.5},
    'Portland':
        {'staff': 3, 'showRoom': 3.5, 'Population1': 3, 'Population2': 20, 'alphaEnquiries': 2, 'betaEnquiries': 1.5},
    'Chichester':
        {'staff': 5, 'showRoom': 5.5, 'Population1': 8, 'Population2': 10, 'alphaEnquiries': 7, 'betaEnquiries': 3.5},
    'Petersfield':
        {'staff': 21, 'showRoom': 12, 'Population1': 6, 'Population2': 6, 'alphaEnquiries': 15, 'betaEnquiries': 8},
    'Petworth':
        {'staff': 6, 'showRoom': 5.5, 'Population1': 2, 'Population2': 2, 'alphaEnquiries': 8, 'betaEnquiries': 5},
    'Midhurst':
        {'staff': 3, 'showRoom': 3.6, 'Population1': 3, 'Population2': 3, 'alphaEnquiries': 2.5, 'betaEnquiries': 1.5},
    'Reading':
        {'staff': 30, 'showRoom': 29, 'Population1': 120, 'Population2': 80, 'alphaEnquiries': 35, 'betaEnquiries': 20},
    'Southampton':
        {'staff': 25, 'showRoom': 16, 'Population1': 110, 'Population2': 80, 'alphaEnquiries': 27, 'betaEnquiries': 12},
    'Bournemouth':
        {'staff': 19, 'showRoom': 10, 'Population1': 90, 'Population2': 22, 'alphaEnquiries': 25, 'betaEnquiries': 13},
    'Henley':
        {'staff': 7, 'showRoom': 6, 'Population1': 5, 'Population2': 7, 'alphaEnquiries': 8.5, 'betaEnquiries': 4.5},
    'Maidenhead':
        {'staff': 12, 'showRoom': 8, 'Population1': 7, 'Population2': 10, 'alphaEnquiries': 12, 'betaEnquiries': 7},
    'Fareham':
        {'staff': 4, 'showRoom': 6, 'Population1': 1, 'Population2': 1, 'alphaEnquiries': 7.5, 'betaEnquiries': 3.5},
    'Romsey':
        {'staff': 2, 'showRoom': 2.5, 'Population1': 1, 'Population2': 1, 'alphaEnquiries': 2.5, 'betaEnquiries': 1},
    'Ringwood':
        {'staff': 2, 'showRoom': 3.5, 'Population1': 2, 'Population2': 2, 'alphaEnquiries': 1.9, 'betaEnquiries': 1.2},
}
outvalue = {
    'Winchester':
        {'alphaSales': 2, 'BetaSales': 0.6, 'profit': 1.5},
    'Andover':
        {'alphaSales': 2.3, 'BetaSales': 0.7, 'profit': 1.6},
    'Basingstoke':
        {'alphaSales': 0.8, 'BetaSales': 0.25, 'profit': 0.5},
    'Poole':
        {'alphaSales': 2.6, 'BetaSales': 0.86, 'profit': 1.9},
    'Woking':
        {'alphaSales': 2.4, 'BetaSales': 1, 'profit': 2},
    'Newbury':
        {'alphaSales': 8, 'BetaSales': 2.6, 'profit': 4.5},
    'Portsmouth':
        {'alphaSales': 2.5, 'BetaSales': 0.9, 'profit': 1.6},
    'Alresford':
        {'alphaSales': 2.1, 'BetaSales': 0.85, 'profit': 2},
    'Salisbury':
        {'alphaSales': 2, 'BetaSales': 0.65, 'profit': 0.9},
    'Guildford':
        {'alphaSales': 2.05, 'BetaSales': 0.75, 'profit': 1.7},
    'Alton':
        {'alphaSales': 1.9, 'BetaSales': 0.70, 'profit': 0.5},
    'Weybridge':
        {'alphaSales': 1.8, 'BetaSales': 0.63, 'profit': 1.4},
    'Dorchester':
        {'alphaSales': 1.5, 'BetaSales': 0.45, 'profit': 1.45},
    'Bridport':
        {'alphaSales': 2.2, 'BetaSales': 0.65, 'profit': 2.2},
    'Weymouth':
        {'alphaSales': 1.8, 'BetaSales': 0.62, 'profit': 1.6},
    'Portland':
        {'alphaSales': 0.9, 'BetaSales': 0.35, 'profit': 0.5},
    'Chichester':
        {'alphaSales': 1.2, 'BetaSales': 0.45, 'profit': 1.3},
    'Petersfield':
        {'alphaSales': 6, 'BetaSales': 0.25, 'profit': 2.9},
    'Petworth':
        {'alphaSales': 1.5, 'BetaSales': 0.55, 'profit': 1.55},
    'Midhurst':
        {'alphaSales': 0.8, 'BetaSales': 0.20, 'profit': 0.45},
    'Reading':
        {'alphaSales': 7, 'BetaSales': 2.5, 'profit': 8},
    'Southampton':
        {'alphaSales': 6.5, 'BetaSales': 3.5, 'profit': 5.4},
    'Bournemouth':
        {'alphaSales': 5.5, 'BetaSales': 3.1, 'profit': 4.5},
    'Henley':
        {'alphaSales': 1.2, 'BetaSales': 0.48, 'profit': 2},
    'Maidenhead':
        {'alphaSales': 4.5, 'BetaSales': 2, 'profit': 2.3},
    'Fareham':
        {'alphaSales': 1.1, 'BetaSales': 0.48, 'profit': 1.7},
    'Romsey':
        {'alphaSales': 0.4, 'BetaSales': 0.1, 'profit': 0.55},
    'Ringwood':
        {'alphaSales': 0.3, 'BetaSales': 0.09, 'profit': 0.4}
}

data = dict()
data["input"] = input
data["output"] = output
data["dmus"] = dmus
data["invalue"] = invalue
data["outvalue"] = outvalue