
import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

import App from './App.vue'
import {routes} from './routes.js'
import {store} from './store.js'


let router = new VueRouter({
	mode: 'history',
	routes
});

router.beforeEach((to, from, next) => {
	console.log(`From: ${from.path} to ${to.path}`);

	if(to.meta.private){
		if(store.getters.isAuth){
			next();
		}
	}

	if(to.name == 'home'){
		next({name:'login'});
	}else{
		next();
	}
});

/**		Modules		**/
new Vue({
	el: 'main',
	router,
	store,
	render: h => h(App)
});