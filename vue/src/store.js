import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export const store = new Vuex.Store({
	state: {
		auth:false,
		pathApi: 'http://localhost:5000'
	},
	getters: { 
		isAuth: (state)=>state.auth,
		getApiLogin: (state)=>state.pathApi+'/auth'
	},
	mutations: { 
		modifyAuth: (state,isAuth) =>{
			state.auth = isAuth;
		}
	},
	actions: { 
		addAuth: ({commit},product)=>{
			commit('modifyAuth',true);
		},
		removeAuth: (context,product)=>{
			context.commit('modifyAuth',false);
		}
	},
});
