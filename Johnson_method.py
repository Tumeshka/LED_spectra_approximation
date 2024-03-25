from Extract_folder_data import *
from Extinction_coef import *
from Spectral_peak_method import *
from Simulate_data import *
import spectra as sp

# Keep the the spectral data in dictionary format!!!

class Johnson_method:
    def __init__(self, simulation = True, folder_path = None, separator = None, starting_wavelength = 600, ending_wavelength = 1200):
        self.absorption_csv_path = r"excoef.csv"
        self.lib_spectral_data = {}
        self.peak_types = ["Single peak", "Double peak", "Triple peak", "Quadruple peak"]
        self.simulation = simulation
        self.folder_path = folder_path
        self.separator = separator
        self.starting_wavelength = starting_wavelength
        self.ending_wavelength = ending_wavelength
        self.lib_central_wavelengths = {}


    def get_extinction_coef(self):
        self.extinction_coefficient_difference = {}
        self.extinction_coefficient_difference_percentage = {}
        self.lib_param = {}
        self.lib_lambdas = {}
        self.lib_troughs = {}
        self.lib_troughs_limits = {}

        if self.simulation:
            for peak_type in self.peak_types:

                self.extinction_coefficient_difference[peak_type] = {}
                self.extinction_coefficient_difference_percentage[peak_type] = {}
                
                data = Simulate_data(peak_type)

                data.simulate_data()
                data.average_data()

                raw_simulated_data = data.get_raw_simulated_data()

                data.hard_floor_data()
                data.normalize_data()
                data.convert_to_list_of_tuples()

                noisy_simulated_data = data.get_simulated_data()

                data.filtfilt()

                filtfilt_simulated_data = data.get_simulated_data()
                spectra = Spectral_peak_method(filtfilt_simulated_data, filtfilt=False)

                # Find the peaks
                spectra.get_peaks()
                self.lib_lambdas[peak_type] = spectra.get_lambdas()

                # Find the troughs
                self.lib_troughs[peak_type] = spectra.get_troughs()

                # Find the peaks and their troughs
                self.lib_troughs_limits[peak_type] = spectra.get_lib_troughs_limits()

                # Reduce the peak distribution by 1
                # spectra.reduce_by_1_peak()

                # reduce the distribution to its respective peaks and run them through the Johnson method
                lib_deconstruced_peaks = spectra.deconstruct_into_peaks()

                # spectra.plot_data()

                lib_recontructed = {}
                total_reconstructed = [0] * len(spectra.wavelength)

                for distribution in lib_deconstruced_peaks:

                    qnt = spectra.cumulitive_quantile(lib_deconstruced_peaks[distribution])

                    reconstructed, param, _ = sp.johnson(list(qnt.values()), spectra.wavelength)
                    lib_recontructed[distribution] = reconstructed
                    # plt.plot(spectra.wavelength, lib_deconstruced_peaks[distribution],label = distribution)

                    max_intensity_deconstructed = max(lib_deconstruced_peaks[distribution])
                    reconstructed_max_intensity = max(reconstructed)
                    reconstructed = [intensity * (max_intensity_deconstructed/reconstructed_max_intensity) for intensity in reconstructed]
                    # plt.plot(spectra.wavelength, reconstructed, label = f"{distribution} reconstructed")

                    total_reconstructed = [x + y for x, y in zip(reconstructed, total_reconstructed)]

                # plt.title(peak_type)
                # plt.legend()
                # plt.show()

                reconstructed = total_reconstructed
                max_intensity = max(spectra.intensity)
                reconstructed_max_intensity = max(reconstructed)

                reconstructed_normalized = list(zip(spectra.wavelength, 
                                            [intensity * (max_intensity/reconstructed_max_intensity) for intensity in reconstructed]))
                

                self.lib_spectral_data[f"{peak_type} raw simulated"] = raw_simulated_data.copy()
                self.lib_spectral_data[f"{peak_type} simulated"] = noisy_simulated_data.copy()
                self.lib_spectral_data[f"{peak_type} reconstructed"] = reconstructed_normalized.copy()
                self.lib_param[f"{peak_type} reconstructed"] = param

                extinction_class_original = Extinction_coef(self.absorption_csv_path, noisy_simulated_data)
                extinction_class_reconstructed = Extinction_coef(self.absorption_csv_path, reconstructed_normalized)

                extinction_coefficients_original = extinction_class_original.get_extinction_coef()
                extinction_coefficients_reconstructed = extinction_class_reconstructed.get_extinction_coef()

                for molecule in extinction_coefficients_original:
                    self.extinction_coefficient_difference[peak_type][molecule] = abs(extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])
                    self.extinction_coefficient_difference_percentage[peak_type][molecule] = round(abs((extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])/extinction_coefficients_original[molecule]) * 100, 2)

        elif self.simulation == False:
            for island in [1,2,3,4]:
                for ID in range(1, 7):

                    folder_path = r"{}".format(f"{self.folder_path}\EM{island}_{ID}")

                    self.extinction_coefficient_difference[f"EM{island}_{ID}"] = {}
                    self.extinction_coefficient_difference_percentage[f"EM{island}_{ID}"] = {}
                    self.lib_param[f"EM{island}_{ID}"] = {}
                    self.lib_lambdas[f"EM{island}_{ID}"] = {}
                    self.lib_troughs[f"EM{island}_{ID}"] = {}
                    self.lib_troughs_limits[f"EM{island}_{ID}"] = {}

                    try:
                        data = Extract_data(folder_path, self.starting_wavelength, self.ending_wavelength)

                        data.extract_data(self.separator)
                        data.average_data()

                        raw_spectral_data = data.get_raw_spectral_data()

                        data.floor_data()
                        data.normalize_data()
                        data.convert_to_list_of_tuples()

                        noisy_original_spectral_data = data.get_spectral_data()

                        data.filtfilt()

                        original_spectral_data = data.get_spectral_data()
                        spectra = Spectral_peak_method(original_spectral_data, filtfilt = False)

                        # Find the peaks
                        spectra.get_peaks()
                        self.lib_lambdas[f"EM{island}_{ID}"] = spectra.get_lambdas()

                        # Find the troughs
                        self.lib_troughs[f"EM{island}_{ID}"] = spectra.get_troughs()

                        # Find the peaks and their troughs
                        self.lib_troughs_limits[f"EM{island}_{ID}"] = spectra.get_lib_troughs_limits()

                        # reduce the distribution to its respective peaks and run them through the Johnson method
                        lib_deconstruced_peaks = spectra.deconstruct_into_peaks()

                        # get the central wavelength
                        self.lib_central_wavelengths[f"EM{island}_{ID}"] = {}
                        self.lib_central_wavelengths[f"EM{island}_{ID}"][spectra.get_central_wavelength()] = spectra.get_lambdas_widths()

                        lib_recontructed = {}
                        total_reconstructed = [0] * len(spectra.wavelength)

                        for distribution in lib_deconstruced_peaks:

                            qnt = spectra.cumulitive_quantile(lib_deconstruced_peaks[distribution])

                            reconstructed, param, _ = sp.johnson(list(qnt.values()), spectra.wavelength)
                            self.lib_param[f"EM{island}_{ID}"][distribution] = param
                            lib_recontructed[distribution] = reconstructed

                            max_intensity_deconstructed = max(lib_deconstruced_peaks[distribution])
                            reconstructed_max_intensity = max(reconstructed)
                            reconstructed = [intensity * (max_intensity_deconstructed/reconstructed_max_intensity) for intensity in reconstructed]

                            total_reconstructed = [x + y for x, y in zip(reconstructed, total_reconstructed)]
                        
                        reconstructed = total_reconstructed
                        max_intensity = max(spectra.intensity)
                        reconstructed_max_intensity = max(reconstructed)

                        reconstructed_normalized = list(zip(spectra.wavelength, 
                                                    [intensity * (max_intensity/reconstructed_max_intensity) for intensity in reconstructed]))

                        self.lib_spectral_data[f"EM{island}_{ID} reconstructed"] = reconstructed_normalized.copy()
                        self.lib_spectral_data[f"EM{island}_{ID} original"] = raw_spectral_data.copy()
                        # self.lib_spectral_data[f"EM{island}_{ID} original_spectral_data"] = original_spectral_data.copy()
                        self.lib_param[f"EM{island}_{ID} reconstructed"] = param

                        extinction_class_original = Extinction_coef(self.absorption_csv_path, noisy_original_spectral_data)
                        extinction_class_reconstructed = Extinction_coef(self.absorption_csv_path, reconstructed_normalized)

                        extinction_coefficients_original = extinction_class_original.get_extinction_coef()
                        extinction_coefficients_reconstructed = extinction_class_reconstructed.get_extinction_coef()

                        for molecule in extinction_coefficients_original:
                            self.extinction_coefficient_difference[f"EM{island}_{ID}"][molecule] = abs(extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])
                            self.extinction_coefficient_difference_percentage[f"EM{island}_{ID}"][molecule] = round(abs((extinction_coefficients_original[molecule] - extinction_coefficients_reconstructed[molecule])/extinction_coefficients_original[molecule]) * 100, 2)

                    except FileNotFoundError:
                        continue

        return self.extinction_coefficient_difference, self.extinction_coefficient_difference_percentage
    
    def get_lib_spectral_data(self):
        return self.lib_spectral_data
    
    def get_lib_param(self):
        return self.lib_param
    
    def get_lib_lambdas(self):
        return self.lib_lambdas
    
    def get_lib_troughs(self):
        return self.lib_troughs 
    
    def get_lib_troughs_limits(self):
        return self.lib_troughs_limits
    
    def get_lib_central_wavelengths(self):
        return self.lib_central_wavelengths