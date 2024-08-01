<template>
  <div class='critical-error-message' :style = 'isErrorDisplay'>
    <i class='fa fa-info-circle' aria-hidden='true'></i>
    <p>{{ criticalErrorMessage }}</p>
  </div>
  <div class='multiview'>
    <vmix v-for='vmix in vmixes' :vmixId='vmix.id' :key='vmix.id'/>
  </div>
</template>
<script setup>
import store from './store'
import {computed, ref} from 'vue'

// TODO: get currentPage from GET, serverURI from config
  const vmixes = ref({});
  const criticalErrorMessage = ref(null);
  const serverURI = 'ws://localhost:9090'; 

  const isErrorDisplay = computed(() => {
    let cssDisplay = 'display: grid';
    if (criticalErrorMessage.value === null) cssDisplay = 'display: none';
    return cssDisplay
  });

  const getURLPage = () => {
    let urlParams = new URLSearchParams(document.location.search);
    return urlParams.get('page');
  }

  const currentPage = getURLPage();

  const socket = new WebSocket(serverURI);
  socket.onopen = (event) => {
    criticalErrorMessage.value = null;
    console.log('Connection opened');
    socket.send(JSON.stringify(
      {type: 'watch', payload: {'page': currentPage}}
    ));
  };
  socket.onerror = (event) => {
    criticalErrorMessage.value = "Can't establish connection with WebSocket Server";
    console.log('Connection error: ', event);
  };
  socket.onclose = (event) => {
    criticalErrorMessage.value = "Can't connect to WebSocket Server";
    console.log('Connection closed');
  };
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
<style>
</style>

<!-- //wsURL - the string URL of the websocket
//waitTimer - the incrementing clock to use if no connection made
//waitSeed - used to reset the waitTimer back to default on a successful connection
//multiplier - how quickly you want the timer to grow on each unsuccessful connection attempt

const openSocket = (wsURL, waitTimer, waitSeed, multiplier) =>{
  let ws = new WebSocket(wsURL);
  console.log(`trying to connect to: ${ws.url}`);

  ws.onopen = () => {
      console.log(`connection open to: ${ws.url}`);
      waitTimer = waitSeed; //reset the waitTimer if the connection is made
      
      ws.onclose = () => {
        console.log(`connection closed to: ${ws.url}`);
        openSocket(ws.url, waitTimer, waitSeed, multiplier);
      };
      
      ws.onmessage = (message) => {
        //do something with messge...
      };
  };
  
  ws.onerror = () => {
    //increaese the wait timer if not connected, but stop at a max of 2n-1 the check time
    if(waitTimer < 60000) waitTimer = waitTimer * multiplier; 
    console.log(`error opening connection ${ws.url}, next attemp in : ${waitTimer/1000} seconds`);
    setTimeout(()=>{openSocket(ws.url, waitTimer, waitSeed, multiplier)}, waitTimer);
  }
}

openSocket(`ws://localhost:3000`, 1000, 1000, 2 -->