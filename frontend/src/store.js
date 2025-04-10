import { createStore } from 'vuex'

let vmixes = {}

const defaultClass = 'grey'
const redClass = 'red'
const greenClass = 'green'
const yellowClass = 'yellow'

function getGlobalPropClass(propState) {
  return propState === 'True' ? redClass : defaultClass
}

function getInfoCSSClass(level) {
  switch (level) {
    case 100:
    case 3:
      return redClass
    case 2:
      return yellowClass
    case 1:
    default:
      return defaultClass
  }
}

function processVmixErrors(state, vmixId, vmixErrors) {
  if (!Array.isArray(vmixErrors) || vmixErrors.length === 0) {
    state.vmixes[vmixId].info = ''
    state.vmixes[vmixId].infoCSSClass = defaultClass
    return
  }
  let vmixError = vmixErrors[0]
  state.vmixes[vmixId].info = vmixError['description']
  state.vmixes[vmixId].infoCSSClass = getInfoCSSClass(vmixError['level'])
}

const store = createStore({
  state() {
    return {
      vmixes
    }
  },
  mutations: {
    init(state, payload) {
      for (const index in payload) {
        let vmix = payload[index]
        state.vmixes[vmix.id] = {
          name: vmix.name,
          isOnline: false,
          info: null,
          infoCSSClass: null,
          props: vmix.view
        }
      }
    },
    monitorError(state, payload) {
      let vmixId = payload.vmixId
      if (!state.vmixes.hasOwnProperty(vmixId)) return
      let vmix = state.vmixes[vmixId]
      vmix.info = payload.error.text
      vmix.infoCSSClass = redClass
    },
    updateVmix(state, payload) {
      let vmixId = payload.vmixId
      if (!state.vmixes.hasOwnProperty(vmixId)) return
      processVmixErrors(state, vmixId, payload.errors)
      let vmix = state.vmixes[vmixId]
      vmix.name = payload.name
      vmix.isOnline = payload.isOnline

      let global = payload.snapshot.global
      let buses = payload.snapshot.buses
      let inputs = payload.snapshot.inputs
      console.log(payload.snapshot.outputs)
      for (const propKey in vmix.props) {
        if (global.hasOwnProperty(propKey)) {
          vmix.props[propKey].cssClass = getGlobalPropClass(global[propKey].value)
          continue
        }
        if (buses.hasOwnProperty(propKey)) {
          let volumeBar = Math.round(parseFloat(buses[propKey].volume_bar))
          let dbfsLeft = Math.round(parseFloat(buses[propKey].dbfs[0]))
          dbfsLeft = dbfsLeft > -100 ? dbfsLeft : '-inf'
          let cssClass = greenClass
          if (buses[propKey].is_muted || volumeBar === 0) cssClass = defaultClass
          vmix.props[propKey].cssClass = cssClass
          vmix.props[propKey].value = dbfsLeft
          continue
        }
        if (inputs.hasOwnProperty(propKey)) {
          let volumeBar = Math.round(parseFloat(inputs[propKey].props.volume))
          let dbfsLeft = Math.round(parseFloat(inputs[propKey].dbfs[0]))
          dbfsLeft = dbfsLeft > -100 ? dbfsLeft : '-inf'
          let cssClass = greenClass
          if (inputs[propKey].props.muted === 'True' || volumeBar === 0) cssClass = defaultClass
          vmix.props[propKey].cssClass = cssClass
          vmix.props[propKey].value = dbfsLeft
        }
      }
    }
  }
})

export default store
