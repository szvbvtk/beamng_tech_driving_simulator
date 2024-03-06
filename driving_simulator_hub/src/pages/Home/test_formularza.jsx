import axios from "axios";




const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData);
  console.log(data);

  try {
    const response = await axios.post(
      "http://localhost:5000/send-data",
        data
    );
    console.log(response);
  } catch (error) {
    console.log(error);
  }
};

const HomePage = () => {
  return (
    <>
      <div>
        <h1>Home Page</h1>
        <button>Click me</button>
      </div>
      <div>
        <h2>Formularz</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="name">Name:</label>
          <input id="name" name="name" type="text" />
          <button type="submit">Submit</button>
        </form>
      </div>
    </>
  );
};

export default HomePage;
