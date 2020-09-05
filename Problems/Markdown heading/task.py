def heading(string, level=1):
    if level <= 0:
        level = 1
    elif level > 6:
        level = 6

    return f"{'#' * level} {string}"
