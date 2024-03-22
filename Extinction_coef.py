import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Extinction_coef():
    def __init__(self, excoef_path, spectral_data, simple_method = False):
        self.excoef_path = excoef_path
        self.spectral_data = spectral_data
        self.df = pd.read_csv(self.excoef_path)
        self.wavelengths = self.df['WL']
        self.simple_spectral_data = spectral_data
        self.simple_method = simple_method

        # matching the length of the spectral data with the length of the extinction coef data

        # self.spectral_data_401_points = {}

        # for wavelength1 in self.df['WL']:
        #     for wavelength2, intensity in self.spectral_data.items():
        #         if wavelength2 >= wavelength1:
        #             self.spectral_data_401_points[wavelength1] = intensity
        #             break
        
        spectral_data_400_points = []

        for wavelength1 in self.df['WL']:
            for idx in range(len(self.spectral_data)):
                if self.spectral_data[idx][0] >= wavelength1:
                    spectral_data_400_points.append((self.spectral_data[idx][0], self.spectral_data[idx][1]))
                    break
        
        self.spectral_data_400_points = spectral_data_400_points
        
        self.spectral_data = spectral_data_400_points
                    
        # normalizing the integral of the spectral data_401_points 
        
        # integral = sum(self.spectral_data_401_points.values())
        # for wavelength in self.spectral_data_401_points.keys():
        #     self.spectral_data_401_points[wavelength] /= integral

        # flooring the spectral data
        
        # min_intensity = min(self.spectral_data_401_points.values())

        # for wavelength in self.spectral_data_401_points.keys():
        #     self.spectral_data_401_points[wavelength] -= min_intensity

        # Normalizing the integral of the spectral data
        integral = sum([item[1] for item in self.spectral_data])

        for idx in range(len(self.spectral_data)):
            self.spectral_data[idx] = (self.spectral_data[idx][0], self.spectral_data[idx][1]/integral)

        simple_integral = sum([item[1] for item in self.simple_spectral_data])

        for idx in range(len(self.simple_spectral_data)):
            self.simple_spectral_data[idx] = (self.simple_spectral_data[idx][0], self.simple_spectral_data[idx][1]/simple_integral)

    def plot_absorbtion_coef(self):
        colors = ["tomato", "steelblue"]
        color_idx = 0
        for molecule in self.df.columns[1:3]:
            extinction_coef = self.df[molecule]
            plt.plot(self.wavelengths, extinction_coef, label=molecule, color = colors[color_idx])
            color_idx += 1
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Absorbtion coefficients')
        plt.legend()
        plt.show()

    def plot_spectral_data(self, title):
        if not self.simple_method:
            plt.plot([item[0] for item in self.spectral_data], [item[1] for item in self.spectral_data], label = f'Spectral data')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Intensity normalized')
            plt.title('Spectral data unaffected by an absorbtion molecule of ' + title)
            plt.xlim(600,1000)
            plt.show()

        else:
            plt.plot([item[0] for item in self.simple_spectral_data], [item[1] for item in self.simple_spectral_data], label = f'Spectral data')
            plt.xlabel('Wavelength (nm)')
            plt.ylabel('Intensity normalized')
            plt.title('Spectral data unaffected by an absorbtion molecule of ' + title)
            plt.xlim(600,1000)
            plt.show()

    def plot_affected_spectral_data_by_absorbtion(self, title):
        colors = ["tomato", "steelblue"]
        color_idx = 0

        if self.simple_method == False:
            for molecule in self.df.columns[1:3]:
                extinction_coef = self.df[molecule]

                self.extinction_coef = extinction_coef

                affected_intensities = [intensity * coef for intensity, coef in zip([item[1] for item in self.spectral_data], extinction_coef)]
                plt.plot([item[0] for item in self.spectral_data], affected_intensities, label=molecule, color = colors[color_idx])
                color_idx += 1

        elif self.simple_method == True:
            for molecule in self.df.columns[1:3]:

                extinction_coef = []
                lib_extinction_coef = []

                for idx in range(len(self.simple_spectral_data)):
                    for idx2 in range(len(self.df['WL'])):
                        if self.simple_spectral_data[idx][0] >= self.df['WL'][idx2] and \
                        self.simple_spectral_data[idx][0] <= self.df['WL'][idx2] + 1:
                            extinction_coef.append(self.df[molecule][idx2])
                            lib_extinction_coef.append((self.simple_spectral_data[idx][0], self.df[molecule][idx2]))
                            break

                # dirty dirty fix (don't do this at home kids)
                extinction_coef.append(0)
                lib_extinction_coef.append((self.simple_spectral_data[-1][0], 0))
                # dirty dirty fix (don't do this at home kids)

                affected_intensities = [intensity * coef for intensity, coef in zip([item[1] for item in self.simple_spectral_data], extinction_coef)]
                plt.plot([item[0] for item in lib_extinction_coef], affected_intensities, label=molecule, color = colors[color_idx])
                color_idx += 1

        plt.title(f'Spectral data affected by an absorbtion molecules of {title}')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Affected intensity')
        plt.xlim(600,1000)
        plt.legend()
        plt.show()

    def get_extinction_coef(self):
        ext_coef = {}
        if self.simple_method == False:
            for molecule in self.df.columns[1:3]:
                extinction_coef = self.df[molecule]
                affected_intensities = [intensity * coef for intensity, coef in zip([item[1] for item in self.spectral_data], extinction_coef)]
                ext_coef[molecule] = sum(affected_intensities)

                self.affected_intensities = affected_intensities
                self.absorption_coef = extinction_coef

        elif self.simple_method == True:
            for molecule in self.df.columns[1:3]:

                extinction_coef = []
                lib_extinction_coef = []

                for idx in range(len(self.simple_spectral_data)):
                    for idx2 in range(len(self.df['WL'])):
                        if self.simple_spectral_data[idx][0] >= self.df['WL'][idx2] and \
                        self.simple_spectral_data[idx][0] <= self.df['WL'][idx2] + 1:
                            extinction_coef.append(self.df[molecule][idx2])
                            lib_extinction_coef.append((self.simple_spectral_data[idx][0], self.df[molecule][idx2]))
                            break

                # dirty dirty fix (don't do this at home kids)
                extinction_coef.append(0)
                lib_extinction_coef.append((self.simple_spectral_data[-1][0], 0))
                # dirty dirty fix (don't do this at home kids)

                affected_intensities = [intensity * coef for intensity, coef in zip([item[1] for item in self.simple_spectral_data], extinction_coef)]
                ext_coef[molecule] = sum(affected_intensities)

                self.affected_intensities = affected_intensities
                self.absorption_coef = extinction_coef

        return ext_coef
    
    def get_spectral_data(self):
        return self.spectral_data
    
    def get_spectral_data_400_points(self):
        return self.spectral_data_400_points 
    
    def get_affected_intensities(self):
        return self.affected_intensities
    
    def get_absorption_coef(self):
        return self.absorption_coef
