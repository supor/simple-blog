
def text(key, default=None, args=None):
    parts = key.split('.')
    if len(parts) == 2:
        name = parts[0]
        key = parts[1]
    if len(parts) == 1:
        name = 'global'
        key = parts.pop(0)

    t = __lines.get(name)
    if t:
        text = t.get(key, default)
        if text and args:
            text = text % args
    else:
        text = default
    return text