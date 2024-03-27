import { useParams } from 'react-router-dom';
import axios from "axios";
import React from 'react';



const handleGetCurrentSpeed = async() => {
    console.log("Getting current speed");
    const data = {
        command: "get-current-speed",
        payload: {}
    };
    try {
        const response = await axios.post(
            "http://localhost:5000/send-data",
            data
        );
        console.log(response.data);
    }catch (error) {
        console.log(error);
    }
}

const handleStartScenario = async(params) => {
    console.log(`Starting scenario ${params.scenarioId}`);
    const scenarioId = params.scenarioId.split('-').pop();
    const data = {
        command: "start-scenario",
        payload: {
            scenarioId: scenarioId
        }
    };
    try {
        const response = await axios.post(
          "http://localhost:5000/send-data",
            data
        );
        console.log(response);
      } catch (error) {
        console.log(error);
      }
}

const ControlPanelPage = () => {
    const params = useParams();

    return (
        <div>
            <h1>Control Panel</h1>
            <p>Scenario ID: {params.scenarioId}</p>
            <button onClick={() => handleStartScenario(params)}>Start Scenario</button><br></br>
            <button onClick={() => handleGetCurrentSpeed()}>Get Current Speed</button>
        </div>
    );
}

export default ControlPanelPage;

