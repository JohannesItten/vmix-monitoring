import {createStore} from 'vuex'

let vmixes = {}

const defaultClass = 'grey';
const redClass = 'red';
const greenClass = 'green';
const yellowClass = 'yellow';

function getGlobalPropClass(propState)
{
    return propState === 'True' ? redClass : defaultClass;
}

function getInfoCSSClass(verbosity)
{
    switch(verbosity)
    {
        case 'parsing':
        case 'error':
            return redClass;
        case 'warning':
            return yellowClass;
    }
    return null;
}

function processVmixErrors(state, vmixId, vmixErrors)
{
    for (let verbosity in vmixErrors)
    {
        let errors = vmixErrors[verbosity];
        if (errors.length === 0) continue;
        state.vmixes[vmixId].info = errors[0];
        state.vmixes[vmixId].infoCSSClass = getInfoCSSClass(verbosity);
        return;
    }

    state.vmixes[vmixId].info = null;
    state.vmixes[vmixId].infoCSSClass = defaultClass;
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
                'isOnline': false,
                'info': null,
                'infoCSSClass': null,
                'props':  vmix.view
            }
        }
    },
    monitorError(state, payload) {
        let vmixId = payload.vmixId;
        if (!state.vmixes.hasOwnProperty((vmixId))) return;
        let vmix = state.vmixes[vmixId];
        vmix.info = payload.error.text;
    },
    updateVmix (state, payload) {
        let vmixId = payload.vmixId;
        if (!state.vmixes.hasOwnProperty(vmixId)) return;
        processVmixErrors(state, vmixId, payload.errors)
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
                let cssClass = greenClass;
                if (buses[propKey].is_muted || volumeBar === 0)
                    cssClass = defaultClass;
                vmix.props[propKey].cssClass = cssClass;
                vmix.props[propKey].value = volumeBar;
                continue;
            }
            if (inputs.hasOwnProperty(propKey))
            {
                let volumeBar = Math.round(parseFloat(inputs[propKey].props.volume));
                let cssClass = greenClass;
                if (inputs[propKey].props.muted === 'True' || volumeBar === 0)
                    cssClass = defaultClass;
                vmix.props[propKey].cssClass = cssClass;
                vmix.props[propKey].value = volumeBar;
            }
        }
    }
  }
});

export default store;
