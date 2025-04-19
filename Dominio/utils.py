def format_number(value):
    """
    Formatea un número con separadores de miles y dos decimales.
    """
    try:
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")  # Formato europeo
    except (ValueError, TypeError):
        return value