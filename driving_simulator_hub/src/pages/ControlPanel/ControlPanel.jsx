import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import React from "react";

import classes from "./ControlPanel.module.css";

const ControlPanelPage = () => {
  const params = useParams();
  const [currentSpeed, setCurrentSpeed] = useState(0);
  const [isGameStarted, setIsGameStarted] = useState(false);

  const startScenario = async (params) => {
    console.log(`Starting scenario ${params.scenarioId}`);
    const scenarioId = params.scenarioId.split("-").pop();
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
      setCurrentSpeed(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      if (isGameStarted) {
        await getCurrentData();
      }
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, [isGameStarted]);

  return (
    <div>
      <h1>Control Panel</h1>
      <p>Scenario ID: {params.scenarioId}</p>
      <button onClick={() => startScenario(params)}>Start Scenario</button>
      <button onClick={stopScenario}>Stop Scenario</button>
      <br></br>
      {isGameStarted && <p id={classes.info}>Current Speed: {currentSpeed}</p>}
    </div>
  );
};

export default ControlPanelPage;
