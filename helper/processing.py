
COMFORT_TYPES = [
    'Tidak Nyaman',
    'Netral',
    'Nyaman'
]

def calculateComfort(output):
    status_format = '%s (%.2f %%)'
    comfort = output['kenyamanan']
    total_prediction = len(comfort)
    if total_prediction == 0: # zero output data
        return "Data Kurang"
    precentage = comfort.count(1) / total_prediction
    rules = [60, 80]
    for i, rule in enumerate(rules):
        if precentage < rule:
            return status_format % (COMFORT_TYPES[i], precentage)
    return status_format % (COMFORT_TYPES[-1], precentage)

