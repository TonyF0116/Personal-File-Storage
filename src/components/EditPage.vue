<template>
    <div class="page_title">{{ page_title }}</div>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000';

export default {
    data() {
        return {
            page_title: 'Edit Page',
        }
    },
    mounted() {
        axios.defaults.headers.common['Authorization'] = this.$route.query.Authorization
        this.initialize_edit_page()
    },
    methods: {
        // Authorization Validation
        initialize_edit_page() {
            axios.post('/api/edit', {}
            ).then(response => {
                console.log(response)
            }, error => {
                console.log(error);
                if (error.response.status == 302 || error.response.status == 401) {
                    this.$router.push(error.response.data.data.redirection);
                }
            })
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