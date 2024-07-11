# Schelling Segregation Model Simulation

This Python program simulates Schelling's model of segregation, visualizing the dynamics of agents in a city based on their happiness with their neighbors. The model demonstrates how individual preferences for neighbors of a similar type can lead to large-scale patterns of segregation.

See: Schelling, T. C. (1969). Models of Segregation. The American Economic Review, 59(2), 488–493.

## Features

- Configurable city size, population density, happiness threshold, and number of types of inhabitants.
- Real-time visualization of the simulation.
- Ability to save the simulation as a GIF for later viewing or sharing.

## Installation

To run this program, you need Python installed on your system along with the following packages:
- `numpy`
- `matplotlib`

## Usage

The main simulation parameters are as follows:
- `city_size` (tuple): The size of the grid used for the simulation, e.g., `(50, 50)`.
- `population_density` (float): The fraction of the grid that is occupied by agents, e.g., `0.9`.
- `happiness_threshold` (float): The threshold of similar neighbors required for an agent to be happy, e.g., `0.5`.
- `number_types` (int): The number of different types of agents, e.g., `2`.

The main parameters for the visualization and saving of the simulations are as follows:
- `save_simulation` (bool): Set to `True` to save the animation as a GIF, or `False` to view the real-time visualization of the simulation.
- `updates_per_frame` (int): The number of simulation updates per frame of the animation, e.g., `100`.
- `interval` (int): The delay between frames in milliseconds, e.g., `200`.
- `filename` (str): The name of the file to save the animation, e.g., `"simulation"`.
- `frames` (int): The number of frames to generate in the saved animation, e.g., `100`.
- `fps` (int): Frames per second for the saved animation, e.g., `20`.

## Example

An example of usage of the package is presented in the `main.py` file with default values for the parameters, which you can adjust as needed. To run the example simulation, execute the `main.py` file:
```bash
python main.py
```

The following image is a result of a simulation with the default parameters of the `main.py` file:
<p align="center">
  <img src="https://github.com/Thomas-bssnt/Schelling-model/assets/49919330/6ecfbd37-f011-4d1d-ae01-209060caf254" height="50%" width="50%">
</p>

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements or bug fixes.
