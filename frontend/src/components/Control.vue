<script setup>
  import {onMounted, ref} from 'vue';
  let wsState = ref(false);
  let monState = ref(false);
  let isRestartBtnDisabled = ref(false);

  let apiBaseURI = 'http://localhost:8000/api';
  const getStateRequest = '/service/state';
  const restartAllRequest = '/service/restart';

  const getServiceState = (() => {
    fetch(apiBaseURI + getStateRequest)
        .then((response) => {
          if (response.ok)
            return response.json();
        })
        .then((json) => {
          wsState.value = json.ws;
          monState.value = json.monitor;
        })
  });

  const getLogs = (() => {
    console.log('logs');
  });

  const restartAllServices = (() => {
    isRestartBtnDisabled.value = true;
    fetch(apiBaseURI + restartAllRequest)
        .then((response) => {
          if (response.ok)
            return response.json();
          else
            isRestartBtnDisabled.value = false;
        })
        .then((json) => {
          let isError = json.isError;
          console.log(isError);
          isRestartBtnDisabled.value = false;
        })
  });

  const update = (() => {
    getServiceState();
    getLogs();
  });


  onMounted(() => {
    update();
    setInterval(update, 5000);
  });
</script>
<template>
  <div class='service grey'>
    <div class='service-state'>
      <i class='fa fa-circle' :class='[wsState ? "color-green" : "color-red"]' aria-hidden='true'></i><span>Websocket Server&nbsp</span>
    </div>
    <div class='service-state'>
      <i class='fa fa-circle' :class='[monState ? "color-green" : "color-red"]' aria-hidden='true'></i><span>Monitor Server&nbsp</span>
    </div>
    <div class='service-control'>
      <button @click='restartAllServices' :disabled='isRestartBtnDisabled'>Restart All</button>
    </div>
  </div>
  <div class='logs grey'>
    <div class='logs-text'>
      Some logs
    </div>
  </div>
</template>
<style>
  .service
  {
    margin: 2% 5%;
    height: 20%;
    width: 90%;

    border-radius: 7px;
    font-size: large;
    font-weight: normal;
  }

  .service .service-state
  {
    padding: 0.2% 1%;
  }

  .service-state span
  {
    display: inline-block;
  }
  .service-state i
  {
    padding: 0 0.5%;
  }

  .service-control
  {
    padding: 0.2% 1%;
  }

  .service-control button
  {
    height: 30px;
    font-size: large;
    font-weight: normal;
  }

  .logs
  {
    height: 80%;
    width: 90%;
    margin: 0 5%;
    border-radius: 7px;
  }

  .logs .logs-text
  {
    min-height: 600px;
    padding: 1% 1%;
  }

  .color-green
  {
    color: #00CC33 !important;
  }

  .color-red
  {
    color: #FF3333 !important;
  }
</style>