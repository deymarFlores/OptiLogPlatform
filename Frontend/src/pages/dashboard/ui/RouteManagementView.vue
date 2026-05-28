<template>
  <div class="route-management-view">
    <RouteManager 
      :isConnectionModeActive="isConnectionModeActive"
      @close="handleClose"
      @toggle-connection-mode="handleToggleMode"
    />
  </div>
</template>

<script setup>
import { RouteManager } from '@/Features/map/ui';

defineProps({
  isConnectionModeActive: Boolean
});

const emit = defineEmits(['close', 'toggle-connection-mode']);

const handleClose = () => {
  emit('close');
};

const handleToggleMode = () => {
  emit('toggle-connection-mode');
};
</script>

<style scoped>
.route-management-view {
  width: 100%;
  height: 100%;
}
</style>
