
<script>
  import RequestOptions from './components/RequestOptions.vue'

  export default {
    components: {
      RequestOptions
    },
    methods: {
      titleClicked() {
        this.$router.push('/')
      }
    }
  }
</script>

<style scoped>
  @import './assets/app.css';
</style>

<template>
  <header>
  </header>

  <main>
    <div id="box">
      <h1 v-on:click="titleClicked">T R A N S C R I B E R</h1>
      <span class="queryBoxElements" id="description">
        Integration of
        <a href="https://google.com">OpenAI's Whisper</a>
        for transcription.
      </span>
      <hr>
      <div id="container">
        <!-- Reload component on router path changes -->
        <router-view :key="$route.fullPath"></router-view>
      </div>
    </div>
  </main>
</template>
