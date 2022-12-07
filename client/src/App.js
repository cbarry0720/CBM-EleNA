import logo from "./logo.svg";
import { useState } from "react";
import "./App.css";
import Map from "./components/Map";
import Navigation from "./components/Navigation";

function App() {
	const [path, setPath] = useState([]);

	return (
		<div>
			<Navigation setPath={setPath} />
			<Map path={path} />
		</div>
	);
}

export default App;
