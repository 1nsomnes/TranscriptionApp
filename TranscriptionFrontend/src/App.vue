
<script src="./scripts/app.js">
  console.log("test");
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
        <select v-model="transcriber_option" v-on:change="updatedSelect" id="toptions">
          <option value="dyt">Download YouTube Video</option>
          <option value="tmp3">Transcribe From MP3</option>
          <option value="tyt">Transcribe From YouTube</option>
          <option value="tl">Live Transcription</option>
        </select>

        <input v-if="transcriber_option == 'dyt' || transcriber_option == 'tyt'" type="text" placeholder="YouTube Url"
          id="yturl" class="tinputs" v-model="video_url">

        <h2 v-if="transcriber_option == 'tl'" class="tinputs">Support for this feature doesn't exist yet...</h2>
        
        <div v-if="transcriber_option == 'tmp3' || transcriber_option == 'tyt'" id="result">
          <h2 class="tinputs">Result:</h2>
          <span id="resultSpan" class="tinputs">{{ transcription_result }}</span>
        </div>

        <button id="transcribe" class="tinputs" v-on:click="buttonClicked()">
          Transcribe
        </button>
      </div>
    </div>
  </main>
</template>
