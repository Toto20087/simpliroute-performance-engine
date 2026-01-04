import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix Leaflet icon issue in React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

interface Stop {
    lat: number;
    lng: number;
    address: string;
}

interface MapProps {
    stops: Stop[];
    optimizedOrder?: string[]; // List of addresses in order
}

function ChangeView({ center }: { center: [number, number] }) {
    const map = useMap();
    map.setView(center);
    return null;
}

export function MapComponent({ stops, optimizedOrder }: MapProps) {
    // Default center (Buenos Aires)
    const center: [number, number] = stops.length > 0
        ? [stops[0].lat, stops[0].lng]
        : [-34.6037, -58.3816];

    // Determine path coordinates if optimized
    let pathCoordinates: [number, number][] = [];

    if (optimizedOrder && optimizedOrder.length > 0) {
        // Map addresses back to coordinates
        // Create a lookup map
        const addrToStop = new Map(stops.map(s => [s.address, s]));

        optimizedOrder.forEach(addr => {
            const stop = addrToStop.get(addr);
            if (stop) {
                pathCoordinates.push([stop.lat, stop.lng]);
            }
        });
    }

    return (
        <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
            <ChangeView center={center} />
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {stops.map((stop, idx) => (
                <Marker key={idx} position={[stop.lat, stop.lng]}>
                    <Popup>
                        {stop.address}
                    </Popup>
                </Marker>
            ))}

            {pathCoordinates.length > 0 && (
                <Polyline
                    positions={pathCoordinates}
                    pathOptions={{ color: 'red', weight: 4 }}
                />
            )}
        </MapContainer>
    );
}
