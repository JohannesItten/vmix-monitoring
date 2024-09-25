<script setup>
  import '../assets/main.css'

  import store from '../store.js'
  import {computed, ref, onMounted} from 'vue'

  const vmixes = ref({});
  const criticalErrorMessage = ref(null);

  const isErrorDisplay = computed(() => {
    let cssDisplay = 'display: grid';
    if (criticalErrorMessage.value === null) cssDisplay = 'display: none';
    return cssDisplay
  });

  let urlParams = new URLSearchParams(document.location.search);
  const currentPage = urlParams.get('page');
  const startSocket = (wsURL, waitTimer, waitSeed, multiplier) => {
    let socket = new WebSocket(wsURL);

    socket.onopen = (event) => {
        criticalErrorMessage.value = null;
        socket.send(JSON.stringify(
          {type: 'watch', payload: {'page': currentPage}}
        ));
        waitTimer = waitSeed;
    };
    socket.onerror = (event) => {
      criticalErrorMessage.value = "Can't establish connection with WebSocket Server";
    }
    socket.onclose = (event) => {
      criticalErrorMessage.value = "Can't establish connection with WebSocket Server";
      if (waitTimer < 60000) waitTimer = waitTimer * multiplier;
      setTimeout(()=>{startSocket(socket.url, waitTimer, waitSeed, multiplier)}, waitTimer);
    }

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      switch (message.type)
      {
        case 'update':
          processMessage(message);
          break;
        case 'init':
          processInit(message);
          break;
        case 'error':
          processMonitorError(message);
          break;
      }
    };
  }

  let serverURI = 'ws://localhost:9090/ws';
  startSocket(serverURI, 1000, 1000, 2);
  // onMounted(() => {
  //   fetch('/defaults').then((response) => {
  //     if (response.ok)
  //     {
  //       return response.json();
  //     }
  //   }).then((json) => {
  //     let serverURI = json.server;
  //     startSocket(serverURI, 1000, 1000, 2);
  //   })
  // });

  const processInit = (message) => {
    store.commit('init', message.message);
    vmixes.value = message.message;
  };

  const processMessage = (message) => {
    let payload = {
      name: message.name,
      vmixId: message.id,
      isOnline: message.isOnline,
      snapshot: message.message,
      errors: message.errors
    };
    store.commit('updateVmix', payload);
  };

  const processMonitorError = (message) => {
    let payload = {
      vmixId: message.id,
      error: message.message
    };
    store.commit('monitorError', payload);
  }
</script>

<template>
  <div class='critical-error-message' :style = 'isErrorDisplay'>
    <i class='fa fa-info-circle' aria-hidden='true'></i>
    <p>{{ criticalErrorMessage }}</p>
  </div>
  <div class='multiview'>
    <vmix v-for='vmix in vmixes' :vmixId='vmix.id' :key='vmix.id'/>
  </div>
</template>

<style scoped>

</style>