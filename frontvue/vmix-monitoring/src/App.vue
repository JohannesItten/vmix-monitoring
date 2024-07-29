<template>
  <div class='multiview'>
    <div class='vmix' v-for='i in 9'>
      <div class='top-bar'>
        <div class='info'>
          <i class='fa fa-info' aria-hidden='true'></i>
          <span class='info-value'>Какая-то инфа</span>
        </div>
        <div class='name'>
          <span class='name-value'>Большой</span>
        </div>
      </div>
      <div class='main-space'></div>
      <div class='low-bar'>
        <div class='state recording red' data-type='global'>
          <div>
            <i class='fa fa-hdd-o' aria-hidden='true'></i>
          </div>
          <div>
            <span class='state-name'>RECORD</span>
          </div>
          <div>
            <span class='state-value'></span>
          </div>
        </div>
        <div class='state red' data-type='global'>
          <div>
            <i class='fa fa-youtube-play' aria-hidden='true'></i>
          </div>
          <div>
            <span class='state-name'>STREAM</span>
          </div>
          <div>
            <span class='state-value'></span>
          </div>
        </div>
        <div class='state red' data-type='audio'>
          <div>
            <i class='fa fa-power-off' aria-hidden='true'></i>
          </div>
          <div>
            <span class='state-name'>ON AIR</span>
          </div>
          <div>
            <span class='state-value'></span>
          </div>
        </div>
        <div class='state green' data-type='audio'>
          <div>
            <i class='fa fa-bus' aria-hidden='true'></i>
          </div>
          <div>
            <span class='state-name'>M</span>
          </div>
          <div>
            <span class='state-value'>100</span>
          </div>
        </div>
        <div class='state green' data-type='audio'>
          <div>
            <i class='fa fa-hdd-o' aria-hidden='true'></i>
          </div>
          <div>
            <span class='state-name'>AUDIO</span>
          </div>
          <div>
            <span class='state-value'>100</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  // const resolution = [
  //   [1920, 1080],
  //   [2560, 1440],
  //   [3840, 2160]
  // ];
  // const maxPerLine = 4;
  // const maxPerColumn = 4;
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
    processMessage(message);
  };

  const processMessage = (message) => {
    if (!message.hasOwnProperty('message')) return;
    let vmix_response = JSON.parse(message['message']);
    let global = vmix_response.global;
    let isStreaming = global.streaming.value;
    console.log('IsStreaming: ' + isStreaming);
  };
</script>
<style>
  html
  {
    font-family: 'Open Sans', sans-serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
    font-variation-settings: 'wdth' 100;
    font-size: 0.85em;
  }
  body
  {
      width: 1920px;
      height: 1080px;
      min-width: 1920px;
      min-height: 1080px;
      max-width: 1920px;
      max-height: 1080px;
      margin: 0;
      padding: 0;
  }
  .multiview
  {
    display: grid;
    grid-template-columns: repeat(3, auto);
    grid-template-rows: repeat(3, auto);
  }
  .vmix
  {
    background-color: rgba(51,51,51,0.9);
    min-width: 640px;
    min-height: 360px;
    max-width: 640px;
    max-height: 360px;
    box-shadow: 0 0 0 1px white inset;

    display: grid;
    grid-template-rows: 9% auto 9%; 
  }

  .top-bar
  {
    display: inline-grid;
    grid-template-columns: 70% 30%;
    column-gap: 1%;
    margin-top: 0.5%;
    margin-left: 1%;
    margin-right: 2%;
  }

  .top-bar div
  {
    border-radius: 7px;
  }

  .top-bar .info
  {
    background-color: #CCCCCC;
    display: flex;
    align-items: center;
  }

  .top-bar .info i
  {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 8%;
  }

  .top-bar .info span
  {
    width: 80%;
  }

  .top-bar .name
  {
    background-color: #999999;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .low-bar
  {
    display: inline-grid;
    grid-template-columns: repeat(5, auto); /* auto-fil auto-fit */
    column-gap: 0.8%;
    margin-bottom: 0.5%;
    margin-left: 1%;
    margin-right: 1%;
  }

  .low-bar .state
  
  {
    border-radius: 7px;
    display: inline-grid;
    grid-template-columns: 25% 40% auto;
  }

  .low-bar .state div
  {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: nowrap;
  }

  .red
  {
    background-color: #FF3333 !important;
  }

  .green
  {
    background-color: #00CC33 !important;
  }

  .grey
  {
    background-color: #999999;
  }

</style>