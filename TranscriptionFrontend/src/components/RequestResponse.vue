<script>
export default {
    data() {
        return {
            requestProgress: '0',
            updateDownload: null,
            requestDone: false
        }
    },
    methods: {
        downloadClicked() {
            fetch('http://localhost:4999/rdownload/' + this.$route.params.id, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Access-Control-Expose-Headers': 'Content-Disposition'
                }
            }).then(res => {
                if (res.status == '500') { }

                let disposition = res.headers.get("Content-Disposition")
                disposition = disposition.split('filename=')[1].split(';')[0];
                disposition = disposition.replaceAll('"','')

                console.log(disposition)

                res.blob().then((blob) => {
                    // answer from stackoverflow :/
                    // https://stackoverflow.com/questions/32545632/how-can-i-download-a-file-using-window-fetch 
                    var url = window.URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = disposition;
                    document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
                    a.click();
                    a.remove();  //afterwards we remove the element again
                })
            })
        }
    },
    created: function () {
        this.updateDownload = setInterval(() => {
            fetch('http://localhost:4999/rprogress/' + this.$route.params.id, {
                method: 'GET'
            }).then(res => {
                if (res.status == '500') {
                    clearInterval(updateDownload);
                    console.log("received error")
                }

                res.text().then(text => {
                    this.requestProgress = text;
                    if (this.requestProgress === 'done') {
                        clearInterval(this.updateDownload)
                        this.requestDone = true
                    }
                })
            }).catch(e => {
                clearInterval(this.updateDownload)
            })
        }, 1000);
    },
    beforeUnmount: function () {
        clearInterval(this.updateDownload);
    }
}
</script>
<style scoped>
@import '../assets/RequestOptions.css';
</style>


<template>
    <h2 style="color:white">Request #{{ $route.params.id }}</h2>

    <iframe width="640" height="480" src="https://www.youtube.com/embed/ekPT4ZXXGSM"
        title="YouTube Speech Recognition Test - good audio" frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe>

    <p>Request Progress: {{ requestProgress }}</p>

    <input v-if="requestDone == true" v-on:click="downloadClicked()" type="button" value="Download">

</template>