def restrict_str(input_str,n):
    m = len(input_str)
    if n > m:
        return input_str
    return input_str[:n] + "..."