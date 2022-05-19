import subprocess
import pandas as pd
import numpy as np
import ROOT
import root_numpy as rn
import time
from array import array
from .calculateModule import calculateModule
import concurrent
from tqdm import tqdm
import os

class Simulation:
    """ """

    def __init__(self, wall, fiber_diameter, events, delete_cfg=False, delete_root=False) -> None:
        
        
        self.delete_cfg = delete_cfg
        self.delete_root = delete_root

        self.wall = wall
        self.fiber_diameter = fiber_diameter
        self.events = events

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

    def runGeant4(self, cfg_file: str, events: int, energy: int) -> str:
        """

        Parameters
        ----------
        cfg_file: str :
            
        events: int :
            
        energy: int :
            

        Returns
        -------

        """

        config_file = f'python_scripts/data/my_configs/{cfg_file}.cfg'
        output_file = f'python_scripts/data/my_root_outputs/{cfg_file}_{energy}_{events}'
        gps_file = f'python_scripts/data/my_gps/{energy}_GeV_my_gps.mac'

        subprocess.call(['./build/FibresCalo', config_file, output_file , gps_file], 
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
        

        return f'{output_file}.root'

    def energyResolution(self, myFile: str, energy: int):
        """Energy resolution in module per energy
        myFile:  - path/to/.root
        energy:  - energy of incident particles (found in .mac file in my_gps folder)

        Parameters
        ----------
        myFile: str :
            
        energy: int :
            

        Returns
        -------
        type
            - each_event_energy: pandas DataFrame with calibrated and not calibrated energy per event

        """
        

        # File Object. Reading root file as variable. File Object
        rootFile = ROOT.TFile.Open(myFile)

        # Getting access to the "shower" branch
        rootTree = rootFile.Get("shower")

        # Turning rootTree into Numpy Array using root_numpy function
        numpyArray = rn.tree2array(rootTree, branches=["totalEnDep", "event"], selection=f'isInCrystal==1')

        # Turning structured ndarray into DataFrame 
        df = pd.DataFrame.from_records(numpyArray)

        # Number of events (кол-во первичных частиц, задается в gps)
        events_number = df['event'].nunique()

        # DataFrame with energy per event (energy left in fibers by incident particle)
        each_event_energy = pd.pivot_table(df, 
                                            values=['totalEnDep'], 
                                            index=['event'],
                                            aggfunc={'totalEnDep': lambda x: np.sum(x)/events_number})

        # Calibrating coefficient
        calib_coeff = (energy / each_event_energy.totalEnDep).sum()/events_number

        # Adding new column with calibrated energy in fibers
        each_event_energy['calibrated'] = calib_coeff * each_event_energy.totalEnDep

        # RMS and MEAN of calibrated energy
        rms_ = each_event_energy.calibrated.std()
        mean_ = each_event_energy.calibrated.mean()

        # Energy resolution during given energy [%]
        energy_resolution = (rms_/mean_).round(5) * 100

        return energy_resolution, each_event_energy

    def delRootFile(self, root_path: str) -> int:
        """

        Parameters
        ----------
        root_path: str :
            

        Returns
        -------

        """

        if os.path.exists(root_path):
            os.remove(root_path)
            return 0
        else:
            return 0

    def delcfg(self, cfg_path: str) -> int:
        """

        Parameters
        ----------
        cfg_path: str :
            

        Returns
        -------

        """


        if os.path.exists(cfg_path):
            os.remove(cfg_path)
            return 0
        else:
            return 0

    def runEnergyResolution(self,
                            energy: int,            # Energy of primary particles per run
                            ):

        """

        Parameters
        ----------
        wall: float :
            
        # Absorber wall between holesfiber_diameter: float :
            
        # Fiber diameterenergy: int :
            
        # Energy of primary particles per runevents: int             # Number of primary particles per run :
            

        Returns
        -------

        """


        print()
        print(f'STARTING PIPELINE ### Energy: {energy} GeV ### Events: {self.events}')
        # print('-----------------------------------------------------------------')
        # print(f"Energy: {energy} GeV")
        # print(f"Events: {self.events}")
        time.sleep(2)

        # print("calculating module parameters")
        module_params_df = calculateModule(wall=self.wall, fiber_diameter=self.fiber_diameter)

        # print("writing to .cfg file")
        cfg_file = self.configWriter(df=module_params_df)

        # print("writing to .mac file")
        self.macWriter(energy = energy, events = self.events)

        # print('starting simulation')
        root_path = self.runGeant4(cfg_file=cfg_file,events=self.events, energy=energy)
        # print("simulation finished (going to sleep for 1 sec.)")
        time.sleep(1)
        
        # print('calculating energy resolution')
        energy_resolution, _df = self.energyResolution(myFile=root_path, energy=energy)
        # print(f'energy resolution finished: {energy_resolution} (going to sleep for 1 sec.)')
        time.sleep(1)
        if self.delete_root == True:
            self.delRootFile(root_path)
            # print('.root deleted')
        if self.delete_cfg == True:
            self.delcfg(cfg_file)
            # print('.cfg deleted')

        # print('-----------------------------------------------------------------')
        # print('FINISHING PIPELINE')
        # print()
        time.sleep(1)
        
        # Subject to minimize
        return energy_resolution

    def fitROOT(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """

        Parameters
        ----------
        dataframe: pd.DataFrame :
            

        Returns
        -------

        """

        energy_resol = dataframe.copy()

        points_number = energy_resol.energy.shape[0]
        energies = array('d', energy_resol.energy)
        resolutions = array('d', energy_resol.energy_resolution)

        gr = ROOT.TGraph(points_number, energies, resolutions)

        myfit = ROOT.TF1("myfit", "sqrt([0]*[0]/x + [1]*[1])")
        myfit.SetParName(0, "Sampling term")
        myfit.SetParName(1, "Constant term")

        gr.Fit(myfit)
        f = gr.GetFunction('myfit')
        samp_term, const_term = f.GetParameter('Sampling term'), f.GetParameter('Constant term')
        samp_term_err, const_term_err = f.GetParError(0), f.GetParError(1)
        ndf,chi2,prob = f.GetNDF(),f.GetChisquare(),f.GetProb()


        outputs = [samp_term, samp_term_err, const_term, const_term_err, ndf, chi2, prob]
        column_df = pd.DataFrame(outputs)
        column_names = ('samp_term', "samp_term_err", 'const_term', 'const_term_err', 'ndf', 'chi2', 'prob')
        results_df = column_df.T
        results_df.columns = column_names
        
        return  results_df

    def runFitting(self, 
                    wall=0.55, 
                    fiber_diameter=2.0, 
                    energies=1, 
                    events=1) -> pd.DataFrame:
        """

        Parameters
        ----------
        wall :
             (Default value = 0.55)
        fiber_diameter :
             (Default value = 2.0)
        energies :
             (Default value = 1)
        events :
             (Default value = 1)

        Returns
        -------

        """
        
        energy_resol = {'energy':[],
                        'energy_resolution':[]}
        for energy in energies:

            er = self.runEnergyResolution(wall            = wall, 
                                          fiber_diameter  = fiber_diameter, 
                                          energy          = energy, 
                                          events          = events)

            energy_resol['energy_resolution'].append(er)
            energy_resol['energy'].append(energy)

        energyResolutions_df = pd.DataFrame(energy_resol)
        fit_df = self.fitROOT(energyResolutions_df)
        
        return fit_df

    def MultiFittingMultProc(self, energies):
        
        energy_resol = {'energy':[],
                    'energy_resolution':[]}

        with concurrent.futures.ProcessPoolExecutor() as executor:
            
            results =list(tqdm(executor.map(self.runEnergyResolution, energies),
                                total=len(energies)))
            print("Pipeline Finished!")

        energy_resol['energy_resolution'] = results
        energy_resol['energy'] = energies

        energyResolutions_df = pd.DataFrame(energy_resol)

        fit_df = self.fitROOT(energyResolutions_df)
        
        return fit_df
        