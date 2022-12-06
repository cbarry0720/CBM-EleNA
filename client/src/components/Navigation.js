import React, { useState } from "react";
import "../styles/navigation.css";
import axios from "axios";

export default function Navigation({ setPointA, setPointB }) {
	const [fromText, setFromText] = useState("");
	const [toText, setToText] = useState("");

	const buttonOnClick = async () => {
		if (fromText.length === 0) {
			alert("Please provide a starting location");
		} else if (toText.length === 0) {
			alert("Please provide a destination");
		} else {
			//replace spaces with pluses for url querying
			let formattedFromText = "";
			for (let i = 0; i < fromText.length; i++) {
				formattedFromText +=
					fromText.charAt(i) === " " ? "+" : fromText.charAt(i);
			}
			let formattedToText = "";
			for (let i = 0; i < toText.length; i++) {
				formattedToText +=
					toText.charAt(i) === " " ? "+" : toText.charAt(i);
			}

			//search from/to locations
			const fromResponse = await axios.get(
				"https://nominatim.openstreetmap.org/search?format=geocodejson&q=" +
					formattedFromText
			);
			const toResponse = await axios.get(
				"https://nominatim.openstreetmap.org/search?format=geocodejson&q=" +
					formattedToText
			);
			//list of from and to locations
			const fromLocations = fromResponse.data.features;
			const toLocations = toResponse.data.features;

			//coordinate arrays for top from/to searches
			const topFromCoord = fromLocations[0].geometry.coordinates;
			const topToCoord = toLocations[0].geometry.coordinates;

			//swap latitute/longitude coordinate locations
			let temp = topToCoord[0];
			topToCoord[0] = topToCoord[1];
			topToCoord[1] = temp;

			//swap latitute/longitude coordinate locations
			temp = topFromCoord[0];
			topFromCoord[0] = topFromCoord[1];
			topFromCoord[1] = temp;

			setPointA(topFromCoord);
			setPointB(topToCoord);
		}
	};

	return (
		<div className="nav-container">
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
			<select className="select">
				<option>Maximize Elevation</option>
				<option>Minimize Elevation</option>
			</select>
			<button className="go" type="button" onClick={buttonOnClick}>
				Go
			</button>
		</div>
	);
}
