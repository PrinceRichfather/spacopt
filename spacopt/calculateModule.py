import pandas as pd
import numpy as np

##############
# ATTRIBUTES #
##############

# Absorber sizes mm
X = 121.00
Y = 121.00


# Densities g/cm^3
dens_fib = 1.05
dens_air = 0.001225
dens_arm = 7.9


# Absorber Parameters
#                    lead   antimony  tin
#                      Pb      Sb     Sn
densities =         [11.34]#,  6.697, 5.75]       # g/cm^3
mass_fraction =     [0.84] #,   0.12,  0.04]       # sum = 1
rad_lengths =       [6.37] #,   8.73,  8.82]       # g/cm^2
moliere_radii =     [18.18]#, 15.81, 15.77]       # g/cm^2

# Radiation Lengths Fibre and Air, g/cm^2
X0_fib = 43.79
X0_air = 36.62

# Moliere Radii of Fibre (Polystyrene and Air, g/cm^2
Rm_fib = 9.97
Rm_air = 8.83

def calculateModule(                    
                    wall                =0.55,              
                    air_radius          =0.1,                
                    fiber_diameter      =2.0,                
                    seed                =42, 
                    absorber_material   =3,                 
                    Z                   =1,                 
                    energy              =1
                    ):
    """

    Parameters
    ----------
    wall :
        (Default value = 0.55)
    air_radius :
         (Default value = 0.1)
    fiber_diameter :
         (Default value = 2.0)
    seed :
         (Default value = 42)
    Z :
         (Default value = 1)
    energy :
         (Default value = 1)

    Returns
    -------

    
    """




        # # Armour inner diam
        # arm_in_diam = fiber_diameter + (air_radius * 2)

        # # Armour outer diam
        # arm_out_diam = arm_in_diam + (armour_thickness * 2)

#######################################################################################################################

    ####################
    # NUMBER OF FIBRES #
    ####################

    # Rounding precision according to wall decimal points
    pitch_precision = len(str(wall))

    # Pitch of the given configuration (distance between two neighbouring fiber centers)
    pitch = round(fiber_diameter + wall + (air_radius * 2), pitch_precision)

    # Hole for the fiber (Fiber diameter + Air layer*2)
    hole_size = round(fiber_diameter + (air_radius * 2), pitch_precision)
 
    # Number of Fibres per axis
    fibres_per_axis = np.ceil(((X - fiber_diameter) / pitch))
 
    # Number of Fibres per Module (w/o staggering!)
    fibers_per_module = fibres_per_axis * fibres_per_axis # Only if we don't use staggering!
 

#######################################################################################################################
 
    ###################
    # VOLUMES SECTION #
    ###################
 
    # Full Module volume cm^3
    full_vol = (X * Y * Z)/1000
 
    # Volume of all Fibres w/o staggering cm^3
    fiber_round_volume = (np.pi * ((fiber_diameter/2)**2) * Z * fibers_per_module)/1000
 
    # Volume of all Air+Fibres w/o staggering cm^3
    air_fiber_round_volume = (np.pi * (((fiber_diameter / 2) + air_radius) ** 2) * Z * fibers_per_module) / 1000
 
    # Volume of all Air cm^3
    air_round_volume = air_fiber_round_volume - fiber_round_volume
 
    # Volume of Full Absorber (not Module!) cm^3
    abs_vol = full_vol - air_fiber_round_volume
 
    # Volume per gram Absorber cm^3
    abs_per_gram_vol = np.sum(np.array(mass_fraction) / np.array(densities))
 
#######################################################################################################################
 
    ###########
    # DENSITY #
    ###########
 
    # Absorber density g/cm^3
    dens_abs = 1 / abs_per_gram_vol
 
    # ASK EVGENII! Module density (not per gram, but full module values taken)
    dens_module = (abs_vol * dens_abs + fiber_round_volume * dens_fib + air_round_volume * dens_air) / full_vol
 
 
#######################################################################################################################
 
    ################
    # MASS SECTION #
    ################
 
    # Mass of all Fibres
    mass_fib = fiber_round_volume * dens_fib
 
    # Mass of Air
    mass_air = air_round_volume * dens_air
 
    # Mass of Absorber (not Module!)
    mass_abs = abs_vol / abs_per_gram_vol
 
    # Mass of Full Module
    mass_full = mass_fib + mass_air + mass_abs
 
 
