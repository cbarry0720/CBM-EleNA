import React from "react";
import {
	MapContainer,
	TileLayer,
	Marker,
	Popup,
	Polyline,
} from "react-leaflet";
import { Icon } from "leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";
import { useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function Map({ path }) {
	const pointA = path.length > 0 ? path[0] : [];
	const pointB = path.length > 0 ? path[path.length - 1] : [];

	const center =
		pointA.length > 0 && pointB.length > 0
			? [(pointA[0] + pointB[0]) / 2, (pointA[1] + pointB[1]) / 2]
			: [42.340382, -72.49681];

	function getZoom() {
		const latitudeDiff = Math.abs(pointA[1] - pointB[1]);
		return Math.floor(Math.log2(360.0 / latitudeDiff));
	}

	const zoom = pointA.length > 0 && pointB.length > 0 ? getZoom() : 13;

	const MyComponent = () => {
		const map = useMap();
		map.setView(center, zoom);
		return null;
	};

	return (
		<MapContainer style={{ height: "100vh" }} center={center} zoom={zoom}>
			<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
			<MyComponent />
			{path.length > 0 ? (
				<Marker
					position={pointA}
					icon={
						new Icon({
							iconUrl: markerIconPng,
							iconSize: [25, 41],
							iconAnchor: [12, 41],
						})
					}
				></Marker>
			) : (
				<></>
			)}
			{path.length > 0 ? (
				<Marker
					position={pointB}
					icon={
						new Icon({
							iconUrl: markerIconPng,
							iconSize: [25, 41],
							iconAnchor: [12, 41],
						})
					}
				></Marker>
			) : (
				<></>
			)}
			,
			{path.length > 0 ? (
				<Polyline
					pathOptions={{ color: "red" }}
					positions={path}
				></Polyline>
			) : (
				<></>
			)}
		</MapContainer>
	);
}
