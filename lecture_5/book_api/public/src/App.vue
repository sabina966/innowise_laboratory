<template>
<!--выдалілі ўвесь змест, каб свой напісаць-->
  <div id="app">
    <auth-component v-if="!isAuth" @handleAuth="handleAuth"/>
    <div v-else>
      <p>Вы зарэгістраваны</p>
    </div>
  </div>
</template>

<script>
/*
  будем дадаваць свой функцыянал
  замест HelloWorld -> AuthComponent
  у папцы components выдаляем HelloWorld.vue
  замест гэтага ствараем там AuthComponent.vue
*/
import AuthComponent from './components/AuthComponent.vue'

export default {
  name: 'App',
  components: {
    AuthComponent
  },
  data() {
    return {
      isAuth: false //будем показывать форму рэгістрацыі, калі false
    }
  },
  methods: {
    handleAuth() {
      this.isAuth = true;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
