def macWriter(self, energy, events) -> None:
    """

    Parameters
    ----------
    energy :
        
    events :
        

    Returns
    -------

    """

    lines = open(f'python_scripts/data/my_gps/{energy}_GeV_my_gps.mac').read().splitlines()

    lines[19] = f'/run/beamOn {events}'

    # output_name = f'material{abs_material}_dfib{diam}_pitch{pitch}_wall{wall}_seed{seed}'
    open(f'python_scripts/data/my_gps/{energy}_GeV_my_gps.mac', 'w').write('\n'.join(lines))