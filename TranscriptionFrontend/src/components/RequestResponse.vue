<script>
export default {
    data() {
        return {
            requestProgress: '0',
            updateDownload: null
        }
    },
    created: function() {
        this.updateDownload = setInterval(() => {
            fetch('http://localhost:4999/rprogress/' + this.$route.params.id, {
                method: 'GET'
            }).then(res => {
                if(res.status == '500') {
                    clearInterval(updateDownload);
                    console.log("received error")
                }

                res.text().then(text => {
                    this.requestProgress = text;
                    if(this.requestProgress === '100') {
                        clearInterval(this.updateDownload)
                    }
                })
            })
        }, 1000);
    },
    beforeUnmount: function() {
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

    <p>Request Progress: {{ requestProgress }}%</p>

</template>