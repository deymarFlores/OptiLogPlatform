<template>
  <div class="map-container">
    <div ref="mapContainer" class="map-view"></div>
    <canvas
      v-if="isConnecting"
      ref="dynamicLineCanvas"
      class="dynamic-line-canvas"
    ></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from "vue";
import L from "leaflet";

const props = defineProps({
  isConnectionModeActive: Boolean,
  locationTypes: {
    type: Array,
    default: () => [],
  },
});

const mapContainer = ref(null);
const dynamicLineCanvas = ref(null);
let map = null;
let markersLayer = null;
let routesLayer = null;
let pointsMarkersMap = new Map();

const emit = defineEmits(["map-click", "route-created", "route-started"]);

const isConnecting = ref(false);
const selectedPointId = ref(null);
const selectedPointCoords = ref(null);
let mousePos = { x: 0, y: 0 };

watch(isConnecting, (newVal) => {
  if (newVal) {
    nextTick(() => {
      updateCanvasSize();
    });
  }
});

const defineExpose = (obj) => {
  Object.assign(mapContainer.value, obj);
};

onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      initializeMap();
    }, 100);
  });
});

const initializeMap = () => {
  if (!mapContainer.value) return;

  map = L.map(mapContainer.value, {
    preferCanvas: true,
    attributionControl: true,
    zoomControl: true,
  }).setView([-16.5, -68.15], 13);

  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    {
      maxZoom: 19,
      maxNativeZoom: 18,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/">CARTO</a>',
      className: "map-tiles",
      crossOrigin: true,
      errorTileUrl:
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
    },
  ).addTo(map);

  markersLayer = L.layerGroup().addTo(map);
  routesLayer = L.layerGroup().addTo(map);

  map.on("click", (e) => {
    if (!isConnecting.value) {
      emit("map-click", e.latlng);
    }
  });

  const mapElement = map.getContainer();
  mapElement.addEventListener("mousemove", (e) => {
    if (isConnecting.value) {
      const rect = mapElement.getBoundingClientRect();
      mousePos.x = e.clientX - rect.left;
      mousePos.y = e.clientY - rect.top;
      drawDynamicLine();
    }
  });

  mapElement.addEventListener("mouseleave", () => {});

  window.addEventListener("resize", updateCanvasSize);

  map.invalidateSize();
  map.getContainer().style.borderRadius = "12px";
  map.getContainer().style.overflow = "hidden";

  updateCanvasSize();
};

const updateCanvasSize = () => {
  if (dynamicLineCanvas.value && mapContainer.value) {
    dynamicLineCanvas.value.width = mapContainer.value.offsetWidth;
    dynamicLineCanvas.value.height = mapContainer.value.offsetHeight;
  }
};

const addMarker = (point) => {
  const popupContent = `
    <div class="custom-popup">
      <p><strong>${point.typeName}</strong></p>
      <p>${point.name}</p>
      <p style="font-size: 0.75rem; color: #a0abb9;">${point.lat.toFixed(4)}, ${point.lng.toFixed(4)}</p>
    </div>
  `;

  const iconElement = document.createElement("div");
  iconElement.className = "custom-marker";
  iconElement.style.backgroundColor = point.color;
  iconElement.innerHTML = `<i class="fas ${point.icon}"></i>`;

  const customIcon = L.divIcon({
    html: iconElement.outerHTML,
    className: "custom-div-icon",
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -30],
  });

  const marker = L.marker([point.lat, point.lng], { icon: customIcon })
    .bindPopup(popupContent)
    .addTo(markersLayer);

  marker.on("click", (e) => {
    e.originalEvent.stopPropagation();

    if (isConnecting.value && selectedPointId.value !== point.id) {
      console.log("Conexión completada:", selectedPointId.value, "→", point.id);
      emit("route-created", {
        fromPointId: selectedPointId.value,
        toPointId: point.id,
      });
      cancelConnectionMode();
    } else if (!isConnecting.value && props.isConnectionModeActive) {
      startConnectionMode(point.id, point);
    }
  });

  pointsMarkersMap.set(point.id, marker);
};

