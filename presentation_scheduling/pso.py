import numpy as np

class PSO:
    def __init__(self, objective_function, num_particles, dimensions, bounds, max_iter):
        self.objective_function = objective_function
        self.num_particles = num_particles
        self.dimensions = dimensions
        self.bounds = bounds
        self.max_iter = max_iter
        self.inertia = 0.5
        self.cognitive = 1.5
        self.social = 1.5
        self.particles = np.random.rand(self.num_particles, self.dimensions)
        self.velocities = np.random.rand(self.num_particles, self.dimensions)
        self.pbest = self.particles.copy()
        self.gbest = self.particles[np.argmin([self.objective_function(p) for p in self.particles])]

    def optimize(self):
        for _ in range(self.max_iter):
            for i, particle in enumerate(self.particles):
                r1, r2 = np.random.rand(2)
                self.velocities[i] = (self.inertia * self.velocities[i] +
                                      self.cognitive * r1 * (self.pbest[i] - particle) +
                                      self.social * r2 * (self.gbest - particle))
                self.particles[i] = particle + self.velocities[i]

                # Apply bounds
                self.particles[i] = np.clip(self.particles[i], self.bounds[:, 0], self.bounds[:, 1])

                if self.objective_function(self.particles[i]) < self.objective_function(self.pbest[i]):
                    self.pbest[i] = self.particles[i]

            self.gbest = self.particles[np.argmin([self.objective_function(p) for p in self.particles])]

        return self.gbest, self.objective_function(self.gbest)
