import os
import matplotlib.pyplot as plt
from Spectral_peak_method import Spectral_peak_method
from scipy.signal import filtfilt, butter

class Extract_data:
    def __init__(self, folder_path, starting_wavelength = 600, ending_wavelength = 1200):
        self.folder_path = folder_path
        self.starting_wavelength = starting_wavelength
        self.ending_wavelength = ending_wavelength

    def extract_data(self, separator = None):
        self.spectral_data = {}

        # find where the data starts and check the separator
        file = os.listdir(self.folder_path)[0]
        with open(os.path.join(self.folder_path, file), 'r') as file:
            lines = file.readlines()

            for line_idx in range(len(lines)):
                if lines[line_idx][0].isdigit():
                    start_data_idx = line_idx
                    if ";" in lines[line_idx]:
                        separator = ";"
                    elif "	" in lines[line_idx]:
                        separator = "	"
                    elif "," in lines[line_idx]:
                        separator = ","
                    elif ":" in lines[line_idx]:
                        separator = ":"
                    break


        #populate the dictionary with the wavelength keys and empty lists as values
        file = os.listdir(self.folder_path)[0]
        with open(os.path.join(self.folder_path, file), 'r') as file:
            lines = file.readlines()

            for line in lines[start_data_idx:]:
                wavelength, intensity = map(float, line.split(separator))
                if float(wavelength) >= self.starting_wavelength and float(wavelength) <= self.ending_wavelength:
                    self.spectral_data[wavelength] = []

        #populate the lists with the intensity values

        for file in os.listdir(self.folder_path):
            if file.endswith(".txt"):
                with open(os.path.join(self.folder_path, file), 'r') as file:
                    lines = file.readlines()

                    for line in lines[start_data_idx:]:
                        wavelength, intensity = map(float, line.split(separator))
                        if float(wavelength) >= self.starting_wavelength and float(wavelength) <= self.ending_wavelength:
                            self.spectral_data[wavelength].append(intensity)

    def get_spectral_data(self):
        return self.spectral_data
    
    def average_data(self):
        for wavelength, intensities in self.spectral_data.items():
            self.spectral_data[wavelength] = sum(intensities)/len(intensities)

    def floor_data(self):
        intensities = self.spectral_data.values()
        min_intensity = min(intensities)
        max_intensity = max(intensities)

        for wavelength, intensity in self.spectral_data.items():
            # subtract the minimum intensity value
            self.spectral_data[wavelength] = intensity - min_intensity
        
        quantile = 4
        multiplier = 2
        threshold_intensity = sorted(list(intensities))[int(len(intensities)/quantile)]

        for wavelength, intensity in self.spectral_data.items():
            if intensity <= threshold_intensity * multiplier:
                # set the intensity to 0 if it is below the threshold
                self.spectral_data[wavelength] = 0

    def normalize_data(self):
        intensities = self.spectral_data.values()
        max_intensity = max(intensities)

        for wavelength, intensity in self.spectral_data.items():
            # normalize the intensity values
            self.spectral_data[wavelength] = (intensity)/max_intensity

    def convert_to_list_of_tuples(self):
        new_list = []
        for key, value in self.spectral_data.items():
            new_list.append((key, value))
        self.spectral_data = new_list

    def filtfilt(self):
        # Apply a filtfilt filter to the spectral data
        # Create a low-pass filter

        b, a = butter(1, 0.1, btype='low', analog=False)

        # Apply the filter

        intensities = [item[1] for item in self.spectral_data]
        filtfilt_intensities = filtfilt(b, a, intensities)
        for idx in range(len(self.spectral_data)):
            self.spectral_data[idx] = (self.spectral_data[idx][0], filtfilt_intensities[idx])


    def plot(self):
        self.normalize_data()
        wavelengths = self.spectral_data.keys()
        intensities = self.spectral_data.values()

        __self__ = Spectral_peak_method(list(zip(wavelengths, intensities)))
        __self__.get_peaks()
        self_lambdas = __self__.get_lambdas()
        self_lambdas_widths = __self__.get_lambdas_widths()

        self.central_wavelength = __self__.get_central_wavelength()

        plt.figure(figsize=(10,5))

        plt.plot(wavelengths, intensities, color = "royalblue", 
                 label=f"{self.folder_path[35:46]} : {self_lambdas[0]} ({round(self_lambdas_widths[0],3)},{round(self_lambdas_widths[1],3)})")
        plt.xlim(int(self_lambdas[0]) - 50,int(self_lambdas[0]) + 51)
        for self_lambda in self_lambdas:
            plt.axvline(self_lambda, color = 'royalblue', linestyle = '-')
            plt.axvline(self_lambdas_widths[0], color = 'royalblue', linestyle = ':')
            plt.axvline(self_lambdas_widths[1], color = 'royalblue', linestyle = ':')
        plt.axvline(self.central_wavelength, color = 'royalblue', linestyle = '-.', label = f"{self.folder_path[35:38]} Central Wavelength: {self.central_wavelength}")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity normalized and averaged")
        plt.title(f"Spectral Data Solo: {self.folder_path[35:]}")
        plt.legend(loc = 'upper right')

        save_directory = r'C:\Users\Tumen\Work\Coding\LED_Calibration_report\solo plots'
        plot_file_name = f"{self.folder_path[35:]}.png"
        plt.savefig(f"{save_directory}/{plot_file_name}")
        print(f"Plot saved at {save_directory}/{plot_file_name}")

        plt.show()

    def compare_plot(self, other):
        self.normalize_data()
        other.normalize_data()

        self_wavelengths = self.spectral_data.keys()
        self_intensities = self.spectral_data.values()
        other_wavelengths = other.spectral_data.keys()
        other_intensities = other.spectral_data.values()

        _self_ = Spectral_peak_method(list(zip(self_wavelengths, self_intensities)))
        _other_ = Spectral_peak_method(list(zip(other_wavelengths, other_intensities)))

        _self_.get_peaks()
        _other_.get_peaks()

        self_lambdas = _self_.get_lambdas()
        other_lambdas = _other_.get_lambdas()

        self_lambdas_widths = _self_.get_lambdas_widths()
        other_lambdas_widths = _other_.get_lambdas_widths()

        self.central_wavelength = _self_.get_central_wavelength()
        other.central_wavelength = _other_.get_central_wavelength()

        self.lambdas_difference = [abs(self_lambda - other_lambda) for self_lambda in self_lambdas for other_lambda in other_lambdas]

        plt.figure(figsize=(10,5))

        plt.plot(self_wavelengths, self_intensities, color = "royalblue", 
                 label=f"{self.folder_path[35:38]} : {self_lambdas[0]} ({round(self_lambdas_widths[0],3)},{round(self_lambdas_widths[1],3)})")
        plt.xlim(int(self_lambdas[0]) - 50,int(self_lambdas[0]) + 51)
        for self_lambda in self_lambdas:
            plt.axvline(self_lambda, color = 'royalblue', linestyle = '-')
            plt.axvline(self_lambdas_widths[0], color = 'royalblue', linestyle = ':')
            plt.axvline(self_lambdas_widths[1], color = 'royalblue', linestyle = ':')
        plt.axvline(self.central_wavelength, color = 'royalblue', linestyle = '-.', label = f"{self.folder_path[35:38]} Central Wavelength: {self.central_wavelength}")

        plt.plot(other_wavelengths, other_intensities, color = "orange",
                 label=f"{other.folder_path[35:38]} : {other_lambdas[0]} ({round(other_lambdas_widths[0],3)},{round(other_lambdas_widths[1],3)})")
        for other_lambda in other_lambdas:
            plt.axvline(other_lambda, color = 'orange', linestyle = '-')
            plt.axvline(other_lambdas_widths[0], color = 'orange', linestyle = ':')
            plt.axvline(other_lambdas_widths[1], color = 'orange', linestyle = ':')
        plt.axvline(other.central_wavelength, color = 'orange', linestyle = '-.', label = f"{other.folder_path[35:38]} Central Wavelength: {other.central_wavelength}")

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity normalized and averaged")
        plt.title(f"Spectral Data Comparison: {self.folder_path[47:]}")
        plt.legend(loc = 'upper right')

        save_directory = r'C:\Users\Tumen\Work\Coding\LED_Calibration_report\compare plots'
        plot_file_name = f"{self.folder_path[47:]}.png"
        plt.savefig(f"{save_directory}/{plot_file_name}")

        plt.show()

    def get_lambdas_difference(self):
        return self.lambdas_difference
    
    def get_central_wavelengths(self, other):
        return self.central_wavelength, other.central_wavelength
    
    def get_central_wavelength(self):
        return self.central_wavelength
    
    def get_raw_spectral_data(self):
        raw_data = self.spectral_data.copy()
        intensities = raw_data.values()
        max_intensity = max(intensities)
        min_intensity = min(intensities)

        for wavelength, intensity in raw_data.items():
            # subtract the minimum intensity value
            raw_data[wavelength] = intensity - min_intensity

        for wavelength, intensity in raw_data.items():
            # normalize the intensity values
            raw_data[wavelength] = (intensity)/(max_intensity - min_intensity)

        
        # convert the dictionary to a list of tuples
        new_raw_data = []
        for key, value in raw_data.items():
            new_raw_data.append((key, value))
        
        return new_raw_data
        