def format_currency(amount):
    """Format a number as Indian Rupee currency string."""
    return f"₹{amount:,.0f}"


def truncate_text(text, max_length=200):
    """Truncate long text with ellipsis."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def safe_get(data, key, default="N/A"):
    """Safely get a value from a dict, returning default if missing."""
    try:
        return data[key] if data and key in data else default
    except Exception:
        return default
