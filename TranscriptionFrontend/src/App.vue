<script setup>
//import HelloWorld from './components/HelloWorld.vue'
//import TheWelcome from './components/TheWelcome.vue'
</script>

<script>


export default {
  data() {
    return {
      greeting: "Hello",
      transcription_result: "No request made yet.",
      video_url: ""
    }
  },
  methods: {
    getTranscription() {
      let data = {
        "video_url" : this.video_url
      }

      this.transcription_result = "Processing..."

      fetch("http://localhost:4999/transcribe", {
        method:'POST',
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
      }).then(res => {
        res.json().then((json_obj) =>{
          this.transcription_result = json_obj['whisper-response']
        })
      }).catch(e => {
        console.log("BIG error lol: " + e)
      })
     
    }
  }
}
</script>

<template>
  <header>
  </header>

  
  <main>
    <h1>{{ greeting }} from Transcriber</h1>
    <span>{{ transcription_result }}</span>
    <input type="url" v-model="video_url" placeholder="YouTube URL" id="youtube-url">
    <button v-on:click="getTranscription">Transcribe</button>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
