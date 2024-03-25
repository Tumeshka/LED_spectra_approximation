import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class Plot_comparison:
    def __init__(self, lib_spectral_data, save_plots, plot_path = None):
            
        self.Single_peak_raw_simulated = lib_spectral_data["Single peak raw simulated"]
        self.Single_peak_Simulated = lib_spectral_data["Single peak simulated"]
        self.Single_peak_reconstructed = lib_spectral_data["Single peak reconstructed"]

        self.Double_peak_raw_simulated = lib_spectral_data["Double peak raw simulated"]
        self.Double_peak_Simulated = lib_spectral_data["Double peak simulated"]
        self.Double_peak_reconstructed = lib_spectral_data["Double peak reconstructed"]

        self.Triple_peak_raw_simulated = lib_spectral_data["Triple peak raw simulated"]
        self.Triple_peak_Simulated = lib_spectral_data["Triple peak simulated"]
        self.Triple_peak_reconstructed = lib_spectral_data["Triple peak reconstructed"]

        self.Quadruple_peak_raw_simulated = lib_spectral_data["Quadruple peak raw simulated"]
        self.Quadruple_peak_Simulated = lib_spectral_data["Quadruple peak simulated"]
        self.Quadruple_peak_reconstructed = lib_spectral_data["Quadruple peak reconstructed"]

        self.save_plots = save_plots
        self.plot_path = plot_path


    def plot_spectra(self, title, is_streamlit = True):

        fig, axs = plt.subplots(2, 2, figsize=(10, 10))
        fig.suptitle(f"Spectra of {title}")

        axs[0, 0].plot([item[0] for item in self.Single_peak_reconstructed], [item[1] for item in self.Single_peak_reconstructed], label = 'Reconstructed')
        axs[0, 0].plot([item[0] for item in self.Single_peak_raw_simulated], [item[1] for item in self.Single_peak_raw_simulated], label = 'Raw simulated')
        axs[0, 0].plot([item[0] for item in self.Single_peak_Simulated], [item[1] for item in self.Single_peak_Simulated], label = 'Processed simulated')
        axs[0, 0].set_title(f'Single_peak')
        axs[0, 0].set_xlabel('Wavelength (nm)')
        axs[0, 0].set_ylabel('Intensity normalized')
        axs[0, 0].legend()

        axs[0, 1].plot([item[0] for item in self.Double_peak_reconstructed], [item[1] for item in self.Double_peak_reconstructed], label = 'Reconstructed')
        axs[0, 1].plot([item[0] for item in self.Double_peak_raw_simulated], [item[1] for item in self.Double_peak_raw_simulated], label = 'Raw simulated')
        axs[0, 1].plot([item[0] for item in self.Double_peak_Simulated], [item[1] for item in self.Double_peak_Simulated], label = 'Processed simulated')
        axs[0, 1].set_title(f'Double_peak')
        axs[0, 1].set_xlabel('Wavelength (nm)')
        axs[0, 1].set_ylabel('Intensity normalized')
        axs[0, 1].legend()

        axs[1, 0].plot([item[0] for item in self.Triple_peak_reconstructed], [item[1] for item in self.Triple_peak_reconstructed], label = 'Reconstructed')
        axs[1, 0].plot([item[0] for item in self.Triple_peak_raw_simulated], [item[1] for item in self.Triple_peak_raw_simulated], label = 'Raw simulated')
        axs[1, 0].plot([item[0] for item in self.Triple_peak_Simulated], [item[1] for item in self.Triple_peak_Simulated], label = 'Processed simulated')
        axs[1, 0].set_title(f'Triple_peak')
        axs[1, 0].set_xlabel('Wavelength (nm)')
        axs[1, 0].set_ylabel('Intensity normalized')
        axs[1, 0].legend()

        axs[1, 1].plot([item[0] for item in self.Quadruple_peak_reconstructed], [item[1] for item in self.Quadruple_peak_reconstructed], label = 'Reconstructed')
        axs[1, 1].plot([item[0] for item in self.Quadruple_peak_raw_simulated], [item[1] for item in self.Quadruple_peak_raw_simulated], label = 'Raw simulated')
        axs[1, 1].plot([item[0] for item in self.Quadruple_peak_Simulated], [item[1] for item in self.Quadruple_peak_Simulated], label = 'Processed simulated')
        axs[1, 1].set_title(f'Quadruple_peak')
        axs[1, 1].set_xlabel('Wavelength (nm)')
        axs[1, 1].set_ylabel('Intensity normalized')
        axs[1, 1].legend()

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Spectra plot " + title + ".png")

        if not is_streamlit:
            plt.show()
        else:
            st.pyplot(fig)

    def plot_cumulative_spectra(self, title, is_streamlit = True):
        fig, axs = plt.subplots(2, 2, figsize=(10, 10))
        fig.suptitle(f'Cumulative spectra of {title}')

        axs[0, 0].plot([item[0] for item in self.Single_peak_reconstructed], np.cumsum([item[1]/np.sum(item[1] for item in self.Single_peak_reconstructed) for item in self.Single_peak_reconstructed]), label = 'Reconstructed')
        axs[0, 0].plot([item[0] for item in self.Single_peak_raw_simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Single_peak_raw_simulated) for item in self.Single_peak_raw_simulated]), label = 'Raw simulated')
        axs[0, 0].plot([item[0] for item in self.Single_peak_Simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Single_peak_Simulated) for item in self.Single_peak_Simulated]), label = 'Processed simulated')
        axs[0, 0].set_title(f'Single_peak')
        axs[0, 0].set_xlabel('Wavelength (nm)')
        axs[0, 0].set_ylabel('Cumulative Intensity normalized')
        axs[0, 0].legend()

        axs[0, 1].plot([item[0] for item in self.Double_peak_reconstructed], np.cumsum([item[1]/np.sum(item[1] for item in self.Double_peak_reconstructed) for item in self.Double_peak_reconstructed]), label = 'Reconstructed')
        axs[0, 1].plot([item[0] for item in self.Double_peak_raw_simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Double_peak_raw_simulated) for item in self.Double_peak_raw_simulated]), label = 'Raw simulated')
        axs[0, 1].plot([item[0] for item in self.Double_peak_Simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Double_peak_Simulated) for item in self.Double_peak_Simulated]), label = 'Processed simulated')
        axs[0, 1].set_title(f'Double_peak')
        axs[0, 1].set_xlabel('Wavelength (nm)')
        axs[0, 1].set_ylabel('Cumulative Intensity normalized')
        axs[0, 1].legend()

        axs[1, 0].plot([item[0] for item in self.Triple_peak_reconstructed], np.cumsum([item[1]/np.sum(item[1] for item in self.Triple_peak_reconstructed) for item in self.Triple_peak_reconstructed]), label = 'Reconstructed')
        axs[1, 0].plot([item[0] for item in self.Triple_peak_raw_simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Triple_peak_raw_simulated) for item in self.Triple_peak_raw_simulated]), label = 'Raw simulated')
        axs[1, 0].plot([item[0] for item in self.Triple_peak_Simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Triple_peak_Simulated) for item in self.Triple_peak_Simulated]), label = 'Processed simulated')
        axs[1, 0].set_title(f'Triple_peak')
        axs[1, 0].set_xlabel('Wavelength (nm)')
        axs[1, 0].set_ylabel('Cumulative Intensity normalized')
        axs[1, 0].legend()

        axs[1, 1].plot([item[0] for item in self.Quadruple_peak_reconstructed], np.cumsum([item[1]/np.sum(item[1] for item in self.Quadruple_peak_reconstructed) for item in self.Quadruple_peak_reconstructed]), label = 'Reconstructed')
        axs[1, 1].plot([item[0] for item in self.Quadruple_peak_raw_simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Quadruple_peak_raw_simulated) for item in self.Quadruple_peak_raw_simulated]), label = 'Raw simulated')
        axs[1, 1].plot([item[0] for item in self.Quadruple_peak_Simulated], np.cumsum([item[1]/np.sum(item[1] for item in self.Quadruple_peak_Simulated) for item in self.Quadruple_peak_Simulated]), label = 'Simulated')
        axs[1, 1].set_title(f'Quadruple_peak')
        axs[1, 1].set_xlabel('Wavelength (nm)')
        axs[1, 1].set_ylabel('Cumulative Intensity normalized')
        axs[1, 1].legend()

        if self.save_plots:
            plt.savefig(self.plot_path + "\\" + "Cumulative spectra plot " + title + ".png")

        if not is_streamlit:
            plt.show()
        else:
            st.pyplot(fig)