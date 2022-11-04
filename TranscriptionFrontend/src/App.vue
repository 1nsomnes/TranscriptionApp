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
      translation_option: "null",
      transcriber_option: "dyt"
    }
  },
  methods: {
    buttonClicked() {
      switch (this.transcriber_option) {
        case 'tyt':
          this.getTranscriptionYt();
          break;
        case 'dyt':
          this.downloadYt();
          break;
        default:
          console.log('other called');
          break;
      }
    },

    getTranscriptionYt() {
      let data = {
        "video_url": this.video_url,
        "translate": this.translation_option
      }

      this.transcription_result = "Processing..."

      fetch("http://localhost:4999/transcribeyt", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(res => {
        res.json().then((json_obj) => {
          this.transcription_result = json_obj['whisper-response']
        })
      }).catch(e => {
        this.transcription_result = "Error communicating with api: " + e;
      })
    },

    downloadYt() {
      let data = {
        "video_url" : this.video_url
      }

      fetch("http://localhost:4999/downloadyt", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(res => {
        
        res.blob().then((blob) => {
          // answer from stackoverflow :/
          // https://stackoverflow.com/questions/32545632/how-can-i-download-a-file-using-window-fetch 

          var url = window.URL.createObjectURL(blob);
          var a = document.createElement('a');
          a.href = url;
          a.download = "result.mp4";
          document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
          a.click();    
          a.remove();  //afterwards we remove the element again
        })
      }).catch(e => {
        this.transcription_result = "Error communicating with api: " + e;
      })
    },

    updatedSelect() {
      if(this.transcriber_option == 'tmp3' || this.transcriber_option == 'tyt') {
        this.transcription_result = 'No request made yet.';
      }
    }
  }
}
</script>

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

<style scoped>
section {
  height: 100%;
}

#box {
  width: 70vw;
  margin: 0 auto;
  display: block;
}

#box>h1 {
  text-align: center;
  color: white;
  font-size: 30px;
}

#container {
  border-radius: 10px;
  padding: 20px 10px;
  margin-top: 20px;
  background-color: #393E46;
}
#container>h2 { 
  color: white; 
  font-size: 20px;
}

#toptions {
  display: block;
  padding: 8px 10px;
  background-color: #EEEEEE;
  border-radius: 10px;
  margin: 0px 10px 20px 10px;
}

#transcribe {
  background-color: #00ADB5;
  border-color: #00ADB5;
  display: block;
  margin-top: 20px;
}

#yturl {
  width: calc(100% - 10px);
  padding: 7px 14px;
  border-radius: 10px;
}

#result>h2 {
  margin-bottom: 0px;
  color: white;
}
#result>span {
  background-color:beige;
  border-radius: 8px;
  padding: 5px 10px;
  color: black;
  border-style:inset;
  border-width: 1.5px;
  display: block;
}

.tinputs {
  margin: 10px;
}
</style>
