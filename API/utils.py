def chunk_list(lst, chunk_size):
    """
    Generador que divide una lista en bloques de tamanio chunk_size.
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
