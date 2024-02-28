from beamngpy import BeamNGpy, Scenario, Vehicle

beamng = BeamNGpy(
    "localhost",
    64256,
    home="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0",
    user="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0\Bin64",
)
beamng.open()

scenario = Scenario("pejas_coast", "Mountain Race")
vehicle = Vehicle("ego_vehicle", model="etk800", license="PEJAS")
# Add it to our scenario at this position and rotation
scenario.add_vehicle(
    vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
)
# Place files defining our scenario for the simulator to read
scenario.make(beamng)
# 010.734|I|GELua.tech_techCore.TechGE|Accepted new client: 127.0.0.1/64189

# Load and start our scenario
beamng.scenario.load(scenario)
beamng.scenario.start()
# Make the vehicle's AI span the map
# vehicle.ai.set_mode("span")
x = input("Hit enter when done...")
if x is not None:
    beamng.close()
# scenarios = beamng.scenario.get_scenarios()
# print(scenarios.keys())
