<script setup>
import { ref } from 'vue'
let isShowNav = ref(true)
const toggleNav = () => {
  isShowNav.value = !isShowNav.value
}
</script>
<template>
  <!-- <nav v-show="isShowNav">
    <a href="" @click.prevent="toggleNav">
      <i class="fa fa-times" aria-hidden="true"></i>
    </a>
    <RouterLink to="/grid">Grid</RouterLink>
    <RouterLink to="/control">Control</RouterLink>
  </nav> -->
  <RouterView></RouterView>
</template>
<style></style>
