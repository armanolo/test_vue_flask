<template>
	<div class="modal">
		<p v-if="$route.query.redirect">
			Anda no seas listo y logeate.
		</p>
		<form @submit.prevent="login" >
			<div class="imgcontainer">
				<img alt="Avatar" class="avatar" src="src/layout/images/img_avatar2.png">
			</div>
			<div class="container">
				<div class='block'>
					<label class='labelStyle' for="email">Email<span>*</span></label>
					<input id="email" v-model.trim="form.email" placeholder="Email o Usuario" required>
				</div>

				<div class='block'>
					<label class='labelStyle' for="password">Constraseña <span>*</span></label>
					<input id="password" v-model="form.password" placeholder="Constraseña" required>
				</div>

				<div>
					<button class="btn" type="submit">Entrar</button>
				</div>
				<p v-if="error" class="error">
					Bad login information
				</p>
			</div>
			<footer>
				<p>Esta pagina web es una prueba.
					<i style="font-size: 0.7em;margin-left: 1.5em;"><b>Estas de acuerdo</b></i>
					<input type="checkbox" id="idBox" style="display: inline !important;width: inherit;margin-left: 5px;" v-model=confirm :true-value='confAO' :false-value='confNA'>
				</p>
				<div v-show="confirm">Me alegro</div>
			</footer>
		</form>
	</div>
</template>

<script>
const axios = require('axios'); 
import {mapGetters, mapActions} from 'vuex'

export default
{
	data:()=>{
		return{
			form:{
				email:'armanolo@hotmail.com',
				password:'anda',
			},
			confirm: null,
			confAO:'Me alegro',
			confNA:'',
			error: false
		}
	},
	computed: mapGetters(['isAuth','getApiLogin']),
	methods:{addAuth: mapActions(['addAuth']).addAuth,
	//methods:{...mapActions(['addAuth']),
		login(){
			let data = {
				username: this.form.email,
				password: this.form.password
			};
			let isLogged = false;
			let nameUser = '';
			let message = '';
			let name = '';

			axios.post(this.getApiLogin,data)
			.then((response) => {
				switch(response.status){
					case 200:{
						isLogged = response.data['isLogged']
						name = response.data['name']
						break;
					}
					case 203:{
						message = `USER ${this.email} error password`;break;
					}
					case 204:{
						message = `USER ${this.email} Unauthorite`;break;
					}
					case 401:{
						message = `USER ${this.email} Missing arguments`;break;
					}
				}
			}).catch((error) => {
				console.log(error);
			}).then( () => {
				if(isLogged){
					this.addAuth(isLogged);
					alert(`Hi ${name}, you are logged`);
					//this.$router.push({ name: 'next_web_site', params: { name } })
				}else{
					alert(`Who are you?`);
				}
			});
			
		}
	}
}	
</script>

<style>


</style>