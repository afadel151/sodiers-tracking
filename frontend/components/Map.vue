<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Feature, Map, View } from 'ol'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'
import 'ol/ol.css'
import { Point } from 'ol/geom'
import { Overlay } from 'ol'
import AppSidebar from './AppSidebar.vue'
import Soldier from './Soldier.vue'
import { createApp } from 'vue'
import { info } from 'autoprefixer'
const center = ref([3.0588, 36.7538])
const projection = ref('EPSG:4326')
const randomName = () => {
  const noms = ['MIKAKDA', 'FADEL', 'HADAD', 'labdi', 'BATACHE']
  const prenoms = ['AISSA', 'ALI', 'RABEH', 'MOHAMED', 'ABDALLAH']
  const grades = ['COLONEL', 'COMMANDANT', 'Lieutenant', 'CAPITEN']
  const unites = ['ENPEI', 'DAT', 'TACTIQUE','SPACIAL_FORCE', 'AVIATION']
  const status= ['mort','vivant','vivant','vivant','mort']
  return {
    nom: noms[Math.floor(Math.random() * noms.length)],
    prenom: prenoms[Math.floor(Math.random() * prenoms.length)],
    grade: grades[Math.floor(Math.random() * grades.length)],
    unite: unites[Math.floor(Math.random() * unites.length)],
    status: status[Math.floor(Math.random() * status.length)],
  }
}

const zoom = ref(12)
const rotation = ref(0)
const map = ref(null)

const soldiers = ref([])
const soldierLayer = ref(null)
const movementInterval = ref(null)
const soldierOverlays = ref([])

const createSoldierOverlay = (coordinates,info,soldierId) => {
  const element = document.createElement('div');
  
  const soldierComponent = createApp(Soldier, {
  id:soldierId,
    position: { x: coordinates[0], y: coordinates[1] }, 
    nom: info.nom,
    prenom:info.prenom,
    grade: info.grade,
    unite: info.unite,
    status: info.status,
  });
  soldierComponent.mount(element);
  const overlay = new Overlay({
    element: element,
    position: coordinates,
    positioning: 'center-center'
  });
  
  return {
    overlay,
    component: soldierComponent,
    id: soldierId,
  };
};

const addRandomSoldier = () => {
  const algiersCenter = [3.0588, 36.7538];
  const radius = 0.01;
  const angle = Math.random() * 2 * Math.PI;
  const distance = Math.random() * radius;
  const x = algiersCenter[0] + distance * Math.cos(angle);
  const y = algiersCenter[1] + distance * Math.sin(angle);
 
  const info = randomName();
  const soldierId = `SOL-${soldiers.value.length + 1}`;
  const soldierOverlay = createSoldierOverlay([x, y], info, soldierId)
  map.value.addOverlay(soldierOverlay.overlay);
  soldierOverlays.value.push(soldierOverlay);
  const soldier = new Feature({
    geometry: new Point([x, y]),
    properties: {
      id: soldierOverlay.id,
      ...info
    }
  });
  
  soldiers.value.push(soldier);
};
 
