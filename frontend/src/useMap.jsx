import { useRef, useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import axios from "axios";

import "mapbox-gl/dist/mapbox-gl.css";
import "./App.css";

const INITIAL_CENTER = [-118.24998, 34.05528];
const INITIAL_ZOOM = 8.5;
const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL;

const getDayColor = (day) => {
  switch (day) {
    case 0:
      return "red";
    case 1:
      return "green";
    case 2:
      return "orange";
    case 3:
      return "blue";
  }
};

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
      // Add starting point
      mapRef.current.loadImage(
        "https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png",
        (error, image) => {
          if (error) throw error;
          mapRef.current.addImage("custom-marker", image);

          mapRef.current.addSource("points", {
            type: "geojson",
            data: {
              type: "FeatureCollection",
              features: [
                {
                  type: "Feature",
                  geometry: {
                    type: "Point",
                    coordinates: INITIAL_CENTER,
                  },
                  properties: {
                    title: "Your Location",
                  },
                },
                {
                  type: "Feature",
                  geometry: {
                    type: "Point",
                    coordinates: [-122.414, 37.776],
                  },
                  properties: {
                    title: "Mapbox SF",
                  },
                },
              ],
            },
          });

          mapRef.current.addLayer({
            id: "points",
            type: "symbol",
            source: "points",
            layout: {
              "icon-image": "custom-marker",
              "text-field": ["get", "title"],
              "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
              "text-offset": [0, 1.25],
              "text-anchor": "top",
            },
          });
        }
      );

      try {
        const wildfires = await axios.get(`${BACKEND_BASE_URL}/wildfires`);

        for (let day = 0; day < 3; ++day) {
          const currDayFires = wildfires.data[day]["features"];
          const names = new Set();
          const polygons = {
            type: "geojson",
            data: {
              type: "FeatureCollection",
              features: [],
            },
            generateId: true,
          };

          for (const fire of currDayFires) {
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

          const layerName = `wildfires_day_${day}`;
          mapRef.current.addSource(layerName, polygons);
          mapRef.current.addLayer({
            id: layerName,
            type: "fill",
            source: layerName,
            layout: {},
            paint: {
              "fill-color": getDayColor(day),
              "fill-opacity": [
                "case",
                ["boolean", ["feature-state", "hover"], false],
                1,
                0.2,
              ],
            },
          });
        }
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

  const handleFetchData = async () => {
    // try {
    //   const prediction = await axios.get(`${BACKEND_BASE_URL}/predict`);
    //   const polygon = {
    //     type: "geojson",
    //     data: {
    //       type: "Feature",
    //       geometry: {
    //         type: "Polygon",
    //         coordinates: prediction.data
    //       }
    //     },
    //     generateId: true,
    //   };
    //   console.log(polygon);
    //   mapRef.current.addSource("prediction", polygon);
    //   mapRef.current.addLayer({
    //     id: "prediction",
    //     type: "fill",
    //     source: "prediction",
    //     layout: {},
    //     paint: {
    //       "fill-color": "orange",
    //       "fill-opacity": [
    //         "case",
    //         ["boolean", ["feature-state", "hover"], false],
    //         1,
    //         0.5,
    //       ],
    //     },
    //   });
    // } catch (err) {
    //   console.error(err);
    // }
  };

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
