from typing import List

import matplotlib
from matplotlib import pyplot as plt

from src.models import HydraulicModelBase


class Plotter:
    def __init__(self, models: List[HydraulicModelBase]):
        self._models = models

    def plot(self) -> plt.Figure:
        coordinate_data, head_data, elevation_data, temperature_data = self._get_plot_data()

        fig, axs = plt.subplots(2, 1, layout='constrained')
        axs[0].plot(coordinate_data, head_data, label='Линия гидравлического уклона', color='blue')
        axs[0].plot(coordinate_data, elevation_data, label='Профиль трассы', color='green')

        # Закрашивание области под графиком s1
        axs[0].fill_between(coordinate_data, elevation_data, color='#98FB98', alpha=0.5)  # alpha задает прозрачность

        # axs[0].set_xlim(0, 2)
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('s1 and s2')
        axs[0].grid(True)

        axs[1].plot(coordinate_data, temperature_data)
        axs[1].set_ylabel('Coherence')
        axs[1].grid(True)

        fig.savefig("plot")
        return fig


    def _get_plot_data(self):
        coordinate_data = []
        head_data = []
        elevation_data = []
        temperature_data = []

        for model in self._models:
            plot_data = model.get_plot_data()

            coordinate_data += plot_data[0]
            head_data += plot_data[1]
            elevation_data += plot_data[2]
            temperature_data += plot_data[3]
        return coordinate_data, head_data, elevation_data, temperature_data