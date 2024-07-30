import { createStore } from 'vuex'

let vmixes = {}

const defaultClass = 'grey';
const activeGlobalClass = 'red';
const activeAudioClass = 'green';

function getGlobalPropClass(propState, isAudio = false)
{
    let propClass = propState === 'True' ? activeGlobalClass : defaultClass;
    return propClass;
}

const store = createStore({
  state () {
    return {
      vmixes
    }
  },
  mutations: {
    init (state, payload) {
        for (const index in payload)
        {
            let vmix = payload[index];
            state.vmixes[vmix.id] = {
                'name': vmix.name,
                'info': [],
                'isOnline': false,
                'props':  vmix.view
            }
        }
    },
    updateProps (state, payload) {
        let vmixId = payload.vmixId;
        if (!state.vmixes.hasOwnProperty(vmixId)) return;
        let vmix = state.vmixes[vmixId];
        vmix.name = payload.name;
        vmix.isOnline = payload.isOnline;
        
        let global = payload.snapshot.global;
        let buses = payload.snapshot.buses;
        let inputs = payload.snapshot.inputs;
        
        for (const propKey in vmix.props)
        {
            if (global.hasOwnProperty(propKey))
            {
                vmix.props[propKey].cssClass = getGlobalPropClass(global[propKey].value);
                continue;
            }
            if (buses.hasOwnProperty(propKey))
            {
                let volumeBar = Math.round(parseFloat(buses[propKey].volume_bar));
                let cssClass = activeAudioClass;
                if (buses[propKey].is_muted || volumeBar == 0)
                    cssClass = defaultClass;
                vmix.props[propKey].cssClass = cssClass;
                vmix.props[propKey].value = volumeBar;
                continue;
            }
            if (inputs.hasOwnProperty(propKey))
            {
                let volumeBar = Math.round(parseFloat(inputs[propKey].props.volume));
                let cssClass = activeAudioClass;
                if (inputs[propKey].props.muted === 'True' || volumeBar == 0)
                    cssClass = defaultClass;
                vmix.props[propKey].cssClass = cssClass;
                vmix.props[propKey].value = volumeBar;
                continue;
            }
        }
    }
  }
});

export default store;
