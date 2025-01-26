import useMap from "./useMap";

function App() {
  const { mapContainerRef, center, zoom, handleReset, handleFetchData } =
    useMap();

  return (
    <>
      <div className="sidebar">
        Longitude: {center[0].toFixed(4)} | Latitude: {center[1].toFixed(4)} |
        Zoom: {zoom.toFixed(2)}
      </div>
      <div className="w-[440px] min-h-[600px] absolute top-[55px] left-[12px] z-10 bg-white/80 rounded-md p-2 shadow-lg bg-opac">
        Hello World!
      </div>
      <div className="flex gap-2 absolute top-[670px] left-[12px] z-10">
        <button
          className="bg-white rounded-md px-4 py-1 shadow-lg hover:cursor-pointer"
          onClick={handleReset}
        >
          Reset
        </button>
        <button
          className="bg-white rounded-md px-4 py-1 shadow-lg hover:cursor-pointer"
          onClick={handleFetchData}
        >
          Get Data
        </button>
      </div>
      <div id="map-container" ref={mapContainerRef} />
    </>
  );
}

export default App;
