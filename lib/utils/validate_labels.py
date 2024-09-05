import json

def parse_labels(request_method):
    labels = request_method.get("labels")
    if not labels:
        return False
    label_list = []
    for label in json.loads(labels):
        label = label["value"]
        if not label_is_valid(label):
            return False
        label_list.append(label)

    return label_list
    

def label_is_valid(label):
    return label.lower() in ("javascript", "python", "ruby")