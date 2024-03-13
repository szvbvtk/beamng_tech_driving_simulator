import { RouterProvider, createBrowserRouter } from "react-router-dom";
import HomePage from "./pages/Home/Home";
import ScenarioSelectionPage from "./pages/ScenarioSelection/ScenarioSelection";
import ControlPanelPage from "./pages/ControlPanel/ControlPanel";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/scenarios",
    element: <ScenarioSelectionPage />,
  },
  {
    path: "/scenarios/:scenarioId",
    element: <ControlPanelPage />,
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
