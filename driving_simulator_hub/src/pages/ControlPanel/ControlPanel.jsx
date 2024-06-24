import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import { withRouter } from "react-router-dom";
import React from "react";

import classes from "./ControlPanel.module.css";

const ControlPanelPage = () => {
  const params = useParams();

  const [currentData, setcurrentData] = useState(0);
  const [isGameStarted, setIsGameStarted] = useState(false);

  const startScenario = async (params) => {
    console.log(`Starting scenario ${params.scenarioId}`);
    const scenarioId = params.scenarioId.split("-").pop();
    setcurrentData(-1);
    const data = {
      command: "start-scenario",
      payload: {
        scenarioId: scenarioId,
      },
    };
    try {
      const response = await axios.post(
        "http://localhost:5000/send-data",
        data
      );
      setIsGameStarted(true);
    } catch (error) {
      console.log(error);
    }
  };

  const stopScenario = async () => {
    console.log("Stopping scenario");
    const data = {
      command: "stop-scenario",
      payload: {},
    };
    try {
      const response = await axios.post(
        "http://localhost:5000/send-data",
        data
      );
      setIsGameStarted(false);
    } catch (error) {
      console.log(error);
    }
  };

  const getCurrentData = async () => {
    console.log("Getting current data");
    const data = {
      command: "get-current-data",
      payload: {},
    };
    try {
      const response = await axios.post(
        "http://localhost:5000/send-data",
        data
      );
      // console.log(response.data);
      // console.log(JSON.parse(response.data)['left_signal']);
      setcurrentData(JSON.parse(response.data));
      console.log(currentData.left_signal);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (isGameStarted) {
      const interval = setInterval(() => {
        getCurrentData();
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [isGameStarted]);

  return (
    <div>
      <div id={classes.title}>
        {/* <h1>Control Panel</h1> */}
        <p>Scenario ID: {params.scenarioId}</p>
      </div>
      <div id={classes.buttons}>
        <button onClick={() => startScenario(params)}>Start Scenario</button>
        <button onClick={stopScenario}>Stop Scenario</button>
      </div>
      <br></br>
      {currentData.speed && (
        <ul id={classes.info}>
          <li>Speed: {currentData.speed}</li>
          <li>Left indicator: {currentData.left_signal.toString()}</li>
          <li>Right indicator: {currentData.right_signal.toString()}</li>
          <li>Gear: {currentData.gear}</li>
        </ul>
      )}
      {currentData === -1 && <h3>Loading...</h3>}
    </div>
  );
};

export default ControlPanelPage;
