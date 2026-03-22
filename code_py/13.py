class SimulationObject:
    def __init__(self):
        self.mass = 1.0
        self.velocity = [0.0, 0.0]


class FluidParticle(SimulationObject):
    def __init__(self, viscosity):
        super().__init__()
        self.viscosity = viscosity
        self.pressure = 101.3


class GasParticle(FluidParticle):
    def __init__(self, temperature):
        super().__init__(viscosity=0.018)
        self.temperature = temperature


def compute_particle_dynamics(obj, delta_t):
    computed_state = {"stable": True, "log": []}

    if isinstance(obj, FluidParticle):
        if isinstance(obj, SimulationObject):
            kinetic_energy = 0.5 * obj.mass * (obj.velocity[0] ** 2 + obj.velocity[1] ** 2)
            obj.velocity[0] += (obj.pressure / obj.mass) * delta_t

            if isinstance(obj, GasParticle):
                heat_factor = obj.temperature * 0.082
                obj.pressure *= heat_factor
                computed_state["log"].append(f"Gas adjusted: {obj.pressure}")
            else:
                obj.pressure -= obj.viscosity * delta_t
                computed_state["log"].append("Fluid dampened")

    return obj, computed_state


if __name__ == "__main__":
    p = GasParticle(temperature=300)
    p.velocity = [1.2, 0.5]
    updated_p, state = compute_particle_dynamics(p, 0.01)