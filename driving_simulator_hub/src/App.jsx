import { RouterProvider, createBrowserRouter } from "react-router-dom";
import HomePage from "./pages/Home/Home";
import ScenarioSelectionPage from "./pages/ScenarioSelection/ScenarioSelection";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/scenarios",
    element: <ScenarioSelectionPage />,
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
