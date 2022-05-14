import pandas as pd

def configWriter(self, df: pd.DataFrame, seed=-1) -> str:         
    """

    Parameters
    ----------
    df: pd.DataFrame :
        
    seed :
            (Default value = -1)

    Returns
    -------
    
    """
        
        
    lines = open('python_scripts/data/my_configs/single_section_canvas.cfg').read().splitlines()
    # Seed
    lines[23] = 'seed = {}'.format(seed)

    # ABSORBER
    lines[305] = 'absorber_size_x   = {}'.format(df.X.to_string(header=False, index=False))
    lines[306] = 'absorber_size_y   = {}'.format(df.Y.to_string(header=False, index=False))
    lines[307] = 'absorber_size_z   = {}'.format(df.absorber_size_z.to_string(header=False, index=False))

    # ABSORBER MATERIAL
    lines[312] = 'absorber_material = {}'.format(df.absorber_material.to_string(header=False, index=False))

    # CELLS
    lines[342] = 'cell_pos_z  = |{}|'.format(0)
    lines[343] = 'cell_x_elements  = |{}|'.format(df.fibres_per_axis.to_string(header=False, index=False))
    lines[344] = 'cell_y_elements  = |{}|'.format(df.fibres_per_axis.to_string(header=False, index=False))
    lines[347] = 'cell_crystal_size_x  = |{}|'.format(df.fiber_diameter.to_string(header=False, index=False))
    lines[348] = 'cell_crystal_size_y  = |{}|'.format(df.fiber_diameter.to_string(header=False, index=False))
    lines[349] = 'cell_crystal_size_z  = |{}|'.format(df.absorber_size_z.to_string(header=False, index=False))
    lines[350] = 'cell_crystal_pitch_x  = |{}|'.format(df.pitch.to_string(header=False, index=False))
    lines[351] = 'cell_crystal_pitch_y  = |{}|'.format(df.pitch.to_string(header=False, index=False))


    abs_material = df.absorber_material.to_string(header=False, index=False)
    diam = df.fiber_diameter.to_string(header=False, index=False)
    pitch = df.pitch.to_string(header=False, index=False)
    wall = df.wall.to_string(header=False, index=False)

    output_name = f'material{abs_material}_dfib{diam}_pitch{pitch}_wall{wall}_seed{seed}'
    open(f"python_scripts/data/my_configs/{output_name}.cfg", 'w').write('\n'.join(lines))

    return output_name