const addSucursalMarker = (sucursal) => {
  if (!map || !markersLayer) {
    console.warn(" Mapa no inicializado aún. Sucursal en queue:", sucursal.name);
    return;
  }

  console.log(" addSucursalMarker llamado con:", sucursal);
  console.log(" type_location_id buscando:", sucursal.type_location_id);
  console.log(" locationTypes disponibles:", props.locationTypes);

  if (props.locationTypes && props.locationTypes.length > 0) {
    console.log(
      " IDs disponibles en locationTypes:",
      props.locationTypes.map((t) => t.id),
    );
  }

  const locationType = props.locationTypes.find(
    (t) => t.id === sucursal.type_location_id,
  );

  console.log(" locationType encontrado:", locationType);

  if (!locationType) {
    console.warn("Tipo de ubicación no encontrado:", sucursal.type_location_id);
    console.warn(
      "IDs disponibles:",
      props.locationTypes.map((t) => t.id),
    );
    return;
  }

  const customIcon = L.divIcon({
    html: `
      <div style="position: relative; display: flex; flex-direction: column; align-items: center;">
        <!-- Etiqueta flotante sobre el icono -->
        <div style="
          background: #1e293b;
          color: #94a3b8;
          font-size: 8px;
          font-weight: 600;
          padding: 3px 8px;
          border-radius: 12px;
          letter-spacing: 0.5px;
          white-space: nowrap;
          margin-bottom: 4px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
          border: 1px solid #334155;
        ">
          <i class="fas fa-building" style="font-size: 7px; margin-right: 3px;"></i>
          SUCURSAL
        </div>
        <!-- Icono principal -->
        <div style="
          background: ${locationType.color || "#475569"};
          width: 38px;
          height: 38px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 16px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
          border: 2px solid white;
          transition: transform 0.2s ease;
        ">
          <i class="fas ${locationType.icon || "fa-warehouse"}"></i>
        </div>
      </div>
    `,
    className: "sucursal-div-icon",
    iconSize: [38, 58],
    iconAnchor: [19, 50],
    popupAnchor: [0, -50],
  });

  const popupContent = `
    <div style="font-family: 'Segoe UI', sans-serif; min-width: 180px;">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px solid #e0e0e0;">
        <i class="fas ${locationType.icon || "fa-warehouse"}" style="color: ${locationType.color || "#475569"}; font-size: 18px;"></i>
        <strong style="color: #333; font-size: 14px;">${sucursal.name}</strong>
      </div>
      <div style="margin-bottom: 4px;">
        <span style="color: #666; font-size: 11px;">📋 Tipo:</span>
        <span style="color: #333; font-size: 11px; font-weight: 500;"> ${locationType.name}</span>
      </div>
      <div>
        <span style="color: #666; font-size: 11px;"> Ubicación:</span>
        <span style="color: #999; font-size: 10px;"> ${sucursal.lat.toFixed(4)}, ${sucursal.lng.toFixed(4)}</span>
      </div>
    </div>
  `;

  const marker = L.marker([sucursal.lat, sucursal.lng], { icon: customIcon })
    .bindPopup(popupContent, {
      maxWidth: 260,
      minWidth: 200,
      className: "sucursal-popup",
    })
    .addTo(markersLayer);

  marker.on("mouseover", function () {
    const iconDiv = this._icon?.querySelector("div:last-child");
    if (iconDiv) {
      iconDiv.style.transform = "scale(1.1)";
      iconDiv.style.transition = "transform 0.2s ease";
    }
  });

  marker.on("mouseout", function () {
    const iconDiv = this._icon?.querySelector("div:last-child");
    if (iconDiv) {
      iconDiv.style.transform = "scale(1)";
    }
  });

  marker.on("click", (e) => {
    e.originalEvent.stopPropagation();

    if (isConnecting.value && selectedPointId.value !== sucursal.id) {
      emit("route-created", {
        fromPointId: selectedPointId.value,
        toPointId: sucursal.id,
      });
      cancelConnectionMode();
    } else if (!isConnecting.value && props.isConnectionModeActive) {
      startConnectionMode(sucursal.id, {
        id: sucursal.id,
        name: sucursal.name,
        lat: sucursal.lat,
        lng: sucursal.lng,
        typeName: locationType.name,
        icon: locationType.icon,
        color: locationType.color,
      });
    }
  });

  pointsMarkersMap.set(sucursal.id, marker);
};

const drawRoute = (fromPoint, toPoint, color = "#1e4a6e", weight = 2) => {
  const polyline = L.polyline(
    [
      [fromPoint.lat, fromPoint.lng],
      [toPoint.lat, toPoint.lng],
    ],
    {
      color: color,
      weight: weight,
      opacity: 0.7,
      dashArray: "5, 5",
      className: "route-line",
    },
  ).addTo(routesLayer);

  return polyline;
};

