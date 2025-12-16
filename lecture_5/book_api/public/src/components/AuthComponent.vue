<script>//no setup!
import axios from "axios";
export default {
name: 'AuthComponent',
data() {
  return {
    registerName: '',
    registerAge: '',
    loginName: ''
  }
},
methods: {
  async register() {
    const response = await axios.post('http://127.0.0.1:8022/users/',{
    name: this.registerName,
    age: Number(this.registerAge)
    });

    console.log('Register success: ' + response.data);
    alert('Карыстальнік паспяхова зарэгістраваны!');

    // Очистить поля после успеха
    this.registerName = '';
    this.registerAge = '';
  },
  async login() {
    const response = await axios.get(`http://127.0.0.1:8022/users/${this.loginName}`);
    if(response.data) {
      this.$emit('handleAuth');
    } else {
      alert('Не знойдзен');
    }
  }
}
}
</script>

<template>
  <div>
    <h2>Рэгістрацыя</h2>
    <form @submit.prevent="register">
      <div>
        <label for="registerName">Імя:</label>
        <input type="text" id="registerName" v-model="registerName">
      </div>

      <div>
        <label for="registerAge">Узрост:</label>
        <input type="text" id="registerAge" v-model="registerAge">
      </div>
      <button type="submit">Рэгістрацыя</button>
    </form>

    <h2>Аўтарызацыя</h2>
    <form @submit.prevent="login">
      <div>
        <label for="loginName">Імя:</label>
        <input type="text" id="loginName" v-model="loginName">
      </div>
      <button type="submit">Аўтарызавацца</button>
    </form>
  </div>
</template>

<style scoped>

</style>