#######################################################################################################################
 
    ##################
    # MASS FRACTIONS #
    ##################
 
    # Mass fraction of Fibers
    mfrac_fib = mass_fib / mass_full
 
    # Mass fraction of Air
    mfrac_air = mass_air / mass_full
 
    # Mass fraction of Absorber
    mfrac_abs = mass_abs / mass_full
 
 
#######################################################################################################################
 
    ######################
    # SAMPLING FRACTIONS #
    ######################
 
    ######## 
    # MASS #
    ########
    
    # Mass Sampling fraction (Should make another version for vector implementation)
    samp_frac_af = mfrac_abs / mfrac_fib
 
    # Mass Sampling fraction (Should make another version for vector implementation)
    samp_frac_fa = mfrac_fib / mfrac_abs
    
    ##########
    # VOLUME #
    ##########
    
    # Volume Sampling fraction (Should make another version for vector implementation)
    vol_samp_frac_af = abs_vol / fiber_round_volume
    
    # Volume Sampling fraction (Should make another version for vector implementation)
    vol_samp_frac_fa = fiber_round_volume / abs_vol
    
 
#######################################################################################################################
 
    #####################
    # RADIATION LENGTHS #
    #####################
 
    # Absorber Radiation Length g/cm^2
    X0_abs = 1 / np.sum(np.array(mass_fraction) / np.array(rad_lengths))
 
    # Module Radiation Length g/cm^2
    X0_module = 1 / ((mfrac_fib / X0_fib) + (mfrac_air / X0_air) + (mfrac_abs / X0_abs))
 
    # Absorber Radiation Length cm
    X0_abs_cm = X0_abs / dens_abs
 
    # Module Radiation Length cm (not per gram, but full module values taken)
    X0_module_cm = X0_module / dens_module
 
    #######################################################################################################################
 
    #################
    # MOLIERE RADII #
    #################
 
    # Absorber Moliere Radius g/cm^2
    Rm_abs = 1/np.sum(np.array(mass_fraction) / np.array(moliere_radii))
 
    # Module Moliere Radius g/cm^2
    Rm_module = 1 / ((mfrac_fib / Rm_fib) + (mfrac_air / Rm_air) + (mfrac_abs / Rm_abs))
 
    # Absorber Moliere Radius cm
    Rm_abs_cm = Rm_abs / dens_abs
 
    # Module Moliere Radius cm (not per gram, but full module values taken)
    Rm_module_cm = Rm_module / dens_module


 
 
