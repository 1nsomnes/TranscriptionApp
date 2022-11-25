<script>
import PreviousRequests from './PreviousRequests.vue'

export default {
    data() {
        return {
            video_url: "",
            ytformat: "mp3",
            translation_option: "null",
            transcriber_option: "dyt",
            request_error: "",
            request_list: []
        }
    },
    created: function() {
        if (this.$cookies.keys().includes('requests')) {
            //TODO: check if keys still exist 

            let json_obj = this.$cookies.get('requests')
            this.request_list = json_obj['value']
        }
    },
    methods: {
        setCookies(request_value) {
            if (!this.$cookies.keys().includes('requests')) {
                this.$cookies.set('requests', JSON.stringify(
                    {
                        "value" : [request_value]
                    }),     
                    '30d');
            } else {
                let json_obj = this.$cookies.get('requests');
                let request_array = Array.from(json_obj['value']);
                request_array.push(request_value);
                json_obj['value'] = request_array;
                this.$cookies.set('requests', JSON.stringify(json_obj), '30d');
            }
        }, 
        buttonClicked() {
            this.request_error = '';
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

            fetch("http://localhost:4999/transcribeyt", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(res => {
                if(res.status === 500) {
                    res.text().then(text => {
                        this.request_error = "Error: " + text;
                    });
                    return;
                }

                res.json().then((json) => {
                    // set cookies 
                    this.setCookies(json['request-number'])
                    this.$router.push('/request/' + json['request-number'])
                })
            }).catch(e => {
                this.request_error = e;
            })
        },

        downloadYt() {
            let data = {
                "video_url": this.video_url,
                "format": this.ytformat
            }

            fetch("http://localhost:4999/downloadyt", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(res => {
                if(res.status === 500) {
                    res.text().then(text => {
                        this.request_error = "Error: " + text;
                    });
                    return;
                }
                
                res.json().then(json => {
                    this.setCookies(json['request-number']);
                    this.$router.push('/request/' + json['request-number']);
                })
            }).catch(e => {
                this.request_error = "ERROR:" + e;
            })
        }
    }, 
    components: {
      PreviousRequests
    }
}
</script>

<style scoped>
@import '../assets/RequestOptions.css';
</style>

<template>
    <select v-model="transcriber_option" id="toptions">
        <option value="dyt">Download YouTube Video</option>
        <option value="tfile">Transcribe From File</option>
        <option value="tyt">Transcribe From YouTube</option>
        <option value="tl">Live Transcription</option>
    </select>

    <input v-model="ytformat" v-if="transcriber_option == 'dyt'" id="ytformat1" class="ytformat" type="radio" name="ytformat" value="mp3" checked>
    <label v-if="transcriber_option == 'dyt'" for="ytformat1">MP3</label>
    <input v-model="ytformat" v-if="transcriber_option == 'dyt'" id="ytformat2" class="ytformat" type="radio" name="ytformat" value="mp4"> 
    <label v-if="transcriber_option == 'dyt'" for="ytformat2">MP4</label>


    <input v-if="transcriber_option == 'dyt' || transcriber_option == 'tyt'" type="text" placeholder="YouTube Url"
        id="yturl" class="tinputs" v-model="video_url">

    <h3 v-if="request_error != ''" class="tinputs">{{ request_error }}</h3>
    
    <h2 v-if="transcriber_option == 'tl'" class="tinputs">Support for this feature doesn't exist yet...</h2>

    <button id="transcribe" class="tinputs" v-on:click="buttonClicked()">
        Transcribe ➔
    </button>

    <div id="prevreqs">
        <h1 style="color:white;">Previous Requests</h1>
        <PreviousRequests v-for="req in this.request_list" :requestNumber="req"></PreviousRequests>
        <h3 v-if="this.request_list.length == 0">No requests have been made yet... Make one above!</h3>
    </div>
</template>