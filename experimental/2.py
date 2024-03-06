from beamngpy import BeamNGpy, Scenario, Vehicle

# Instantiate BeamNGpy instance running the simulator from the given path,
# communicating over localhost:64256
bng = BeamNGpy(
    "localhost",
    64256,
    home="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0",
    user="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0\Bin64",
)
# Launch BeamNG.tech
bng.open()
# Create a scenario in west_coast_usa called 'example'
scenario = Scenario("west_coast_usa", "example")
# Create an ETK800 with the licence plate 'PYTHON'
vehicle = Vehicle("ego_vehicle", model="etk800", license="PYTHON")
# Add it to our scenario at this position and rotation
scenario.add_vehicle(
    vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
)

# vehicle2 = Vehicle("ego_vehicle2", model="etk800", license="PYTHON")

# scenario.add_vehicle(
#     vehicle2, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
# )


# vehicle2.ai_set_mode("span")
# Place files defining our scenario for the simulator to read
scenario.make(bng)

# Load and start our scenario
bng.scenario.load(scenario)
bng.scenario.start()

# Make the vehicle's AI span the map
input("Hit enter when done...")

# Set the weather to a specific value