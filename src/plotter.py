from typing import List

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from src.models import HydraulicModelBase, Pipeline
from src.models.pipeline import SelfFlow


class Plotter:
    def __init__(
            self,
            models: List[HydraulicModelBase],
            inlet_head: float,  # Костыль №1
    ):
        self._inlet_head = inlet_head
        self._temperature_env = None
        self._models = models
        self.self_flows: List[SelfFlow] = []

    def plot(self) -> plt.Figure:
        coordinate_data, head_data, elevation_data, temperature_data, head_max_data = self._get_plot_data()
        coordinate_data = np.array(coordinate_data) / 1e3
        temperature_data = np.array(temperature_data) - 273.15


        fig, axs = plt.subplots(2, 1, layout='tight', height_ratios=[2,1])
        fig.set_size_inches(10, 12)

        


        axs[0].plot(coordinate_data, head_data, label='Линия гидравлического уклона', color='blue')
        axs[0].plot(coordinate_data, elevation_data, label='Профиль трассы', color='green')
        axs[0].plot(coordinate_data, head_max_data, label='Максимальный напор', color='red', linestyle='--')
        axs[0].plot(
            (coordinate_data[0], coordinate_data[0]),
            (elevation_data[0], self._inlet_head),
            label='Подпор', color='red')
        if self.self_flows:
            i = 1
            for self_flow in self.self_flows:
                
                axs[0].plot([self_flow.start_coordinate / 1000, self_flow.end_coordinate / 1000], [self_flow.start_elevation, self_flow.end_elevation], color='red')
                
                x = (self_flow.start_coordinate + self_flow.end_coordinate) / 2 / 1000
                y = (self_flow.start_elevation + self_flow.end_elevation) / 2 + 200
                
                # Форматирование текста
                text = f"Саматечный участок №{i}\nДлина: {self_flow.length / 1000:.3f} км\nCтепень заполнения: {self_flow.filling_degree:.2f}"
                bbox={"fill": False,
                   "linestyle": "solid",
                   "linewidth": 0.5}
               
                axs[0].text(x, y, text, bbox=bbox, fontsize=10, ha='center', va='center')
                i += 1

        axs[0].legend(loc='best')
        axs[0].fill_between(coordinate_data, elevation_data, color='#98FB98', alpha=0.5)  # alpha задает прозрачность

        axs[0].set_xlabel('Координата, км')
        axs[0].set_ylabel('Напор, м')
        axs[0].grid(True)

        axs[1].plot(coordinate_data, temperature_data, label='Линия изменения температуры', color='blue')
        # if self._temperature_env:
        #     axs[1].axhline(y=self._temperature_env - 273.15, color='red', linestyle='--', label='Температура окружающей среды')
        axs[1].legend(loc='right')
        axs[1].set_xlabel('Координата, км')
        axs[1].set_ylabel('Температура, С')
        axs[1].grid(True)

        fig.savefig("plot")
        return fig

    def _get_plot_data(self):
        coordinate_data = []
        head_data = []
        elevation_data = []
        temperature_data = []
        head_max_data = []

        for model in self._models:


            plot_data = model.get_plot_data()
            coordinate_data += plot_data[0]
            head_data += plot_data[1]
            elevation_data += plot_data[2]
            temperature_data += plot_data[3]
            head_max_data += plot_data[4]

            if isinstance(model, Pipeline):
                self._temperature_env = model.temperature_env
                self.self_flows += model.self_flows


        return coordinate_data, head_data, elevation_data, temperature_data, head_max_data
