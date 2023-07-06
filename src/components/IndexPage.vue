<template>
    <h1>Index Page</h1>
    <button @click="goToEditPage">Go To Edit Page</button>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000';


export default {
    data() {
        return {
        }
    },
    mounted() {
        axios.defaults.headers.common['Authorization'] = this.$route.query.Authorization
        this.initialize_index_page()
    },
    methods: {
        // Authorization Validation and get basic user information
        initialize_index_page() {
            axios.post('/api/index', {}
            ).then(response => {
                console.log(response)
                // this.userid = response.data.userid;
                // this.username = response.data['username'];
                // this.nickname = response.data['nickname'];
                // this.files = response.data['files'];
            }, error => {
                // error.
                console.log(error);
                if (error.response.status == 302 || error.response.status == 401) {
                    this.$router.push(error.response.data.data.redirection);
                }
            })
        },

        // Example for redirection using router
        goToEditPage() {
            this.$router.push({ path: '/edit', query: { Authorization: this.$route.query.Authorization } })
        },
    }
}
</script>

<style></style>