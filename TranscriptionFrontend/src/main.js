import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'

import RequestOptions from './components/RequestOptions.vue'
import RequestResponse from './components/RequestResponse.vue'
import Error404 from './components/Error404.vue'

import './assets/main.css'

const routes = [
    { path: '/', component: RequestOptions },
    { path: '/request/:id', component: RequestResponse },
    {
        path: '/:catchAll(.*)',
        name: 'Error',
        component: Error404,
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

const app = createApp(App);

app.use(router)

app.mount("#app")

