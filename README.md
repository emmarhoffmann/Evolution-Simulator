# Evolution Simulator

## About
This is a Python and Pygame-based simulation where creatures exhibit behaviors such as moving, finding food, reproducing, mutating, and dying, mimicking the processes of natural evolution. The simulator allows creatures to evolve over time based on the conditions of their environment, with random mutations influencing future generations.

## Features
- **Movement and Interaction**: Creatures move around the environment, seeking food to sustain themselves.
- **Reproduction**: When creatures find a suitable partner and conditions are met, they reproduce, passing on traits to the next generation.
- **Mutation**: During reproduction, random mutations occur, influencing the behavior, appearance, or survival chances of the offspring.
- **Energy-based Life Cycle**: Creatures must maintain their energy by finding food or they risk death due to starvation.
- **Gender Representation**: Creatures can have different genders, influencing their reproductive behavior.

## Project Structure
- `EvolutionSimulator.py`: The main Python file that runs the simulation, handling creature behavior, the environment, and the evolutionary processes.
  - **Creature Class**: Represents the creatures in the ecosystem, managing their energy, position, gender, and behavior.
  - **Ecosystem Management**: Handles the overall environment where creatures live, reproduce, and die.
  - **Pygame Integration**: Uses Pygame to visualize the simulation, rendering creatures, food, and environmental interactions.