const moveSoldier = (soldier) => {
  const algiersCenter = [3.0588, 36.7538];
  const currentCoords = soldier.getGeometry().getCoordinates();
  
  const distanceFromCenter = Math.sqrt(
    Math.pow(currentCoords[0] - algiersCenter[0], 2) +
    Math.pow(currentCoords[1] - algiersCenter[1], 2)
  );
  
  const movementRange = 0.0005;
  let newX = currentCoords[0] + (Math.random() - 0.5) * movementRange;
  let newY = currentCoords[1] + (Math.random() - 0.5) * movementRange;
  
  const newDistanceFromCenter = Math.sqrt(
    Math.pow(newX - algiersCenter[0], 2) +
    Math.pow(newY - algiersCenter[1], 2)
  );
  
  const maxDistance = 0.015;
  if (newDistanceFromCenter > maxDistance) {
    const angle = Math.atan2(
      algiersCenter[1] - currentCoords[1],
      algiersCenter[0] - currentCoords[0]
    );
    newX = currentCoords[0] + Math.cos(angle) * movementRange;
    newY = currentCoords[1] + Math.sin(angle) * movementRange;
  }
  
  const duration = 500;
  const startTime = Date.now();
  const startCoords = currentCoords;
  
  const animate = () => {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    const easedProgress = progress < 0.5
      ? 2 * progress * progress
      : 1 - Math.pow(-2 * progress + 2, 2) / 2;
    
    const currentX = startCoords[0] + (newX - startCoords[0]) * easedProgress;
    const currentY = startCoords[1] + (newY - startCoords[1]) * easedProgress;
    soldier.getGeometry().setCoordinates([currentX, currentY]);
    const overlay = soldierOverlays.value.find(o => o.id === soldier.get('properties').id);
    if (overlay) {
      overlay.overlay.setPosition([currentX, currentY]);
    }
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  };
  
  requestAnimationFrame(animate);
};

const startSoldierMovement = () => {
  if (movementInterval.value) {
    clearInterval(movementInterval.value);
  }
  
  movementInterval.value = setInterval(() => {
    soldiers.value.forEach(soldier => {
      moveSoldier(soldier);
    });
  }, 1000)
};

const stopSoldierMovement = () => {
  if (movementInterval.value) {
    clearInterval(movementInterval.value);
    movementInterval.value = null;
  }
};
//ajouter un soldat bouger dynamiquement 
const addRealSoldier = async () => {
  try {
    const gps = await $fetch('http://localhost:8000/api/last-gps') // adresse backend
    const x = parseFloat(gps.lon)
    const y = parseFloat(gps.lat)

    const soldierOverlay = createSoldierOverlay([x, y])
    map.value.addOverlay(soldierOverlay.overlay)
    soldierOverlays.value.push(soldierOverlay)

    const soldier = new Feature({
      geometry: new Point([x, y]),
      properties: {
        id: soldierOverlay.id,
        type: 'real',
        nom: 'Dakich',
        prenom: 'Zin',
        grade: 'comandant',
        unite: 'enpei',
        status:'vivant',
        position:{lat: y,  lon:x,},
      }
    })

    soldiers.value.push(soldier)
  } catch (error) {
    console.error('Erreur lors de la récupération de la position GPS :', error)
  }
}

onMounted(() => {
  map.value = new Map({
    target: 'map',
    layers: [
      new TileLayer({
        source: new OSM()
      })
    ],
    view: new View({
      center: center.value,
      projection: projection.value,
      zoom: zoom.value,
      rotation: rotation.value
    })
  });

  for (let i = 0; i < 5; i++) {
    addRandomSoldier();
  }
  
  startSoldierMovement();

  map.value.on("click", function (evt) {
    
  });
})

onUnmounted(() => {
  stopSoldierMovement();
  soldierOverlays.value.forEach(overlay => {
    overlay.component.unmount();
  });
  soldierOverlays.value = [];
});

</script>

<template>
  <SidebarProvider class="h-screen w-screen ">
    <AppSidebar class="absolute z-10" />
    <div id="map" class="h-screen relative w-full">
      <SidebarTrigger class="absolute top-2 left-10 z-10" />
      <div class="absolute bottom-4 right-4 flex gap-2 z-10">
        <button 
          @click="addRandomSoldier"
          class="bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-600 transition-colors"
        >
          Add Soldier
        </button>
        <button 
          @click="startSoldierMovement"
          class="bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-green-600 transition-colors"
        >
          Start Movement
        </button>
        <button 
          @click="stopSoldierMovement"
          class="bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-red-600 transition-colors"
        >
          Stop Movement
        </button>
        <button
          @click="addRealSoldier"
          class="bg-purple-500 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-purple-600 transition-colors"
          >
          Add Real Soldier
         </button>
    
      </div>
    </div>
  </SidebarProvider>
</template>
