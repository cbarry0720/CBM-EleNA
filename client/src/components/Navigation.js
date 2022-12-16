import React, { useState } from "react";
import "../styles/navigation.css";
import L from "leaflet";
import axios from "axios";
export default function Navigation({ setPath }) {
	const [fromText, setFromText] = useState("");
	const [toText, setToText] = useState("");
	const [elevationOption, setElevationOption] =
		useState("Maximize Elevation");

	const formOnSubmit = async (e) => {
		e.preventDefault();
		if (fromText.length === 0) {
			alert("Please provide a starting location");
		} else if (toText.length === 0) {
			alert("Please provide a destination");
		} else {
			let fromTextFormatted = "";
			for (let i = 0; i < fromText.length; i++) {
				if (fromText[i] === " ") {
					fromTextFormatted += "+";
				} else {
					fromTextFormatted += fromText[i];
				}
			}
			let toTextFormatted = "";
			for (let i = 0; i < toText.length; i++) {
				if (toText[i] === " ") {
					toTextFormatted += "+";
				} else {
					toTextFormatted += toText[i];
				}
			}

			const url =
				"http://127.0.0.1:5000/route?start=" +
				fromTextFormatted +
				"&finish=" +
				toTextFormatted +
				"&routeMultiplier=2" +
				"&min=" +
				(elevationOption === "Maximize Elevation" ? "False" : "True");
			try {
				const response = await axios.get(url);
				const data = response.data;
				const route = data.route;
				if (
					route[0].x === route[route.length - 1].x &&
					route[0].y === route[route.length - 1].y
				) {
					alert("Cannot use same location for start and end");
					return;
				}
				setPath(route.map((point) => L.latLng(point.y, point.x)));
			} catch (error) {
				alert("Invalid location(s)");
				console.log(error);
			}
		}
	};

	return (
		<div data-testid="nav-container" className="nav-container">
			<form onSubmit={formOnSubmit}>
				<input
					className="from"
					placeholder="From"
					onChange={(e) => {
						setFromText(e.target.value);
					}}
				/>
				<input
					className="to"
					placeholder="To"
					onChange={(e) => {
						setToText(e.target.value);
					}}
				/>
				<select
					onChange={(e) => {
						setElevationOption(e.target.value);
					}}
					className="select"
				>
					<option>Maximize Elevation</option>
					<option>Minimize Elevation</option>
				</select>
				<button className="go" type="submit">
					Go
				</button>
			</form>
		</div>
	);
}
