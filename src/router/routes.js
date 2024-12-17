// const routes = [{
//     path: '/',
//     component: () => import('layouts/MainLayout.vue'),
//     children: [
//       { path: '', component: () => import('pages/IndexPage.vue') }
//     ]
//   },
//   { path: '/about', component: () => import('pages/AboutPage.vue') },
//   // Always leave this as last one,
//   // but you can also remove it
//   {
//     path: '/:catchAll(.*)*',
//     component: () => import('pages/ErrorNotFound.vue')
//   }
// ]

// export default routes
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'), // Hlavní rozložení
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') } // Domovská stránka
    ]
  },

  // /aut/login
  {
    path: '/auth',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: 'login',
        component: () => import('pages/LoginPage.vue')
      },
      {
        path: 'signup',
        component: () => import('pages/SignUpPage.vue')
      }
    ]
  },
  // /try/try_without_registration
  {
    path: '/try',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: 'try_without_registration',
        component: () => import('pages/TryPage.vue')
      },
      {
        path: 'get_started',
        component: () => import('pages/GetStartedPage.vue')
      },
      {
        path: 'whisper',
        component: () => import('pages/WhisperPage.vue')
      },
      {
        path: 'TimeLineTest',
        component: () => import('pages/TimeLineTestPage.vue')
      },
      {
        path: 'demo_project',
        component: () => import('pages/DemoProjectPage.vue')
      }
    ]
  },

  // Chybová stránka pro neexistující cesty (volitelné)
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
