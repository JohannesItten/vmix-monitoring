const STATE_MAIN_ENABLED = "red", 
      STATE_MAIN_DISABLED = "grey",
      STATE_AUDIO_ENADLED = "green",
      STATE_AUDIO_DISABLED = "red",
      STATE_INFO = "grey"

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
        if (!msg.hasOwnProperty("state") || msg.state == null) { return; }
        processState(msg["id"], msg["state"]);
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
        default:
            enabledState = STATE_INFO;
            disabledState = STATE_INFO;
            break;
    }

    propertyElem.classList.remove("red", "grey", "green");
    propertyValue ? propertyElem.classList.add(enabledState) : propertyElem.classList.add(disabledState);
}

function processState(vmix_id, state)
{
    stateElement = document.getElementById(vmix_id);
    if (!stateElement) { return; }
    //update Online state
    onlineElem = stateElement.querySelector(".online");

    switchBooleanPropertyState(stateElement, "online", state.online);
    switchBooleanPropertyState(stateElement, "recording", state.recording);
    switchBooleanPropertyState(stateElement, "streaming", state.streaming);
    
    speakerElem = stateElement.querySelector(".speaker-name");
    if (state.speaker != null)
    {
        speakerElem.innerHTML = state.speaker;
    }
    else
    {
        speakerElem.innerHTML = "";
    }
     
}

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:9090/");
    initConnection(websocket);
    recieveMessage(websocket);
});