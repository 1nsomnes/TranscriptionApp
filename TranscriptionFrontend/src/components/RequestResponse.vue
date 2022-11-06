<script>
export default {
    computed: {
        requestProgress() {
            fetch('http://localhost:4999/rprogress', {
                method: 'GET'
            }).then(res => {
                res.text().then(text => {
                    return text;
                })
            })
        }
    }
}
</script>
<style scoped>
    @import '../assets/RequestOptions.css';
</style>


<template>
    <h2 style="color:white">Request #{{ $route.params.id }}</h2>
    
    <iframe width="640" height="480" src="https://www.youtube.com/embed/ekPT4ZXXGSM" 
    title="YouTube Speech Recognition Test - good audio" 
    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>

    <p>Request Progress: {{ requestProgress }}</p>

</template>