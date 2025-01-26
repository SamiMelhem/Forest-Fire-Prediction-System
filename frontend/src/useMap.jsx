import { useRef, useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import axios from "axios";

import "mapbox-gl/dist/mapbox-gl.css";
import "./App.css";

const INITIAL_CENTER = [-118.24998, 34.05528];
const INITIAL_ZOOM = 8.5;
const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL;

export default function useMap() {
  const mapRef = useRef();
  const mapContainerRef = useRef();

  const [center, setCenter] = useState(INITIAL_CENTER);
  const [zoom, setZoom] = useState(INITIAL_ZOOM);

  useEffect(() => {
    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_API_KEY;
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current,
      center: center,
      zoom: zoom,
      style: "mapbox://styles/mapbox/light-v11",
    });

    mapRef.current.on("load", async () => {
      try {
        const wildfires = await axios.get(`${BACKEND_BASE_URL}/wildfires`);

        const names = new Set();
        const polygons = {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: [],
          },
          generateId: true,
        };

        for (const fire of wildfires.data) {
          const attr = fire.attributes;
          const name = attr.attr_IncidentName;
          const cause = attr.attr_FireCause;
          const desc = attr.attr_IncidentShortDescription;
          const percentContained = attr.attr_PercentContained;
          const rings = fire.geometry.rings;

          if (!names.has(name)) {
            const polygon = {
              type: "Feature",
              geometry: {
                type: "Polygon",
                coordinates: rings,
              },
              properties: {
                id: name,
                name: name,
                cause: cause,
                description: desc,
                percentContained: percentContained,
              },
            };
            polygons.data.features.push(polygon);
            names.add(name);
          }
        }

        mapRef.current.addSource("wildfires", polygons);
        mapRef.current.addLayer({
          id: "wildfires",
          type: "fill",
          source: "wildfires",
          layout: {},
          paint: {
            "fill-color": "orange",
            "fill-opacity": [
              "case",
              ["boolean", ["feature-state", "hover"], false],
              1,
              0.5,
            ],
          },
        });
      } catch (err) {
        console.error(err);
      }
    });
    mapRef.current.on("move", () => {
      const mapCenter = mapRef.current.getCenter();
      const mapZoom = mapRef.current.getZoom();

      setCenter([mapCenter.lng, mapCenter.lat]);
      setZoom(mapZoom);
    });

    return () => {
      mapRef.current.remove();
    };
  }, []);

  const handleFetchData = async () => {};

  const handleReset = () => {
    mapRef.current.flyTo({
      center: INITIAL_CENTER,
      zoom: INITIAL_ZOOM,
    });
  };

  return {
    mapContainerRef,
    center,
    zoom,
    handleFetchData,
    handleReset,
  };
}
