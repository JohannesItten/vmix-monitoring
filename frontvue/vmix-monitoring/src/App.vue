<template>
  <div class='multiview'>
    <vmix v-for='vmix in vmixes' :vmixId='vmix.id' :key='vmix.id'/>
  </div>
</template>
<script setup>
  import store from './store'
  import { ref } from 'vue'

  const vmixes = ref({})

  const socket = new WebSocket('ws://localhost:9090');
  socket.onopen = (event) => {
    console.log('Connection opened');
    socket.send(JSON.stringify(
      {type: 'watch'}
    ));
  };
  socket.onclose = (event) => {
    console.log('Connection closed');
  };
  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === 'update')
    {
      processMessage(message);
      return;
    }
    if (message.type === 'init')
    {
      processInit(message);
    }
  };

  const processInit = (message) => {
    store.commit('init', message.message);
    vmixes.value = message.message;
  };

  const processMessage = (message) => {
    let payload = {name: message.name, 
                  vmixId: message.id,
                  isOnline: message.isOnline,
                  snapshot: message.message};
    store.commit('updateProps', payload);
  };
</script>
<style>
</style>