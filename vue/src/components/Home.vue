<template>
	<div>
		<router-view/>
		<router-view name='second'/>
	</div>
</template>

<script>
	import {mapGetters,mapActions} from 'vuex'
	export default{
		data(){
			return{
			}
		},
		mounted(){
		},
		computed: mapGetters(['isAuth']),
		methods: mapActions(['addAuth','removeAuth'])
	}	
</script>

<style>

.block{
	display: table-cell;
	padding: 6%;
}

/* Full-width input fields */
input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Set a style for all buttons */
button {
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  opacity: 0.8;
}

/* Center the image and position the close button */
.imgcontainer {
  text-align: center;
  margin: 24px 0 12px 0;
  position: relative;
}

img.avatar {
  width: 20%;
  border-radius: 50%;
}

.container {
  padding: 16px;
}

span.psw {
  float: right;
  padding-top: 16px;
}

/* The Modal (background) 
.modal {
  position: fixed; / Stay in place /
  z-index: 1; / Sit on top /
  left: 25%;
  top: 0;
  width: 50%; / Full width /
  height: 100%; / Full height /
  overflow: auto; / Enable scroll if needed /
  padding-top: 60px;
}
*/
.modal {
	position: fixed;
	left: 15%;
	top: 5%;
	width: 60%;
	height: 60%;
	overflow: auto;
	padding: 3%;
	border-style: solid;
}
</style>
