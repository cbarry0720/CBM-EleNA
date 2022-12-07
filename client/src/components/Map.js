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
import "../styles/map.css";

export default function Map({ path }) {
	const center =
		path.length > 0
			? [
					(path[0].lat + path[path.length - 1].lat) / 2,
					(path[0].lng + path[path.length - 1].lng) / 2,
			  ]
			: [42.340382, -72.49681];

	function getZoom() {
		const latitudeDiff = Math.abs(path[0].lng - path[path.length - 1].lng);
		return Math.floor(Math.log2(360.0 / latitudeDiff)) + 1;
	}

	const zoom = path.length > 0 ? getZoom() : 13;

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
					position={[path[0].lat, path[0].lng]}
					icon={
						new Icon({
							iconUrl: markerIconPng,
							iconSize: [25, 41],
							iconAnchor: [12, 41],
						})
					}
				>
					<Popup className="popup">
						<h6>Start</h6>
					</Popup>
				</Marker>
			) : (
				<></>
			)}
			{path.length > 0 ? (
				<Marker
					position={[
						path[path.length - 1].lat,
						path[path.length - 1].lng,
					]}
					icon={
						new Icon({
							iconUrl: markerIconPng,
							iconSize: [25, 41],
							iconAnchor: [12, 41],
						})
					}
				>
					<Popup className="popup">
						<h6>End</h6>
					</Popup>
				</Marker>
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
