from .groestl import groestl

def groestl_hash(x):
    """Double groestl512 hash."""
    result = groestl(512).digest(x)
    return groestl(512).digest(result)[:32]