const drawDynamicLine = () => {
  if (!dynamicLineCanvas.value || !selectedPointCoords.value) {
    return;
  }

  const canvas = dynamicLineCanvas.value;
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#d4a373";
  ctx.lineWidth = 2;
  ctx.setLineDash([5, 5]);
  ctx.globalAlpha = 0.6;

  ctx.beginPath();
  ctx.moveTo(selectedPointCoords.value.x, selectedPointCoords.value.y);
  ctx.lineTo(mousePos.x, mousePos.y);
  ctx.stroke();

  ctx.globalAlpha = 1;
  ctx.setLineDash([]);
};

const startConnectionMode = (pointId, point) => {
  console.log("Conexión iniciada desde:", point.name);
  isConnecting.value = true;
  selectedPointId.value = pointId;

  const marker = pointsMarkersMap.get(pointId);
  if (marker) {
    const latLng = marker.getLatLng();
    const point_px = map.latLngToContainerPoint(latLng);
    selectedPointCoords.value = {
      x: point_px.x,
      y: point_px.y,
    };
  }

  emit("route-started", { pointId, point });
};

const cancelConnectionMode = () => {
  console.log("Cancelando modo conexión");
  isConnecting.value = false;
  selectedPointId.value = null;
  selectedPointCoords.value = null;
  if (dynamicLineCanvas.value) {
    const ctx = dynamicLineCanvas.value.getContext("2d");
    ctx.clearRect(
      0,
      0,
      dynamicLineCanvas.value.width,
      dynamicLineCanvas.value.height,
    );
  }
};

const clearMarkers = () => {
  if (markersLayer) {
    markersLayer.clearLayers();
  }
  pointsMarkersMap.clear();
};

const clearRoutes = () => {
  if (routesLayer) {
    routesLayer.clearLayers();
  }
};

const getMapInstance = () => map;

defineExpose({
  addMarker,
  addSucursalMarker,
  clearMarkers,
  drawRoute,
  clearRoutes,
  startConnectionMode,
  cancelConnectionMode,
  isConnecting,
  getMapInstance,
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  position: relative;
  flex: 1;
}

.map-view {
  height: 100%;
  width: 100%;
}

.dynamic-line-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: crosshair;
  z-index: 999;
  pointer-events: none; /* No capturar eventos del mouse - solo dibujar */
}
</style>

<style>
.custom-popup {
  background: rgba(255, 255, 255, 0.98);
  border: 2px solid #d4a373;
  border-radius: 8px;
  color: #1e4a6e;
  font-size: 0.9rem;
  padding: 0.75rem;
  font-family: inherit;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.custom-popup p {
  margin: 0.25rem 0;
}

.custom-popup strong {
  color: #d4a373;
  font-weight: 700;
}

.custom-marker {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
  border: 3px solid rgba(255, 255, 255, 0.8);
  font-weight: bold;
}

.custom-div-icon {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.route-line {
  opacity: 0.7;
}

.leaflet-container {
  background: #eef2f9;
  font-family: "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
}

.leaflet-control-attribution {
  background: rgba(255, 255, 255, 0.9) !important;
  color: #5f7d95 !important;
  font-size: 0.75rem;
}

.leaflet-control-attribution a {
  color: #1e4a6e !important;
}

.leaflet-control-zoom {
  border: 1px solid #d9d9d9 !important;
  border-radius: 4px !important;
  background: white !important;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1) !important;
}

.leaflet-control-zoom-in,
.leaflet-control-zoom-out {
  background: white !important;
  color: #1e4a6e !important;
  font-size: 1.2rem !important;
  width: 36px !important;
  height: 36px !important;
  line-height: 36px !important;
  border: none !important;
  font-weight: bold !important;
  text-align: center !important;
}

.leaflet-control-zoom-in:hover,
.leaflet-control-zoom-out:hover {
  background: #f5f5f5 !important;
  color: #d4a373 !important;
}

.leaflet-popup-content-wrapper {
  border-radius: 8px !important;
}

.leaflet-popup-tip {
  background: rgba(255, 255, 255, 0.98) !important;
}

.leaflet-pane {
  z-index: auto;
}

.leaflet-overlay-pane {
  z-index: 400;
}

.leaflet-shadow-pane {
  z-index: 500;
}

.leaflet-marker-pane {
  z-index: 600;
}

.leaflet-popup-pane {
  z-index: 700;
}

.leaflet-tooltip-pane {
  z-index: 800;
}
</style>
