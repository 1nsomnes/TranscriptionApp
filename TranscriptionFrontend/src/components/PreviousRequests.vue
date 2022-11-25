<script>
export default {
    props: ['requestNumber'],
    methods: {
        requestClicked() {
            this.$router.push('/request/' + this.requestNumber);
        }
    }
}
</script>

<style scoped>
    #element {
       background-color: gray; 
       color: white;
    }
    #element:hover {
        cursor:pointer;
    }
</style>

<template> 
    <div id="element" v-on:click="requestClicked">
        {{ requestNumber }}
    </div>
</template>