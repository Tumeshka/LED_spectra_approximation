from Extract_folder_data import *
from Extinction_coef import *
from Spectral_peak_method import *
import spectra as sp
import Wheeler_quantile_johnson_approximation as Wheeler

# Keep the the spectral data in dictionary format!!!

class Johnson_decomposition_method:
    def __init__(self, P15 = False, P20 = False):
        self.absorption_csv_path = r"C:\Users\Tumen\Work\Coding\Recontructed_vs_origianl_extinction_coef\excoef.csv"
        self.P15 = P15
        self.P20 = P20
        self.lib_spectral_data = {}
        self.lib_cumsum_spectral_data = {}

    def get_extinction_coef(self):
        self.extinction_coefficient_difference = {}
        self.extinction_coefficient_difference_percentage = {}
        self.lib_param = {}

        for island in [1]:
            for ID in range(2, 3):

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
                    data.normalize_data()
                    data.convert_to_list_of_tuples()

                    noisy_original_spectral_data = data.get_spectral_data()

                    data.filtfilt()

                    original_spectral_data = data.get_spectral_data()
                    spectra = Spectral_peak_method(original_spectral_data)

                    qnt = spectra.cumulitive_quantile()
                    print(qnt)
                    reconstructed, param, _ = sp.johnson(list(qnt.values()), spectra.wavelength)

                    wavelengths = [x[0] for x in original_spectral_data]
                    intensities = [x[1] for x in original_spectral_data]

                    max_intensity = max(intensities)
                    reconstructed_max_intensity = max(reconstructed)

                    reconstructed_normalized = list(zip(spectra.wavelength, 
                                              [intensity * (max_intensity/reconstructed_max_intensity) for intensity in reconstructed]))
                    
                    reconstructed_normalized_reduced = []
                    
                    for idx in range(len(reconstructed_normalized)):
                            reconstructed_normalized_reduced.append((reconstructed_normalized[idx][0], 
                                                                    original_spectral_data[idx][1] - reconstructed_normalized[idx][1]))
                    
                    shortest_distance_spectra = []

                    for i in range(len(original_spectral_data)):
                        distance = 100
                        for j in range(len(reconstructed_normalized)):
                            
                            if original_spectral_data[i][1] >= reconstructed_normalized[j][1]:
                                new_distance = np.sqrt((original_spectral_data[i][1] - reconstructed_normalized[j][1])**2 \
                                                + (original_spectral_data[i][0]/1112.74 - reconstructed_normalized[j][0]/1112.74)**2)
                            elif original_spectral_data[i][1] < reconstructed_normalized[i][1]:
                                distance = 0
                                break

                            if new_distance < distance:
                                distance = new_distance
                        
                        shortest_distance_spectra.append((original_spectral_data[i][0], distance))

                    extinction_class_original = Extinction_coef(self.absorption_csv_path, noisy_original_spectral_data)
                    extinction_class_reconstructed = Extinction_coef(self.absorption_csv_path, reconstructed_normalized)

                    extinction_coefficients_original = extinction_class_original.get_extinction_coef()
                    extinction_coefficients_reconstructed = extinction_class_reconstructed.get_extinction_coef()

                    for molecule in extinction_coefficients_original:
                        self.extinction_coefficient_difference[f"EM{island}_{ID}"][molecule] = abs(extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])
                        self.extinction_coefficient_difference_percentage[f"EM{island}_{ID}"][molecule] = round(abs((extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])/extinction_coefficients_original[molecule]) * 100, 2)

                    self.lib_spectral_data[f"EM{island}_{ID} original"] = noisy_original_spectral_data
                    self.lib_spectral_data[f"EM{island}_{ID} reconstructed"] = reconstructed_normalized
                    self.lib_spectral_data[f"EM{island}_{ID} reconstructed reduced"] = reconstructed_normalized_reduced
                    self.lib_spectral_data[f"EM{island}_{ID} shortest distance"] = shortest_distance_spectra
                    self.lib_param[f"EM{island}_{ID}"] = param

                    self.lib_cumsum_spectral_data[f"EM{island}_{ID} original"] = [(x, y) for x, y in zip(wavelengths, np.cumsum(intensities)/np.sum(intensities))]
                    self.lib_cumsum_spectral_data[f"EM{island}_{ID} reconstructed"] = [(x, y) for x, y in zip(wavelengths, np.cumsum([x[1] for x in reconstructed_normalized])/np.sum([x[1] for x in reconstructed_normalized]))]
                    self.lib_cumsum_spectral_data[f"EM{island}_{ID} reconstructed reduced"] = [(x, y) for x, y in zip(wavelengths, np.cumsum([x[1] for x in reconstructed_normalized_reduced])/np.sum([x[1] for x in reconstructed_normalized_reduced]))]

                except FileNotFoundError:
                    continue

        return self.extinction_coefficient_difference, self.extinction_coefficient_difference_percentage
    
    def get_lib_spectral_data(self):
        return self.lib_spectral_data
    
    def get_lib_cumsum_spectral_data(self):
        return self.lib_cumsum_spectral_data
    
    def get_lib_param(self):
        return self.lib_param