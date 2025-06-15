<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

// ✅ Fusion des deux interfaces dans un seul `defineProps`
const props = defineProps<{
  id: string;
  position: { x: number; y: number };
  nom: string;
  prenom: string;
  grade: string;
  unite: string;
}>()

const isHovered = ref(false)
const isDialogOpen = ref(false)

const formatCoordinates = (x: number, y: number) => {
  return `${x.toFixed(4)}, ${y.toFixed(4)}`
}
</script>


<template>
  <div class="relative group" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
    <Dialog>
      <DialogTrigger as-child>
        <div
          class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center shadow-lg cursor-pointer transform transition-transform duration-200 hover:scale-110"
          :class="{ 'ring-2 ring-blue-300': isHovered }">
          <img src="/helmet.png" class="w-6 h-6 " alt="Soldier" />
        </div>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Soldier Details</DialogTitle>
          <DialogDescription>
            Information about soldier {{ id }}
          </DialogDescription>
        </DialogHeader>
        <div class="grid gap-10 grid-cols-6  py-4">
          <!-- Left side (3 items) -->
          <div class="col-span-3 flex flex-col gap-4">
            <div class="flex items-center gap-2">
              <div class="font-medium w-20">Status</div>
              <span
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs bg-green-100 text-green-800 font-medium">
                Active
              </span>
            </div>
            <div class="flex items-center gap-2">
              <div class="font-medium w-20">Location</div>
              <span class="text-sm text-gray-600">
                {{ formatCoordinates(position.x, position.y) }}
              </span>
            </div>
            <!--<div class="flex items-center gap-2">
              <div class="font-medium w-20">Battery</div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div class="bg-blue-600 h-2.5 rounded-full" style="width: 85%"></div>
              </div>
            </div>-->
          </div>
          <!-- Right side (4 items) -->
          <div class="col-span-3 flex flex-col gap-4">
            <div class="flex items-center gap-2">
              <div class="font-medium w-20">Nom</div>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{nom}}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <div class="font-medium w-20">Prenom</div>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
               {{prenom}}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <div class="font-medium w-20">Grade</div>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{grade}}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <div class="font-medium w-20">Unite</div>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{unite}}
              </span>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  </div>
</template>

<style scoped>
.animate-ping {
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes ping {

  75%,
  100% {
    transform: scale(2);
    opacity: 0;
  }
}
</style>
