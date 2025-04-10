import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import { createMemoryHistory, createRouter } from 'vue-router'
import VmixComponent from '@/components/Vmix.vue'
import GridComponent from '@/components/Grid.vue'
import ControlComponent from '@/components/Control.vue'

const routes = [
  { path: '/', component: GridComponent },
  { path: '/grid', component: GridComponent },
  { path: '/control', component: ControlComponent }
]

const router = createRouter({
  history: createMemoryHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.use(store)
app.component('Vmix', VmixComponent)
app.mount('#app')
