def get_db_url() -> str:
    """
    Get the database URL from the system environment variable.
    
    :return: Database URL string.
    """
    db_url = os.getenv('TIP_ICS_POSTGRES_DB_URL')
    if db_url is None:
        raise ValueError("TIP_ICS_POSTGRES_DB_URL environment variable is not set.")
    
    # URL encode username and password
    db_url_parts = db_url.split('@')
    if len(db_url_parts) != 2:
        raise ValueError("Invalid DATABASE_URL format.")
    
    user_info, rest = db_url_parts
    user_info_encoded = quote(user_info, safe=':')
    return f"{user_info_encoded}@{rest}"
