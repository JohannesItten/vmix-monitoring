//
// It's a complete shit, but i need to sleep.
// Anyway in stable branch it has been rewritten with Svelte
// and normal state machine
//

const STATE_MAIN_ENABLED = "red", 
      STATE_MAIN_DISABLED = "grey",
      STATE_AUDIO_ENADLED = "green",
      STATE_AUDIO_DISABLED = "red",
      STATE_INFO = "grey",
      STATE_ERROR = "red";

const MODE_CONSTRUCTION = "DEV",
      MODE_PRODUCTION  = "PROD";

const CURRENT_MODE = MODE_CONSTRUCTION;

const COLOR_CLASSES = ["red", "grey", "green"]

function initConnection(websocket)
{
    websocket.addEventListener("open", () => {
        let event = { type: "watch" };
        websocket.send(JSON.stringify(event));
    });
}

function recieveMessage(websocket)
{
    websocket.addEventListener("message", ({ data }) => {
        msg = JSON.parse(data);
        if (msg.hasOwnProperty("init"))
        {
            processInitResponse(msg["init"]);
            return;
        }
        if (!msg.hasOwnProperty("state")) { return; }
        if (!msg.state)
        {
            processError(msg["id"], msg["state"], msg["reason"]);
            return;
        }
        processState(msg["id"], msg["state"]);
        processError(msg["id"], msg["state"], state["reason"]);
    });
}

function processInitResponse(msg)
{
    Object.keys(msg).forEach(id => {
        state = JSON.parse(msg[id]);
        processState(id, state["state"]);
        processError(id, state["state"], state["reason"]);
    });
}

function switchBooleanPropertyState(stateElem, propertyClass, propertyValue, type = "main")
{
    propertyElem = stateElem.querySelector("." + propertyClass);
    if (propertyElem == null) { return; }

    switch (type) {
        case "main":
            enabledState = STATE_MAIN_ENABLED;
            disabledState = STATE_MAIN_DISABLED;
            break;
        case "audio":
            enabledState = STATE_AUDIO_ENADLED;
            disabledState = STATE_AUDIO_DISABLED;
            break;
        default:
            enabledState = STATE_INFO;
            disabledState = STATE_INFO;
            break;
    }

    propertyElem.classList.remove("red", "grey", "green");
    propertyValue ? propertyElem.classList.add(enabledState) : propertyElem.classList.add(disabledState);
}

function switchElemColorState(elem, state)
{
    elem.classList.remove("red", "grey", "green");
    elem.classList.add(state);
}

function updateVolume(stateElem, propertyClass, volume)
{
    propertyElem = stateElem.querySelector("." + propertyClass);
    if (propertyElem == null) { return; }

    volElem = propertyElem.querySelector(".volume");
    if (volElem == null) { return; }
    volElem.innerHTML = volume;
}

function processError(vmix_id, state, reason)
{
    stateElement = document.getElementById(vmix_id);
    if (!stateElement) { return; }

    errorElement = stateElement.querySelector(".error");
    errorDescElement = stateElement.querySelector(".error-description");
    if (!errorElement || !errorDescElement) { return; }

    if (state == null)
    {
        errorDescElement.innerHTML = reason;
        switchElemColorState(errorElement, STATE_ERROR);
        return;
    }

    let errors = []
    //Process preset parse errors
    Object.keys(state.parse_error).forEach(key => {
        if (!state.parse_error[key]){
            errors.push({"level": 1, "reason": key});
        }
    });

    //Process stream/rec/in air errors
    if (state.online)
    {
        if (!state.recording) { errors.push({"level": 2, "reason": "Запись!"}); }
        if (!state.streaming) { errors.push({"level": 2, "reason": "Стрим!"}); }
        if (!state.master.state) { errors.push({"level": 2, "reason": "МАСТЕР!!!"}); }
    }
    
    maxErrorLevel = 0;
    mainReason = "";

    errors.forEach(err => {
        if (err.level > maxErrorLevel)
        {
            maxErrorLevel = err.level;
            mainReason = err.reason;
        }
        else if (err.level == maxErrorLevel)
        {
           mainReason += " " + err.reason; 
        }
    });
    
    errorDescElement.innerHTML = mainReason;
    switch(maxErrorLevel)
    {
        case 0:
        case 1:
            switchElemColorState(errorElement, STATE_INFO);
            break;
        default:
            switchElemColorState(errorElement, STATE_ERROR);
    }
}

function processState(vmix_id, state)
{
    if (!state) { return; }
    
    stateElement = document.getElementById(vmix_id);
    if (!stateElement) { return; }
    //update Online state
    onlineElem = stateElement.querySelector(".online");

    switchBooleanPropertyState(stateElement, "online", state.online);
    switchBooleanPropertyState(stateElement, "recording", state.recording);
    switchBooleanPropertyState(stateElement, "streaming", state.streaming);
    
    //process audio
    switchBooleanPropertyState(stateElement, "master", state.master.state, "audio");
    switchBooleanPropertyState(stateElement, "busA", state.busA.state, "audio");
    switchBooleanPropertyState(stateElement, "audio", state.audio.state, "audio");
    switchBooleanPropertyState(stateElement, "zoom", state.audio_zoom.state, "audio");
    updateVolume(stateElement, "master", state.master.volume);
    updateVolume(stateElement, "busA", state.busA.volume);
    updateVolume(stateElement, "audio", state.audio.volume);
    updateVolume(stateElement, "zoom", state.audio_zoom.volume);

    speakerElem = stateElement.querySelector(".speaker-name");
    
    if (state.speaker != null)
    {
        speakerElem.innerHTML = state.speaker;
    }
    else
    {
        speakerElem.innerHTML = "?";
    }
}

window.addEventListener("DOMContentLoaded", () => {
    let server_ip = document.getElementById("server_address").value
    const websocket = new WebSocket("ws://" + server_ip + ":9090/");
    initConnection(websocket);
    recieveMessage(websocket);
});
