<template>
  <div class="auth-form">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />
      <button>Register</button>
    </form>
  </div>
</template>

<script>
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
    async register() {
      try {
        await apiUtils.post('/register', {
            username: this.username,
            password: this.password
        }, {
            headers: {
                "Content-Type": "application/json"
            }
        })
        showToast('success', 'Registration successful!')
        this.$router.push('/login')
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
