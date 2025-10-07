// frontend/src/pages/Home.jsx
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from "react-leaflet";
import L from "leaflet";
import { useEffect, useRef } from "react";

// small marker fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

export default function Home({ areas = [], recs = [] }) {
  const mapRef = useRef();

  useEffect(() => {
    if (recs && recs.length > 0 && mapRef.current) {
      try {
        const map = mapRef.current;
        const first = recs[0];
        if (first && first.lat && first.lng) {
          map.setView([first.lat, first.lng], 13);
        }
      } catch (e) { /* ignore */ }
    }
  }, [recs]);

  const center = areas.length ? [areas[0].lat || 19.076, areas[0].lng || 72.8777] : [19.076, 72.8777];

  return (
    <div className="map-wrap">
      <MapContainer center={center} zoom={12} scrollWheelZoom style={{height:'100%', width:'100%'}} whenCreated={m => mapRef.current = m}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        {areas.map(a => (
          a.lat && a.lng && (
            <Marker key={a.id} position={[a.lat, a.lng]}>
              <Popup>
                <strong>{a.name}</strong><br/>
                {a.city} — BLSI: {a.blsi ?? "n/a"}
                <br/>
                Badges: {(a.badges||[]).join(", ")}
              </Popup>
            </Marker>
          )
        ))}

        {recs.map(r => r.lat && r.lng && (
          <CircleMarker key={`rec-${r.areaId}`} center={[r.lat, r.lng]} radius={10} pathOptions={{color:'green'}}>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
