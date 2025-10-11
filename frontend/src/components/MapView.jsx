import React, { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from "react-leaflet";

export default function MapView({ areas, center, zoom = 13 }) {
  const mapRef = useRef();

  // choose center
  const mapCenter = center ?? (areas && areas.length ? [areas[0].lat, areas[0].lng] : [18.5204,73.8567]);

  return (
    <div className="map-container shadow-lg mt-6">
      <MapContainer center={mapCenter} zoom={zoom} style={{ height: "100%", width: "100%" }} ref={mapRef}>
        <TileLayer
          attribution='© OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {areas && areas.map(a => {
          const color = a.blsi >= 75 ? "green" : a.blsi >= 50 ? "orange" : "red";
          return (
            <Marker key={a.id} position={[a.lat, a.lng]}>
              <Popup>
                <div className="text-sm">
                  <strong>{a.name}</strong><br/>
                  BLSI: {Math.round(a.blsi)}<br/>
                  Rent: ₹{a.avg_rent}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
