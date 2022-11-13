
<script>
  import RequestOptions from './components/RequestOptions.vue'

  export default {
    components: {
      RequestOptions
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
      <h1>T R A N S C R I B E R</h1>
      <span class="queryBoxElements" id="description">
        Integration of
        <a href="https://google.com">OpenAI's Whisper</a>
        for transcription.
      </span>
      <span style="color:white; font-weight: bold;">-</span>
      <div id="container">
        <router-view/>
      </div>
    </div>
  </main>
</template>
