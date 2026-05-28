<template>
  <div class="setup-layout">
    <SetupNavbar />
    <CompanySetup />
  </div>
</template>

<script setup>
import SetupNavbar from './SetupNavbar.vue';
import CompanySetup from '../CompanySetup.page.vue';
</script>

<style scoped>
.setup-layout {
  width: 100%;
  min-height: 100vh;
}
</style>
