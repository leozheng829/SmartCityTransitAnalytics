import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { getBusPositions, getTrainData } from '@/lib/api';
import { Bus, TrainFront, Map } from 'lucide-react';

// Replace with your Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1Ijoic21hcnRjaXR5dHJhbnNpdCIsImEiOiJjbDJnN2U1N2kwMDVhM2lydW4yZnZsNXpkIn0.H8Y3NbVX_4yQBhxrLRktzA';

interface LiveMapProps {
  type: "bus" | "train";
}

export const LiveMap: React.FC<LiveMapProps> = ({ type }) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;

    // Initialize map
    if (!map.current) {
      try {
        map.current = new mapboxgl.Map({
          container: mapContainer.current,
          style: 'mapbox://styles/mapbox/streets-v11',
          center: [-84.39, 33.75], // Atlanta coordinates
          zoom: 11
        });

        map.current.on('load', () => {
          setLoading(false);
        });
      } catch (err) {
        console.error("Error initializing map:", err);
        setError("Failed to initialize map");
        setLoading(false);
      }
    }

    // Clean up function to remove map when component unmounts
    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  // Load data based on map type
  useEffect(() => {
    if (!map.current || loading) return;
    
    // Clear existing markers
    const existingMarkers = document.querySelectorAll('.mapboxgl-marker');
    existingMarkers.forEach(marker => marker.remove());
    
    const fetchData = async () => {
      try {
        if (type === 'bus') {
          const buses = await getBusPositions();
          
          // Add bus markers
          buses.forEach(bus => {
            if (!bus.position?.latitude || !bus.position?.longitude) return;
            
            // Create a custom marker element
            const markerEl = document.createElement('div');
            markerEl.className = 'bus-marker';
            markerEl.innerHTML = `
              <div class="bg-green-500 text-white p-2 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bus"><path d="M8 6v6"/><path d="M15 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4c-1.1 0-2.1.8-2.4 1.8L.2 13c-.1.4-.2.8-.2 1.2 0 .4.1.8.2 1.2.3 1.1.8 2.8.8 2.8h3"/><circle cx="7" cy="18" r="2"/><circle cx="15" cy="18" r="2"/></svg>
              </div>
            `;
            
            // Add popup with bus info
            const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(`
              <div>
                <h3 class="font-bold">Bus ${bus.vehicle?.label}</h3>
                <p>Route: ${bus.routeId || 'Unknown'}</p>
                ${bus.occupancyStatus ? `<p>Status: ${bus.occupancyStatus.replace(/_/g, ' ')}</p>` : ''}
              </div>
            `);
            
            // Add marker to map
            new mapboxgl.Marker(markerEl)
              .setLngLat([bus.position.longitude, bus.position.latitude])
              .setPopup(popup)
              .addTo(map.current!);
          });
        } else {
          const trains = await getTrainData();
          
          // Add train markers
          trains.forEach(train => {
            if (!train.LATITUDE || !train.LONGITUDE) return;
            
            // Create element for train marker
            const markerEl = document.createElement('div');
            markerEl.className = 'train-marker';
            
            // Color based on line
            let color = 'bg-purple-500';
            if (train.LINE === 'RED') color = 'bg-red-500';
            if (train.LINE === 'GOLD') color = 'bg-yellow-500';
            if (train.LINE === 'BLUE') color = 'bg-blue-500';
            if (train.LINE === 'GREEN') color = 'bg-green-500';
            
            markerEl.innerHTML = `
              <div class="${color} text-white p-2 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-train-front"><path d="M8 3.1V7a4 4 0 0 0 8 0V3.1"/><path d="m9 15-1-1"/><path d="m15 15 1-1"/><path d="M9 19c-2.8 0-5-2.2-5-5v-4a8 8 0 0 1 16 0v4c0 2.8-2.2 5-5 5Z"/><path d="m8 19-2 3"/><path d="m16 19 2 3"/></svg>
              </div>
            `;
            
            // Create popup with train info
            const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(`
              <div>
                <h3 class="font-bold">${train.LINE} Line Train</h3>
                <p>Train ID: ${train.TRAIN_ID}</p>
                <p>Direction: ${train.DIRECTION} to ${train.DESTINATION}</p>
                <p>Next Station: ${train.STATION}</p>
                <p>Arrival: ${train.NEXT_ARR} (${train.WAITING_TIME})</p>
              </div>
            `);
            
            // Add marker to map
            new mapboxgl.Marker(markerEl)
              .setLngLat([parseFloat(train.LONGITUDE), parseFloat(train.LATITUDE)])
              .setPopup(popup)
              .addTo(map.current!);
          });
        }
      } catch (err) {
        console.error('Error fetching data for map:', err);
        setError('Failed to load map data');
      }
    };
    
    fetchData();
    
    // Refresh data every 30 seconds
    const intervalId = setInterval(fetchData, 30000);
    return () => clearInterval(intervalId);
  }, [type, loading]);

  return (
    <div className="w-full h-full rounded-lg overflow-hidden bg-gray-100 relative">
      {/* Map container */}
      <div ref={mapContainer} className="absolute inset-0 w-full h-full" />
      
      {/* Static placeholder always visible during loading */}
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white">
          <div className="text-center">
            <div className={`text-4xl mb-4 ${type === 'bus' ? 'text-green-500' : 'text-purple-500'}`}>
              {type === 'bus' ? <Bus size={48} /> : <TrainFront size={48} />}
            </div>
            <p className="text-xl font-semibold">
              {type === 'bus' ? 'Bus Routes Map' : 'Train Lines Map'}
            </p>
            <p className="text-sm text-muted-foreground mt-2">
              Loading map data...
            </p>
          </div>
        </div>
      )}
      
      {/* Error state */}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-white">
          <div className="text-red-500 text-center">
            <p className="text-xl font-semibold">{error}</p>
            <p className="text-sm mt-2">Please try again later</p>
          </div>
        </div>
      )}
    </div>
  );
};
