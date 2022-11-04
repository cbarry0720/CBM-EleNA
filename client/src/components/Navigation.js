import React from "react";
import "../styles/navigation.css";

export default function Navigation() {
	return (
		<div className="nav-container">
			<input className="from" placeholder="From" />
			<input className="to" placeholder="To" />
			<select className="select">
				<option>Maximize Elevation</option>
				<option>Minimize Elevation</option>
			</select>
		</div>
	);
}
