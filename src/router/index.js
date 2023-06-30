import { createRouter, createWebHistory } from 'vue-router';
import AccountPage from '../components/AccountPage.vue';
import IndexPage from '../components/IndexPage.vue';
import EditPage from '../components/EditPage.vue';

const routes = [
    {
        path: '/',
        redirect: '/Index'
    },
    {
        path: '/Account',
        component: AccountPage
    },
    {
        path: '/Index',
        component: IndexPage
    },
    {
        path: '/Edit',
        component: EditPage
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
