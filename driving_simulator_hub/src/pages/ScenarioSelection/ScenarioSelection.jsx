import ScenarioCard
 from "../../components/ScenarioCard/ScenarioCard";
import classes from "./ScenarioSelection.module.css";

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

const ScenarioSelectionPage = () => {
  return (
    <div className={classes.container}>
      <div className={classes.header}>
        <h1>Scenario Selection</h1>
        <h2>Choose a scenario to play</h2>
      </div>
      <div className={classes.scenarioList}>
        {SCENARIOS.map((scenario) => (
          <ScenarioCard scenario={scenario} />
        ))}
      </div>
    </div>
  );
};

export default ScenarioSelectionPage;
