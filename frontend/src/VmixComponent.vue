<script setup>
  defineProps({
    vmixId: String
  })
</script>
<template>
  <div class='vmix' :data-id='[vmixId]'>
        <div class='top-bar'>
          <div class='info' :class='[$store.state.vmixes[vmixId].infoCSSClass]'>
            <div><i class='fa fa-info' aria-hidden='true'></i></div>
            <div><span class='info-value'>{{ $store.state.vmixes[vmixId].info }}</span></div>
          </div>
          <div class='name' :class='{ red: $store.state.vmixes[vmixId].isOnline }'>
              <span class='name-value'>{{ $store.state.vmixes[vmixId].name }}</span>
          </div>
        </div>
      <div class='main-space'></div>
      <div class='low-bar'>
        <div v-for='(prop, propId) in $store.state.vmixes[vmixId].props' class='state' :class=[prop.cssClass]>
            <div>
                <i :class='[ prop.icon ]' aria-hidden='true'></i>
            </div>
            <div>
                <span class='state-name'>{{ prop.text }}</span>
            </div>
            <div>
                <span class='state-value'>{{ prop.value }}</span>
            </div>
        </div>
      </div>
  </div> 
</template>
<script>
</script>
<style>
</style>