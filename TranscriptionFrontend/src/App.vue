
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
      <h1>👋 Welcome to Transcriber!</h1>
      <span class="queryBoxElements" id="description">
        Transcriber takes your YouTube URL and translates it using 
        <a href="https://google.com">OpenAI's Whisper</a>
        according to your specifications. Enjoy!
      </span>
      <div id="container">
        <router-view/>
      </div>
    </div>
  </main>
</template>
