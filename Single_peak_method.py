from Extract_folder_data import *
from Extinction_coef import *
from Spectral_peak_method import *

class Single_peak_method:
    def __init__(self, P15 = False, P20 = False):
        self.P15 = P15
        self.P20 = P20
        self.absorption_csv_path = r"C:\Users\Tumen\Work\Coding\Recontructed_vs_origianl_extinction_coef\excoef.csv"
        self.absorption_csv_file = pd.read_csv(self.absorption_csv_path)
        self.lib_spectral_data = {}

    def get_extinction_coef(self):
        self.extinction_coefficient_difference = {}
        self.extinction_coefficient_difference_percentage = {}

        for island in [1]:
            for ID in range(1, 7):

                if self.P15:
                    folder_path = r"C:\Users\Tumen\Work\Coding\my_data\P15 (20 mA)\EM{}".format(f"{island}_{ID}")
                elif self.P20:
                    folder_path = r"C:\Users\Tumen\Work\Coding\my_data\P20 (90 mA)\EM{}".format(f"{island}_{ID}")
                else:
                    raise Warning("Please specify the folder path, P15 or P20")

                self.extinction_coefficient_difference[f"EM{island}_{ID}"] = {}
                self.extinction_coefficient_difference_percentage[f"EM{island}_{ID}"] = {}

                try:
                    data = Extract_data(folder_path)

                    data.extract_data()
                    data.average_data()
                    data.floor_data()
                    data.normalize_data()
                    data.convert_to_list_of_tuples()

                    noisy_original_spectral_data = data.get_spectral_data()

                    data.filtfilt()

                    original_spectral_data = data.get_spectral_data()
                    spectra = Spectral_peak_method(original_spectral_data, filtfilt = False)

                    spectra.get_peaks()
                    lambda_peak = spectra.get_lambdas()[0]

                    extinction_class_original = Extinction_coef(self.absorption_csv_path, noisy_original_spectral_data)
                    extinction_coefficients_original = extinction_class_original.get_extinction_coef()

                    idx = 0
                    for wavelength in self.absorption_csv_file["WL"]:
                        idx += 1
                        if wavelength >= lambda_peak:
                            extinction_coefficients_reconstructed = {"O2Hb": self.absorption_csv_file["O2Hb"][idx],
                                                                     "HHb": self.absorption_csv_file["HHb"][idx]}
                            break
                    

                    for molecule in extinction_coefficients_original:
                            self.extinction_coefficient_difference[f"EM{island}_{ID}"][molecule] = abs(extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])
                            self.extinction_coefficient_difference_percentage[f"EM{island}_{ID}"][molecule] = round(abs((extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])/extinction_coefficients_original[molecule]) * 100, 2)
                    
                    self.lib_spectral_data[f"EM{island}_{ID} original"] = noisy_original_spectral_data
                    self.lib_spectral_data[f"EM{island}_{ID} reconstructed"] = [(wavelength, extinction_coefficients_reconstructed["O2Hb"] + extinction_coefficients_reconstructed["HHb"]) for wavelength in [x[0] for x in original_spectral_data]]

                except FileNotFoundError:
                    continue

            return self.extinction_coefficient_difference, self.extinction_coefficient_difference_percentage
        
    def get_lib_spectral_data(self):
        return self.lib_spectral_data