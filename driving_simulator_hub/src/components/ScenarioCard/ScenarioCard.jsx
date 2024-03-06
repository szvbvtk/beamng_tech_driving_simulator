const ScenarioCard = ({ scenario }) => {
    return (
        <div className="scenario">
            <h3>{scenario.name}</h3>
            <p>{scenario.description}</p>
            <button>Wybierz</button>
        </div>
    )
}

export default ScenarioCard;