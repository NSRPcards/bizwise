import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

const defaultIcon = new L.Icon({
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function Home({ businesses }) {
  const defaultCenter = [19.076, 72.8777]; // Mumbai center

  return (
    <div style={{ height: "400px", width: "100%", marginTop: "20px" }}>
      <MapContainer
        center={defaultCenter}
        zoom={10}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='© <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {businesses.map((biz, index) => (
          <Marker
            key={index}
            position={[19.076, 72.8777]} // temporary position (Mumbai)
            icon={defaultIcon}
          >
            <Popup>
              <b>{biz.name}</b>
              <br />
              {biz.location} <br />
              {biz.category}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

export default Home;
