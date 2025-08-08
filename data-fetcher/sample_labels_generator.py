labels = {
    23096260: 0,  # Normal block
    23096261: 1,  # Anomalous block
    23096262: 0,
    23096263: 0,
    23096264: 1,  # Anomalous
    23096265: 0,
    23096266: 0,
    23096267: 1,  # Anomalous
    23096268: 0,
    23096269: 0,
    23096270: 1,  # Anomalous
    23096271: 0,
    23096272: 0,
    23096273: 1,  # Anomalous
    23096274: 0,
    23096275: 0,
    23096276: 1,  # Anomalous
    23096277: 0,
    23096278: 0,
    23096279: 0,
}

import json
with open('../data/labels.json', 'w') as f:
    json.dump(labels, f)

print("labels.json saved")
