import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'

import RequestOptions from './components/RequestOptions.vue'
import RequestResponse from './components/RequestResponse.vue'

import './assets/main.css'

const routes = [
    { path: '/', component: RequestOptions },
    { path: '/request', component: RequestResponse }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

const app = createApp(App);
app.use(router)
app.mount("#app")

