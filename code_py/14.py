class AvionicsSystem:
    def __init__(self, serial):
        self.serial = serial
        self.diagnostic_log = []


class UnmannedAerialVehicle(AvionicsSystem):
    def __init__(self, serial, battery_level):
        super().__init__(serial)
        self.battery_level = battery_level
        self.is_airborne = False


class CargoDrone(UnmannedAerialVehicle):
    def __init__(self, serial, battery_level, payload_kg):
        super().__init__(serial, battery_level)
        self.payload_kg = payload_kg
        self.delivery_status = "IDLE"


def execute_flight_sequence(vehicle, flight_plan):
    telemetry = {"coordinates": [0, 0, 0], "efficiency": 1.0}

    if isinstance(vehicle, UnmannedAerialVehicle):
        vehicle.is_airborne = True
        step_count = len(flight_plan)
        telemetry["efficiency"] = (vehicle.battery_level / 100) * step_count
        vehicle.diagnostic_log.append(f"UAV flight sequence initiated for {vehicle.serial}")

        for coord in flight_plan:
            telemetry["coordinates"] = [c + 1.5 for c in coord]

    elif isinstance(vehicle, CargoDrone):
        vehicle.delivery_status = "IN_TRANSIT"
        vehicle.payload_kg -= 0.5
        telemetry["status"] = "CARGO_MODE_ACTIVE"
        vehicle.diagnostic_log.append("Executing specialized cargo protocols")

    return vehicle, telemetry


if __name__ == "__main__":
    drone = CargoDrone(serial="ALPHA-9", battery_level=85, payload_kg=12.5)
    plan = [[10, 20, 100], [15, 25, 120]]
    updated_drone, data = execute_flight_sequence(drone, plan)