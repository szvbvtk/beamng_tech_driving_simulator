import { useNavigate } from "react-router-dom";

import classes from "./ScenarioCard.module.css";

const ScenarioCard = ({ scenario }) => {
  const imagePath = require(`../../assets/images/${scenario.img_name}`);
  const navigate = useNavigate();

  const handleScenarioSelection = () => {
    console.log(
      `Selected scenario: ${scenario.name}; command: ${scenario.command}`
    );
    navigate(`scenario-${scenario.id}`);
  };

  return (
    <div className={classes.scenario} onClick={handleScenarioSelection}>
      <div className={classes.image}>
        {" "}
        <img src={imagePath} alt={"scenario 1"} />
      </div>

      <div className={classes.title}>
        <h3>{scenario.name}</h3>
      </div>
      <div className={classes.description}>{scenario.description}</div>
    </div>
  );
};

export default ScenarioCard;
