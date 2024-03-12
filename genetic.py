import random
import numpy as np

class EightPuzzleGeneticSolver:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.population_size = 100
        self.generations = 999
        self.mutation_rate = 0.3

    def generate_individual(self):
        return random.sample(range(1, 10), 9)

    def fitness(self, individual):
        return sum(1 for a, b in zip(individual, self.goal_state.flatten()) if a == b)

    def crossover(self, parent1, parent2):
        split_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:split_point] + parent2[split_point:]
        child2 = parent2[:split_point] + parent1[split_point:]
        return child1, child2

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            idx1, idx2 = sorted(random.sample(range(len(individual)), 2))
            individual[idx1:idx2] = individual[idx1:idx2][::-1]
        return individual

    def evolve(self):
        population = [self.generate_individual() for _ in range(self.population_size)]

        with open("generations.txt", "w") as f:
            # Write initial population
            f.write("Población inicial:\n")
            for i, individual in enumerate(population):
                f.write(f"  Individuo {i + 1}: {individual}\n")

            for generation in range(self.generations):
                population.sort(key=self.fitness, reverse=True)
                parents = population[:self.population_size // 2]

                # Write information of the current generation to the file
                f.write(f"\nGeneración {generation}:\n")
                for i, parent in enumerate(parents):
                    f.write(f"  Pareja {i + 1}: {parent}\n")

                new_population = parents.copy()
                while len(new_population) < self.population_size:
                    parent1, parent2 = random.choices(parents, k=2)
                    child1, child2 = self.crossover(parent1, parent2)
                    child1 = self.mutate(child1)
                    child2 = self.mutate(child2)
                    new_population.append(child1)
                    new_population.append(child2)

                population = new_population
                population.sort(key=self.fitness, reverse=True)

                # Write additional information to the file
                f.write("  Nuevos individuos:\n")
                for i in range(self.population_size // 2):
                    f.write(f"    {new_population[i * 2]} (Fitness: {self.fitness(new_population[i * 2])})\n")
                    f.write(f"    {new_population[i * 2 + 1]} (Fitness: {self.fitness(new_population[i * 2 + 1])})\n")

                f.write("  Individuos que mutaron:\n")
                for i in range(self.population_size // 2, self.population_size):
                    f.write(f"    {new_population[i]} (Fitness: {self.fitness(new_population[i])})\n")

                f.write("  Números en posición correcta:\n")
                for i in range(self.population_size // 2):
                    correct_positions = [num for num, (a, b) in enumerate(zip(new_population[i], self.goal_state.flatten()), 1) if a == b]
                    f.write(f"    {correct_positions}\n")

                # Check if solution found
                if self.fitness(parents[0]) == len(self.goal_state.flatten()):
                    f.write("¡Solución encontrada!\n")
                    return np.array(parents[0]).reshape(3, 3)

        # Return best individual found if solution not found
        return np.array(population[0]).reshape(3, 3)

import numpy as np

def establecerEstadosDesdeArchivo(nombreArchivo):
    matrizInicial = []
    matrizFinal = []
    try:
        with open(nombreArchivo, 'r') as archivo:
            leyendoConfiguracionFinal = False
            for i, linea in enumerate(archivo):
                if linea.strip() == "-":
                    leyendoConfiguracionFinal = True
                    continue
                fila = list(map(int, linea.strip().split()))
                if not leyendoConfiguracionFinal:
                    matrizInicial.append(fila)
                else:
                    matrizFinal.append(fila)

            if len(matrizInicial) != 3 or len(matrizFinal) != 3:
                raise ValueError("Se esperan 3 filas para la matriz inicial y final.")

            # Convertir a arrays numpy
            initial_state = np.array(matrizInicial).flatten()
            goal_state = np.array(matrizFinal).flatten()

            return initial_state, goal_state

    except FileNotFoundError:
        print("El archivo no existe.")
        return None, None
    except ValueError as e:
        print(e)
        return None, None

# Ejemplo de uso
initial_state, goal_state = establecerEstadosDesdeArchivo("configuracion_inicial.txt")
if initial_state is not None and goal_state is not None:
    print("Estados cargados exitosamente desde el archivo.")
    solver = EightPuzzleGeneticSolver(initial_state, goal_state)
    print("Estado inicial:")
    print(np.array(initial_state).reshape(3, 3))
    solution = solver.evolve()
    print("\nSolución encontrada:")
    print(solution)
else:
    print("No se pudieron cargar los estados desde el archivo.")

