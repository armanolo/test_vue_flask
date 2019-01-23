import Login from './components/Login.vue'
import Home from './components/Home.vue'
import Nav from './components/Nav.vue'

import {store} from './store.js'

export const routes = [
	{
		path:'/', 
		name:'home', 
		component: Home,
		children: [
			{
				path:'login/',
				name:'login',
				components:
				{
					default: Nav,
					second: Login
				},
				props: { default: true, second: true }
			}
		]
	},
	{ path: '*', redirect:{name:'login'} }
]
