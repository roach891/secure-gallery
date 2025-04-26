<template>
  <div class="auth-form">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <button>Login</button>
    </form>
  </div>
</template>

<script>
import { login } from '../auth.js'
import apiUtils from '../helpers/apiUtils'
import { showToast } from '../helpers/toastUtils'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const res = await apiUtils.post('/login', {
          username: this.username,
          password: this.password
        })
        login(res.data.access_token)
        showToast('success', 'Login successful!')
        this.$router.push('/gallery')
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          showToast('error', err.response.data.error)
        } else {
          showToast('error', 'Login failed, please try again.')
        }
      }
    }
  }
}
</script>
