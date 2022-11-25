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
                    let statusInfo = json['progress']
                    if(statusInfo === 'done') {
                        this.status = '100%';
                    } else {
                        let percent = statusInfo['downloaded_bytes']/statusInfo['total_bytes'];
                        percent = Math.round(percent * 1000)/10;
                        this.status = percent + "%";
                    }
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
    created: function () {
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
#grid {
    display: grid;
    grid-template-columns: 65% 15% 15%;
    column-gap: 2.5%;
}

#grid>.section1>h2 {
    color:white;
    text-decoration: underline;
}

#grid>.section1, #grid>.section3>h2  {
    cursor: pointer;
}

#grid>.item>h2 {
    font-size: 15px;
    text-overflow: ellipsis;
    display:block;
}
#grid>.item>h3 {
    font-size: 13px;
    text-overflow: ellipsis;
}

#grid>.section3>h2 { 
    text-align: center;
}


#status {
    display:table;
    margin: 0 auto;
}
#status>h2 {
    display: inline-block;
    font-size: 15px;
}
#status>h3 {
    font-size: 13px;
    display:block;
}

</style>

<template>
    <div id="element">
        <div id="grid">
            <div class="item section1" v-on:click="requestClicked">
                <h2> {{ this.title }} </h2>
                <h3> Id: {{ requestNumber }} </h3>
                <h3> Info: {{ this.info }} </h3>
            </div>
            <div class="item section2">
                <div id="status">
                    <h2>Status:</h2>
                    <h3>{{ this.status }}</h3>
                </div>
            </div>

            <div class="item section3">
                <h2 v-on:click="updateInfo">Refresh</h2>
            </div>
        </div>

    </div>
</template>