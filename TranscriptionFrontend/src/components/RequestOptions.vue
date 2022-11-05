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
            this.$router.push('/request')
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
                "video_url": this.video_url
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
            if (this.transcriber_option == 'tmp3' || this.transcriber_option == 'tyt') {
                this.transcription_result = 'No request made yet.';
            }
        }
    }
}
</script>

<style scoped>
@import '../assets/RequestOptions.css';
</style>

<template>
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
</template>