#######################################################################################################################
 
    ############################
    # MODULE NEW CONFIGURATION #
    ############################
 
    # Module 7X0 cm
    X0_7 = X0_module_cm * 7
 
    # Module 25X0 cm
    X0_25 = X0_module_cm * 25
 
    # absorber_size_z mm
    absorber_size_z = np.ceil(X0_25)*10


    ###################
    # VOLUMES SECTION #
    ###################

    # Z in mm
    Z = absorber_size_z
 
    # Full Module volume cm^3
    full_vol = (X * Y * Z)/1000
    
    # Volume of ONE Fiber cm^3
    fiber_one_vol = Z * np.pi * (fiber_diameter/2)**2

    # Volume of ALL Fibres w/o staggering cm^3
    fiber_round_volume = (fiber_one_vol* fibers_per_module)/1000
    
    # Volume of ONE Air+Fibers cm^3
    air_fiber_one_vol = Z * np.pi * (air_radius + fiber_diameter/2)**2 

    # Volume of ALL Air+Fibres w/o staggering cm^3
    air_fiber_round_volume = (air_fiber_one_vol * fibers_per_module) / 1000
 
    # Volume of ALL Air cm^3
    air_round_volume = air_fiber_round_volume - fiber_round_volume

    # Second option for ALL Air Volume cm^3
    air_round_second_all = (((np.pi * Z * (fiber_diameter + air_radius*2)**2 - fiber_diameter**2)/4)*fibers_per_module)/1000
    # print(f'air_round_second_all: {air_round_second_all:.2f}')
    # Volume of Full Absorber (not Module!) cm^3
    abs_vol = full_vol - air_fiber_round_volume
 
    # Volume per gram Absorber cm^3
    abs_per_gram_vol = np.sum(np.array(mass_fraction) / np.array(densities))

    

    # # ONE Armour volume cm^3
    # arm_vol_single = ((np.pi * Z * (arm_out_diam**2 - arm_in_diam**2))/4)/1000

    # # ALL Armour volume cm^3
    # arm_vol_all = arm_vol_single * fibers_per_module






    ################
    # MASS SECTION #
    ################
 
    # Mass of all Fibres
    mass_fib = fiber_round_volume * dens_fib
 
    # Mass of Air
    mass_air = air_round_volume * dens_air
 
    # Mass of Absorber (not Module!)
    mass_abs = abs_vol / abs_per_gram_vol

    # Mass of Armour gr
    # mass_arm_full = arm_vol_all * dens_arm
 
    # Mass of Full Module
    # mass_full = mass_fib + mass_air + mass_abs + mass_arm_full
    mass_full = mass_fib + mass_air + mass_abs 



    # print(f"arm_vol_single: {arm_vol_single:.2f} cm^3")
    # print(f"arm_vol_all: {arm_vol_all:.2f} cm^3")
    # print(f"arm_out_diam: {arm_out_diam} mm")
    # print(f"arm_in_diam: {arm_in_diam} mm")
    # print(f"mass_arm_full: {mass_arm_full:.2f} gr")
 


    ##########################
    # VALUES FOR CONFIG FILE #
    ##########################

    # # cell_crystal_size_z = | 0 | 1 |         Cell Size Z (absolute value)
    # cell_crystal_size_z_0 = np.ceil(X0_7*10)
    # cell_crystal_size_z_1 = np.ceil(X0_25)*10 - np.ceil(X0_7*10)
 
    # # cell_pos_z = | 0 | 1 |                  Cell position Z (coordinates)
    # cell_pos_z_0 = -(cell_crystal_size_z_1) / 2
    # cell_pos_z_1 = cell_crystal_size_z_0 / 2
 
    # # cell_separator_position = ...           Cell Separator position (between cells | 0 | 1 |)
    # cell_separator_position = cell_pos_z_0 + cell_crystal_size_z_0/2


    summary_dict = {
                    "X" :                       X,
                    "Y" :                       Y,
                    "Z" :                       Z,
                    "pitch" :                   pitch,
                    "hole_size":                hole_size,
                    'fibres_per_axis':          fibres_per_axis,
                    'fibers_per_module':        fibers_per_module,
                    'full_vol':                 full_vol,
                    'fiber_round_volume':       fiber_round_volume,
                    'air_fiber_round_volume':   air_fiber_round_volume,
                    'air_round_volume':         air_round_volume,
                    'abs_vol':                  abs_vol,
                    'abs_per_gram_vol':         abs_per_gram_vol,
                    'dens_abs':                 dens_abs,
                    'dens_module':              dens_module,
                    'mass_fib':                 mass_fib,
                    'mass_air':                 mass_air,
                    'mass_abs':                 mass_abs,
                    'mass_full':                mass_full,
                    'mfrac_fib':                mfrac_fib,
                    'mfrac_air':                mfrac_air,
                    'mfrac_abs':                mfrac_abs,
                    'samp_frac_af':             samp_frac_af,
                    'samp_frac_fa':             samp_frac_fa,
                    'vol_samp_frac_af':         vol_samp_frac_af,
                    'vol_samp_frac_fa':         vol_samp_frac_fa,
                    'X0_abs':                   X0_abs,
                    'X0_module':                X0_module,
                    'X0_abs_cm':                X0_abs_cm,
                    'X0_module_cm':             X0_module_cm,
                    'Rm_abs':                   Rm_abs,
                    'Rm_module':                Rm_module,
                    'Rm_abs_cm':                Rm_abs_cm,
                    'Rm_module_cm':             Rm_module_cm,
                    'X0_7':                     X0_7,
                    'X0_25':                    X0_25,
                    'absorber_size_z':          absorber_size_z,
                    'absorber_material':        absorber_material,
                    'fiber_diameter':           fiber_diameter,
                    'wall':                     wall}


    summary_df = pd.DataFrame(summary_dict, index=[0])

    return summary_df


# results = calculateModule()
# print(results.T)