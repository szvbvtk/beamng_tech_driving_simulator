import { Link } from "react-router-dom";

import classes from "./Home.module.css";

const HomePage = () => {
  return (
    <>
      <div className={classes.container}>
        <Link to="/scenarios" className={classes.link}>
          Przejdź do wyboru scenariuszy
        </Link>
      </div>
    </>
  );
};

export default HomePage;
