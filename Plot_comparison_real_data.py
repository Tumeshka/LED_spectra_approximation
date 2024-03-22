import matplotlib.pyplot as plt
import numpy as np

class Plot_comparison_real_data:
    def __init__(self, lib_spectral_data, save_plots, plot_path = None):

        self.number_of_rows = len(lib_spectral_data)//8
        if len(lib_spectral_data)%8 != 0:
            self.number_of_rows += 1
        self.lib_spectral_data = lib_spectral_data
        self.keys = list(lib_spectral_data.keys())

        self.keys_original = [key for key in self.keys if "original" in key]
        self.keys_reconstructed = [key for key in self.keys if "reconstructed" in key]

        self.save_plots = save_plots
        self.plot_path = plot_path

    def plot_spectra(self, title):
        number_of_columns = 4
        fig, axs = plt.subplots(self.number_of_rows, number_of_columns, figsize=(number_of_columns*5, self.number_of_rows*5))
        fig.suptitle(f"Spectra of {title}", y = 1.00)

        for idx, key in enumerate(self.keys_original):
            x = idx//number_of_columns
            y = idx%number_of_columns

            key_reconstructed = self.keys_reconstructed[idx]

            label = key_reconstructed[5:]
            axs[x, y].plot([item[0] for item in self.lib_spectral_data[key_reconstructed]], [item[1] for item in self.lib_spectral_data[key_reconstructed]], label = label)
            label = key[5:]
            axs[x, y].plot([item[0] for item in self.lib_spectral_data[key]], [item[1] for item in self.lib_spectral_data[key]], label = label)

            axs[x, y].set_title(key[:5])
            axs[x, y].set_xlabel('Wavelength (nm)')
            axs[x, y].set_ylabel('Intensity normalized')
            axs[x, y].legend()

        plt.tight_layout()

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Spectra plot " + title + ".png")
        plt.show()

    def plot_cumulative_spectra(self, title):
        number_of_columns = 4

        fig, axs = plt.subplots(self.number_of_rows, number_of_columns, figsize=(number_of_columns*5, self.number_of_rows*5))
        fig.suptitle(f"Spectra of {title}", y = 1.00)

        for idx, key in enumerate(self.keys_original):
            x = idx//number_of_columns
            y = idx%number_of_columns

            key_reconstructed = self.keys_reconstructed[idx]

            label = key_reconstructed[5:]
            sum = np.sum([item[1] for item in self.lib_spectral_data[key_reconstructed]])
            axs[x, y].plot([item[0] for item in self.lib_spectral_data[key_reconstructed]], np.cumsum([item[1]/sum for item in self.lib_spectral_data[key_reconstructed]]), label = label)
            label = key[5:]
            sum = np.sum([item[1] for item in self.lib_spectral_data[key]])
            axs[x, y].plot([item[0] for item in self.lib_spectral_data[key]], np.cumsum([item[1]/sum for item in self.lib_spectral_data[key]]), label = label)

            axs[x, y].set_title(key[:5])
            axs[x, y].set_xlabel('Wavelength (nm)')
            axs[x, y].set_ylabel('Intensity normalized')
            axs[x, y].legend()

        plt.tight_layout()

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Cumulative spectra plot " + title + ".png")
        plt.show()

