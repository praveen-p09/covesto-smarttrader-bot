def human_readable_number(n):
    if n is None:
        return "N/A"
    try:
        n = float(n)
        if n >= 1_000_000_000_000:
            return f"{n / 1_000_000_000_000:.2f}T"
        elif n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.2f}B"
        elif n >= 1_000_000:
            return f"{n / 1_000_000:.2f}M"
        else:
            return f"{n:.0f}"
    except:
        return "N/A"