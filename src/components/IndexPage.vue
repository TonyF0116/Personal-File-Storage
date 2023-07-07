<template>
    <div class="page_title">{{ page_title }}</div>
    <button @click="goToEditPage">Go To Edit Page</button>
    <h1>{{ account_id }}</h1>
    <ol v-for="file in files" :key="file">
        <li>{{ file[2] }}</li>
    </ol>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000';


export default {
    data() {
        return {
            page_title: 'Index Page',
            account_id: 0,
            name: "",
            administration: 0,
            avatar_suffix: "",
            files: null,

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
                this.account_id = response.data.data.user_info[0][0];
                this.name = response.data.data.user_info[0][2];
                if (this.name == null) {
                    response.data.data.user_info[0][1];
                }
                this.administration = response.data.data.user_info[0][3];
                this.avatar_suffix = response.data.data.user_info[0][4];
                this.files = response.data.data.user_files

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

<style>
.page_title {
    font-family: Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    font-size: xxx-large;
}
</style>