import React, { useState } from "react";
import "../styles/navigation.css";
import L from "leaflet";
export default function Navigation({ setPointA, setPointB, setPath }) {
	const [fromText, setFromText] = useState("");
	const [toText, setToText] = useState("");

	const buttonOnClick = async () => {
		if (fromText.length === 0) {
			alert("Please provide a starting location");
		} else if (toText.length === 0) {
			alert("Please provide a destination");
		} else {
			const data = {
				route: [
					{ y: 42.3768075, x: -72.5197531, street_count: 3 },
					{ y: 42.376868, x: -72.5197516, street_count: 3 },
					{ y: 42.3770921, x: -72.5197455, street_count: 4 },
					{ y: 42.3772842, x: -72.519748, street_count: 3 },
					{ y: 42.3774973, x: -72.5197482, street_count: 3 },
					{ y: 42.3775214, x: -72.5197449, street_count: 3 },
					{ y: 42.3775624, x: -72.5197457, street_count: 4 },
					{ y: 42.3776212, x: -72.519746, street_count: 4 },
					{ y: 42.3778737, x: -72.5197511, street_count: 4 },
					{ y: 42.3779852, x: -72.5197534, street_count: 4 },
					{ y: 42.3781293, x: -72.5197564, street_count: 4 },
					{ y: 42.3782049, x: -72.5197579, street_count: 4 },
					{ y: 42.378768, x: -72.519507, street_count: 3 },
					{ y: 42.378757, x: -72.5197779, street_count: 4 },
					{ y: 42.3792471, x: -72.5196497, street_count: 3 },
					{ y: 42.3792615, x: -72.5196426, street_count: 4 },
					{ y: 42.3793789, x: -72.5195848, street_count: 4 },
					{ y: 42.3795155, x: -72.519206, street_count: 3 },
					{ y: 42.3799646, x: -72.5190215, street_count: 3 },
					{ y: 42.3799883, x: -72.5193196, street_count: 4 },
					{ y: 42.3800416, x: -72.5193064, street_count: 3 },
				],
				totalDistance: 0,
				totalElevation: 0,
			};

			const route = data.route;
			setPath(route.map((point) => L.latLng(point.y, point.x)));
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
