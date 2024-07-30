import { createStore } from 'vuex'

let vmixes = {}
for (let i=0; i<9; i++)
{
    vmixes[i] = {
        'name': null,
        'props': {
            recording: {
                text: 'RECORD',
                icon: 'fa fa-hdd-o',
                state: null,
                value: null,
                cssClass: 'grey'
              },
              streaming: {
                text: 'STREAM',
                icon: 'fa fa-youtube-play',
                state: null,
                value: null,
                cssClass: 'grey'
              },
              master: {
                text: 'M',
                icon: 'fa fa-bus',
                state: null,
                value: null,
                cssClass: 'grey'
              },
              busA: {
                text: 'A',
                icon: 'fa fa-bus',
                state: null,
                value: null,
                cssClass: 'grey'
              },
              audiokey: {
                text: 'AUDIO',
                icon: 'fa fa-volume-up',
                state: null,
                value: null,
                cssClass: 'grey'
              }
        },
        'info': [],
        'isOnline': true
    }
}

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
    updateProps (state, payload) {
        //TODO: check vmix id
        let vmixId = 0;
        let vmix = state.vmixes[vmixId];
        vmix.name = payload.name;
        
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
