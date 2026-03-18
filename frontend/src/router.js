import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('./views/RegisterView.vue'),
    meta: { guest: true },
  },
  {
    path: '/shared/:token',
    name: 'SharedFile',
    component: () => import('./views/SharedFileView.vue'),
    meta: { public: true },
  },
  {
    path: '/shared-folder/:token',
    name: 'SharedFolder',
    component: () => import('./views/SharedFolderView.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('./components/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/drive',
      },
      {
        path: 'drive',
        name: 'Drive',
        component: () => import('./views/DriveView.vue'),
      },
      {
        path: 'drive/:folderId',
        name: 'Folder',
        component: () => import('./views/DriveView.vue'),
        props: true,
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('./views/DashboardView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.guest && token) {
    next('/drive')
  } else {
    next()
  }
})

export default router
