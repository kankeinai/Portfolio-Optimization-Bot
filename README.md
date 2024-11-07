
# Portfolio Optimization Bot

This project provides a portfolio optimization solution through a Telegram bot interface, focusing on investment decisions with stochastic factors, constraints, and dependencies between projects. Users can interact with the bot to upload data, define parameters, and receive an optimization report.

For creation of this README.MD file cudos to ChatGPT-4o

## Features

- **Optimization**: Maximize portfolio revenue within a budget, considering each project's cost, benefit, and risk of failure.
- **Stochastic Modeling**: Account for scenarios of project success/failure, modeling uncertainty in outcomes.
- **Dependency Constraints**: Ensures that projects with dependencies are selected accordingly.
- **Analysis**: Provides insight into revenue distributions, expected value of perfect information, and price of stochastic solutions.
- **User-Friendly Bot Interface**: Telegram bot assists users in submitting project data and retrieving a detailed report.

## Getting Started

### Prerequisites

- Python 3.x
- Required packages listed in `requirements.txt`
- Telegram account and API credentials

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Portfolio_Optimization.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Telegram bot credentials by creating a `.env` file or by updating `config.py`.

### Usage

1. **Prepare Input Data**: Ensure that your input file (`.xlsx` or `.csv`) contains the columns: `project`, `benefit`, `cost`, `risk`, `dependence`. Refer to the example format in `instructions.pdf`.

2. **Run the Bot**: Execute the bot with:
   ```bash
   python bot.py
   ```

3. **Interact via Telegram**: 
   - Upload your input file to the bot.
   - Set the required optimization parameters.
   - Receive the generated report.

### Output

The bot generates an automatically formatted report (`sample_report.pdf` for reference) that includes:

- Project selection based on optimization
- Expected revenue analysis for each scenario
- Graphical distribution of revenue for training and test sets
- Calculations of stochastic solution metrics

### Example Report

A sample report is provided in `sample_report.pdf`. This document demonstrates the final output structure, including revenue distributions, budget utilization, and recommended project investments.

## Files Overview

- **bot.py**: The main bot script to handle Telegram interactions.
- **config.py**: Configuration file for API credentials and settings.
- **keyboards.py**: Defines custom keyboards for the Telegram bot interface.
- **utils.py**: Helper functions for data processing.
- **script.jl**: Julia script for computationally intensive tasks.
- **Manifest.toml**: Configuration file for the Julia environment.
- **Project.toml**: Defines dependencies and project setup for the Julia script.
- **example_files/**: Contains example input files demonstrating the required format.
- **requirements.txt**: Lists Python dependencies needed for the project.
- **instructions.pdf**: Detailed explanation of the model, constraints, and usage instructions.

## Project Structure

- **`/example_files`**: Folder containing example input files for testing.
- **`bot.py`**: Main bot script to handle Telegram interactions.
- **`config.py`**: Configuration settings for bot credentials and parameters.
- **`keyboards.py`**: Defines custom keyboards for user interaction in the Telegram bot.
- **`utils.py`**: Contains utility functions to support data processing.
- **`script.jl`**: A Julia script for handling optimization calculations.
- **`Manifest.toml` and `Project.toml`**: Define the Julia environment and dependencies.
- **`requirements.txt`**: Specifies Python dependencies.
- **`README.md`**: Documentation file (this file) for project overview and usage instructions.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## Contact

For questions or suggestions, contact [Milana](milka3341@gmail.com).
