# 🧬 Cellular Ecosystem Simulator

A 2D ecosystem simulator built in Python, modeling cellular behavior, reproduction, and evolution within a virtual environment incorporating physical and chemical constraints.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🔬 Overview

This project simulates a cellular ecosystem where cells evolve within a 2D environment. Each cell can:

* Move autonomously
* Reproduce based on defined probabilities
* Age and die naturally
* Interact with environmental factors (temperature, glucose)

The simulation uses realistic physical models with metric units for cell size (μm³), and includes biological parameters such as replication rates and maximum age.

## ✨ Features

### 🎯 Cellular Simulation

* **Intelligent Cells**: Random movement with collision detection
* **Reproduction**: Probabilistic replication with available space check
* **Life Cycle**: Progressive aging visualized by color changes
* **Natural Death**: Automatic removal of old cells

### 🌍 Physical Environment

* **Environmental Grid**: Coordinate system with occupancy management
* **Physical Parameters**: Temperature and glucose concentration
* **Spatial Constraints**: Prevention of cell overlap

### 📊 Analysis and Visualization

* **Graphical Interface**: Real-time visualization using Pygame
* **Data Collection**: Automatic logging of cell population
* **Scientific Graphs**: Population dynamics visualized with Matplotlib

### 🛠️ Utility Tools

* **Directional System**: Movement in 8 cardinal and diagonal directions
* **Data Logger**: Recording and visualization of metrics
* **Modularity**: Extensible object-oriented architecture

## 🔧 Installation

### Prerequisites

* Python 3.8 or higher
* pip (Python package manager)

### Quick Installation

```bash
# Clone the repository
git clone <your-repo>
cd project

# Install dependencies
pip install pygame matplotlib

# Run the simulation
python main.py
```

## 🎮 Usage


### Simulation Parameters

Modify constants in `Cell.py` to customize your simulation:

```python
# Cellular parameters
replication_rate = 1/1000    # Probability of reproduction
max_age = 6000               # Maximum age (cycles)
speed = 5                    # Movement speed

# Physical dimensions
calculus_width = 1e-6        # Width in meters
width = 20                   # Display size in pixels
```

### Controls

* **Close**: Click the window's close button
* **Observation**: Simulation stops automatically if no cells remain

## 🔬 Scientific Model

### Realistic Biological Parameters

* **Cell Size**: 1μm × 1μm × 1μm (typical bacterial volume)
* **Membrane Surface**: 6μm² (perfect cube)
* **Replication Rate**: 0.1% per cycle (adjustable)
* **Life Expectancy**: 6000 simulation cycles

### Physical Models

* **Brownian Motion**: Random movement in 8 directions
* **Volume Exclusion**: Prevention of spatial overlap
* **Visual Aging**: Linear RGB interpolation (blue → black)

## 🛠️ Development

### Possible Extensions

* [ ] **Multi-species**: Different cell types with unique characteristics
* [ ] **Metabolism**: Glucose consumption and waste production
* [ ] **Mutations**: Genetic evolution of cell parameters
* [ ] **Interactions**: Cell-to-cell communication
* [ ] **Biomes**: Environments with temperature/nutrient gradients

## 📈 Metrics and Analysis

Integrated logging captures:

* **Population**: Number of cells over time
* **Dynamics**: Births, deaths, movements
* **Graphs**: Automated visualization via Matplotlib
