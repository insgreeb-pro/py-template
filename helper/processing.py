
COMFORT_TYPES = [
    'Tidak Nyaman',
    'Netral',
    'Nyaman'
]

def calculateComfort(output):
    comfort = output['kenyamanan']
    precentage = comfort.count(1) / len(comfort)
    rules = [60, 80]
    for i, rule in enumerate(rules):
        if precentage < rule:
            return '%s (%s)' % (COMFORT_TYPES[i], precentage)
    return '%s (%s)' % (COMFORT_TYPES[-1], precentage)

