<template>
	<div>
		<nav id="mainav">
			<ul>
				<div v-if="isAuth">
						<li class="active"><a href="index.html">Home</a></li>
						<li><a class="drop" href="#">Pages</a>
							<ul>
								<li><router-link to="/">Home</router-link></li>
								<li><router-link to="/login">Login</router-link></li>
							</ul>
						</li>
				</div>
				<div v-else>
					<li class="active">
						<div style="height:70px"></div>
					</li>
				</div>
			</ul>
		</nav>
	</div>
</template>
<script>
	import {mapGetters} from 'vuex'
	export default{
		computed: mapGetters(['isAuth'])
	}	
</script>

<style>
</style>
