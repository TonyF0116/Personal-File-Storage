<template>
    <h1>Index Page</h1>
    <button @click="goToEditPage">Go To Edit Page</button>
</template>

<script>
export default {
    methods: {
        // Example for redirection using router
        goToEditPage() {
            this.$router.push('/edit');
        }
    }
}
</script>

<style></style>