import ScenarioCard from "../../components/ScenarioCard/ScenarioCard";

import classes from "./ScenarioSelection.module.css";
import SCENARIOS from "../../assets/data/scenarios.json";

const ScenarioSelectionPage = () => {
  return (
    <div className={classes.container}>
      <div className={classes.header}>
        <h1>Scenario Selection</h1>
        <h2>Choose a scenario to play</h2>
      </div>
      <div className={classes.scenarioList}>
        {SCENARIOS.map((scenario) => (
          <ScenarioCard scenario={scenario} key={scenario.id} />
        ))}
      </div>
    </div>
  );
};

export default ScenarioSelectionPage;
