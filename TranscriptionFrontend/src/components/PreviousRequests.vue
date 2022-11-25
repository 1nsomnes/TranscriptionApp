<script>
export default {
    props: ['requestNumber'],
    methods: {
        requestClicked() {
            this.$router.push('/request/' + this.requestNumber);
        },
        updateInfo() {
            fetch('http://localhost:4999/rinfo/' + this.requestNumber, {
                method: 'GET'
            }).then(res => {
                if (res.status == '500') {
                    console.log("received error")
                }

                res.json().then(json => {
                    this.title = json['title']
                    this.info = json['data']
                    this.status = json['progress']
                })
            })
        }
    }, 
    data() {
        return {
            title: "Unloaded title...",
            info: "Unloaded info...",
            status: "Unloaded status..."
        }
    },
    created: function() {
        this.updateInfo();
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
        {{ this.title}}
        Id: {{ requestNumber }}
        Info: {{ this.info }}
        Status: {{ this.status }}
    </div>
</template>