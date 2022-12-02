import logo from "./logo.svg";
import { useState } from "react";
import "./App.css";
import Map from "./components/Map";
import Navigation from "./components/Navigation";

function App() {
	const [pointA, setPointA] = useState([]);
	const [pointB, setPointB] = useState([]);

	return (
		<div>
			<Navigation setPointA={setPointA} setPointB={setPointB} />
			<Map pointA={pointA} pointB={pointB} />
		</div>
	);
}

export default App;
