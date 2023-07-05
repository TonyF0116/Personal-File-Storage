import { createRouter, createWebHistory } from 'vue-router';
import AccountPage from '../components/AccountPage.vue';
import IndexPage from '../components/IndexPage.vue';
import EditPage from '../components/EditPage.vue';

const routes = [
    {
        path: '/',
        redirect: '/index'
    },
    {
        path: '/account',
        component: AccountPage
    },
    {
        path: '/index',
        component: IndexPage
    },
    {
        path: '/edit',
        component: EditPage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
