import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import VmixComponent from './VmixComponent.vue'

const app = createApp(App)
app.use(store)
app.component('Vmix', VmixComponent)
app.mount('#app')