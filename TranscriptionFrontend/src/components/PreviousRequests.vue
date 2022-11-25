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
       background-color: rgb(70, 68, 68); 
       padding: 10px;
       border-radius: 8px;
       margin: 10px 0px;
    }
    #element:hover {
        cursor:pointer;
    }
</style>

<template> 
    <!-- TODO: Add more personal request title information -->
    <div id="element" v-on:click="requestClicked">
        Request {{ requestNumber }}
    </div>
</template>