class Plot_comparison_real_data_inter:

    def __init__(self, lib_spectral_data_p15, lib_spectral_data_p20, lib_central_wavelengths_p15, lib_central_wavelengths_p20, save_plots, plot_path = None):

        self.save_plots = save_plots
        self.plot_path = plot_path

        larger_lib = lib_spectral_data_p15 if len(lib_spectral_data_p15) >= len(lib_spectral_data_p20) else lib_spectral_data_p20
        smaller_lib = lib_spectral_data_p15 if len(lib_spectral_data_p15) < len(lib_spectral_data_p20) else lib_spectral_data_p20

        self.larger_lib_central_wavelengths = lib_central_wavelengths_p15 if len(lib_spectral_data_p15) >= len(lib_spectral_data_p20) else lib_central_wavelengths_p20
        self.smaller_lib_central_wavelengths = lib_central_wavelengths_p15 if len(lib_spectral_data_p15) < len(lib_spectral_data_p20) else lib_central_wavelengths_p20

        self.larger_P = "p15" if len(lib_spectral_data_p15) >= len(lib_spectral_data_p20) else "p20"
        self.smaller_P = "p15" if len(lib_spectral_data_p15) < len(lib_spectral_data_p20) else "p20"

        self.number_of_rows = len(larger_lib)//8
        if len(larger_lib)%8 != 0:
            self.number_of_rows += 1
        self.larger_lib = larger_lib
        self.smaller_lib = smaller_lib

        self.larger_lib_keys = list(larger_lib.keys())
        self.smaller_lib_keys = list(smaller_lib.keys())

        self.larger_lib_keys_original = [key for key in self.larger_lib_keys if "original" in key]
        self.smaller_lib_keys_original = [key for key in self.smaller_lib_keys if "original" in key]

    def plot_spectra(self, title):
        number_of_columns = 4
        fig, axs = plt.subplots(self.number_of_rows, number_of_columns, figsize=(number_of_columns*5, self.number_of_rows*5))
        fig.suptitle(f"Spectra of {title}", y = 1.00)
        colours = ["blue", "orange"]

        for idx, key in enumerate(self.larger_lib_keys_original):
            x = idx//number_of_columns
            y = idx%number_of_columns

            label = self.larger_P
            axs[x, y].plot([item[0] for item in self.larger_lib[key]], [item[1] for item in self.larger_lib[key]], label = label, color = colours[0])
            dominant_wl = list(self.larger_lib_central_wavelengths[key[:5]].keys())[0]
            axs[x, y].axvline(x = dominant_wl, color = colours[0], linestyle = "--", ymax = 1, label = "Dominant wavelength")
            fwhm_left = list(self.larger_lib_central_wavelengths[key[:5]].values())[0][0]
            fwhm_right = list(self.larger_lib_central_wavelengths[key[:5]].values())[0][1]
            axs[x, y].axvline(fwhm_left, color = colours[0], linestyle = ":", ymax = 0.25, label = "FWHM")
            axs[x, y].axvline(fwhm_right, color = colours[0], linestyle = ":", ymax = 0.25)
            axs[x, y].axvline((fwhm_left + fwhm_right)/2, color = colours[0], linestyle = "-", ymax = 0.5, label = "Central wavelength")

            if key in self.smaller_lib_keys_original:
                label = self.smaller_P
                axs[x, y].plot([item[0] for item in self.smaller_lib[key]], [item[1] for item in self.larger_lib[key]], label = label, color = colours[1])
                dominant_wl = list(self.smaller_lib_central_wavelengths[key[:5]].keys())[0]
                axs[x, y].axvline(x = dominant_wl, color = colours[1], linestyle = "--", ymax = 1, label = "Dominant wavelength")
                fwhm_left = list(self.smaller_lib_central_wavelengths[key[:5]].values())[0][0]
                fwhm_right = list(self.smaller_lib_central_wavelengths[key[:5]].values())[0][1]
                axs[x, y].axvline(fwhm_left, color = colours[1], linestyle = ":", ymax = 0.25, label = "FWHM")
                axs[x, y].axvline(fwhm_right, color = colours[1], linestyle = ":", ymax = 0.25)
                axs[x, y].axvline((fwhm_left + fwhm_right)/2, color = colours[1], linestyle = "-", ymax = 0.5, label = "Central wavelength")

            axs[x, y].set_title(key[:5])
            axs[x, y].set_xlabel('Wavelength (nm)')
            axs[x, y].set_ylabel('Intensity normalized')
            axs[x, y].legend()

        plt.tight_layout()

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Spectra plot " + title + ".png")
        plt.show()