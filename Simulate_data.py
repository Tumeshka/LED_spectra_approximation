import numpy as np
from scipy.signal import filtfilt, butter
from scipy.stats import johnsonsu
import random

class Simulate_data():

    def __init__(self, peak_type):
        # create a clean simulated data
        self.simulated_data = {}

        single_loc = self.__loc()
        double_loc = self.__loc()
        triple_loc = self.__loc()
        quadruple_loc = self.__loc()

        stats = {"Single peak": {single_loc: self.__scale()},
                 "Double peak": {double_loc:self.__scale(), double_loc + self._separation():self.__scale()},
                 "Triple peak": {triple_loc:self.__scale(), triple_loc + self._separation():self.__scale(), 
                                 triple_loc - self._separation():self.__scale()},
                 "Quadruple peak": {quadruple_loc:self.__scale(), quadruple_loc + self._separation():self.__scale(), 
                                    quadruple_loc - self._separation():self.__scale(), quadruple_loc + self._separation():self.__scale()}}
        
        self.stats = stats[peak_type]

        self.a = random.randint(1, 2)
        self.b = random.randint(1, 5)

        weights = [random.random() for _ in range(len(self.stats))]
        self.weights = [weight/sum(weights) for weight in weights]


    def __scale(self, lower = 10, upper = 40):
        return random.randint(lower, upper)
    
    def __loc(self):
        return random.randint(800, 900)

    def _separation(self):
        return random.randint(25, 75)

    def simulate_data(self, num_points = 500):
        
        wavelengths = np.linspace(600, 1100, num_points + 1)

        for wavelength in wavelengths:
            self.simulated_data[wavelength] = []

        weights_idx = 0
        for mean, std_dev in self.stats.items():
            intensities = johnsonsu.pdf(x = wavelengths, a = self.a, b = self.b, loc = mean, scale = std_dev)
            intensities = [intensity * self.weights[weights_idx] for intensity in intensities]
            weights_idx += 1

            for idx in range(len(wavelengths)):
                self.simulated_data[wavelengths[idx]].append(intensities[idx])

        # add noise to the simulated data (floor, peaks and shifts)
                
        floor = 0.0008

        for wavelength in self.simulated_data:
            self.simulated_data[wavelength] = [intensity + np.random.normal(loc = 0, scale = 0.00005) + floor for intensity in self.simulated_data[wavelength]]
    
    def average_data(self):
        for wavelength, intensities in self.simulated_data.items():
            self.simulated_data[wavelength] = sum(intensities)/len(intensities)

    def hard_floor_data(self):
        intensities = self.simulated_data.values()
        min_intensity = min(intensities)

        for wavelength, intensity in self.simulated_data.items():
            # subtract the minimum intensity value
            self.simulated_data[wavelength] = intensity - min_intensity
        
        quantile = 4
        multiplier = 2
        threshold_intensity = sorted(list(intensities))[int(len(intensities)/quantile)]

        for wavelength, intensity in self.simulated_data.items():
            if intensity <= threshold_intensity * multiplier:
                # set the intensity to 0 if it is below the threshold
                self.simulated_data[wavelength] = 0

    def soft_floor_data(self):
        intensities = self.simulated_data.values()
        min_intensity = min(intensities)

        for wavelength, intensity in self.simulated_data.items():
            # subtract the minimum intensity value
            self.simulated_data[wavelength] = intensity - min_intensity
    

    def normalize_data(self):
        intensities = self.simulated_data.values()
        max_intensity = max(intensities)

        for wavelength, intensity in self.simulated_data.items():
            # normalize the intensity values
            self.simulated_data[wavelength] = (intensity)/max_intensity

    def convert_to_list_of_tuples(self):
        new_list = []
        for key, value in self.simulated_data.items():
            new_list.append((key, value))
        self.simulated_data = new_list

    def filtfilt(self):
        # Apply a filtfilt filt for the spectral data
        # Create a low-pass filter

        b, a = butter(1, 0.1, btype='low', analog=False)

        # Apply the filter

        intensities = [item[1] for item in self.simulated_data.copy()]
        filtfilt_intensities = filtfilt(b, a, intensities)
        max_filtfilt_intensity = max(filtfilt_intensities)
        for idx in range(len(self.simulated_data)):
            self.simulated_data[idx] = (self.simulated_data[idx][0], filtfilt_intensities[idx]/max_filtfilt_intensity)

    def get_simulated_data(self):
        return self.simulated_data
    
    def get_raw_simulated_data(self):
        raw_simulated_data = self.simulated_data.copy()
        intensities = raw_simulated_data.values()
        max_intensity = max(intensities)
        min_intensity = min(intensities)

        for wavelength, intensity in raw_simulated_data.items():
            # subtract the minimum intensity value
            raw_simulated_data[wavelength] = intensity - min_intensity

        for wavelength, intensity in raw_simulated_data.items():
            # normalize the intensity values
            raw_simulated_data[wavelength] = (intensity)/(max_intensity - min_intensity)

        
        # convert the dictionary to a list of tuples
        new_raw_simulated_data = []
        for key, value in raw_simulated_data.items():
            new_raw_simulated_data.append((key, value))
        
        return new_raw_simulated_data