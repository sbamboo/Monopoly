def playsound(filename,player):
    return f"\033[31mError: Not inplometed yet!\033[0m"
    # Imports
    import platform
    # Set platform
    platformv = platform.system()
    # MP3 player
    if player == "mp3":
        if platformv == "Windows":
            # Playfile
            return f"\033[31mError: Platform {platformv} not supported!\033[0m"
        else:
            return f"\033[31mError: Platform {platformv} not supported!\033[0m"
    else:
        return "\033[31mError: Player not found!\033[0m"
