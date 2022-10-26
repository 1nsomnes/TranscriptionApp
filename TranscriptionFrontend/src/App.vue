<script setup>
//import HelloWorld from './components/HelloWorld.vue'
//import TheWelcome from './components/TheWelcome.vue'
</script>

<script>


export default {
  data() {
    return {
      transcription_result: "No request made yet.",
      video_url: "",
      translation_option: "null"
    }
  },
  methods: {
    getTranscription() {
      let data = {
        "video_url" : this.video_url
      }
      
      console.log("Translation Request:" + this.translation_option)
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
    <div class="queryBox">
      <h1 class="queryBoxElements">👋 Welcome to Transcriber!</h1>
      <span class="queryBoxElements" id="description">
        Transcriber takes your YouTube URL and translates it using 
        <a href="https://google.com">OpenAI's Whisper</a>
        according to your specifications. Enjoy!</span>
      <input class="queryBoxElements" type="url" v-model="video_url" placeholder="YouTube URL" id="youtube-url">
      <select class="queryBoxElements" id="tranlateOptions" v-model="translation_option">
        <option value="null">No Translation</option>
        <option value="en">English</option>
        <option value="fr">French</option>
      </select>
      <button class="queryBoxElements" v-on:click="getTranscription">Transcribe</button>
      <span id="result" class="queryBoxElements">{{ transcription_result }}</span>
    </div>
  </main>
</template>

<style scoped>

#result {
  display: block;
  background-color:beige;
  border-radius: 8px;
  padding: 5px 10px;
  color: black;
  border-style:inset;
  border-width: 1.5px;
}
input {
  display: block;
  width:fit-content;
}
button {
  display: block;
}

/* Top Text */
h1 {
  color: white;
  font-size: 40px;
  text-align: center;
}
#description {
  display: block;
  font-size: 20px;
}

.queryBoxElements  {
  margin: 15px 10px;
}
</style>
