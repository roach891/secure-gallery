<template>
  <nav class="navbar">
    <div class="left-section">
      <router-link to="/" class="app-name">Secure Gallery</router-link>
      <div class="left-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link v-if="!auth.isLoggedIn" to="/login" class="nav-link">Login</router-link>
        <router-link v-if="!auth.isLoggedIn" to="/register" class="nav-link">Register</router-link>
        <router-link v-if="auth.isLoggedIn" to="/gallery" class="nav-link">My Gallery</router-link>
      </div>
    </div>

    <div class="right-section" v-if="auth.isLoggedIn">
      <span class="welcome-message">Welcome, {{ auth.username }}</span>
      <button @click="handleLogout" class="logout-button">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { auth, logout } from '../auth.js'
import { useRouter } from 'vue-router'
import { showToast } from '../helpers/toastUtils'

const router = useRouter()

function handleLogout() {
  logout()
  showToast('success', 'Logged out successfully!')
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #333;
  color: #fff;
  font-size: 16px;
  border-bottom: 2px solid #444;
  gap: 2rem;
}

.left-section,
.right-section {
  display: flex;
  align-items: center;
  gap: 2rem; /* Gap between items inside left/right sections */
}

.app-name {
  font-size: 20px;
  font-weight: bold;
  color: #ffcc00;
  text-decoration: none;
}

.left-links {
  display: flex;
  gap: 1rem; /* Space between nav links */
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #ffcc00;
}

.welcome-message {
  font-size: 14px;
}

.logout-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.logout-button:hover {
  background-color: #e60000;
}
</style>