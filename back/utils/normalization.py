
def normalize_minimize(values):
    min_val = min(values)
    max_val = max(values)
    return [(val - min_val) / (max_val - min_val) for val in values]

def normalize_maximize(values):
    min_val = min(values)
    max_val = max(values)
    return [(max_val - val) / (max_val - min_val) for val in values]
