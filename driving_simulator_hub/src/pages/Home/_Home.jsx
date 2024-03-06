import ScenarioCard from "../../components/ScenarioCard/ScenarioCard"

const SCENARIOS = [
  {
    id: 1,
    name: "scenariusz 1",
    description: "opis scenariusza 1",
    command: "run_scenario_1",
  },
  {
    id: 2,
    name: "scenariusz 2",
    description: "opis scenariusza 2",
    command: "run_scenario_2",
  },
  {
    id: 3,
    name: "scenariusz 3",
    description: "opis scenariusza 3",
    command: "run_scenario_3",
  },
];

const HomePage = () => {
  return (
    <>
      <div className="container">
        <h1>Wybierz scenariusz</h1>
        <div className="scenario-list">
          {SCENARIOS.map((scenario) => (
            <ScenarioCard scenario={scenario} />
          ))}
        </div>
      </div>
    </>
  );
};

export default HomePage;
