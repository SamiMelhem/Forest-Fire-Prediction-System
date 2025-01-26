import useMap from "./useMap";
import { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL;

function App() {
  const { mapContainerRef, center, zoom, handleReset } =
    useMap();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `${BASE_URL}/recommendations?time_to_fire=${10}`
        );
        setRecommendations(response.data.recommendations);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <>
      <div className="sidebar">
        Longitude: {center[0].toFixed(4)} | Latitude: {center[1].toFixed(4)} |
        Zoom: {zoom.toFixed(2)}
      </div>
      <div className="w-[440px] min-h-[500px] absolute top-[55px] left-[12px] z-10 bg-white rounded-md py-3 px-4 shadow-xl">
        <h1 className="text-2xl mb-3">Wildfire Precautions</h1>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <ul className="list-disc ml-4">
            {recommendations.map((rec) => (
              <li key={rec}>{rec}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="flex gap-2 absolute top-[570px] left-[12px] z-10">
        <button
          className="bg-white rounded-md px-4 py-1 shadow-lg hover:cursor-pointer"
          onClick={handleReset}
        >
          Reset
        </button>
      </div>
      <div id="map-container" ref={mapContainerRef} />
    </>
  );
}

export default App;
