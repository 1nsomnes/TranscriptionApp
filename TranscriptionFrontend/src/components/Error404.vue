<script>
export default {
    methods: {
        homeClicked() {
            this.$router.push('/')
        }
    }
}
</script>

<style scoped>
    h1,h3 {
        text-align: center;
    }
    h1 {
        color:white;
        font-size: 32px;
    }
    a {
        text-decoration: underline;
    }
    a:hover {
        cursor: pointer;
    }
</style>

<template> 
<h1>Error 404</h1>
<h3>The page you have requested does not exist...
    <a v-on:click="homeClicked">Return home</a>
</h3>
</template>