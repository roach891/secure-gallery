import { reactive } from 'vue'
import { jwtDecode } from 'jwt-decode'

const token = localStorage.getItem('token')
const username = localStorage.getItem('username')

export function isTokenExpired(token) {
  try {
    const decoded = jwtDecode(token)
    const now = Math.floor(Date.now() / 1000)
    return decoded.exp < now
  } catch (error) {
    return true
  }
}

export const auth = reactive({
  isLoggedIn: !!token,
  username: username || null
})

if (token && !isTokenExpired(token)) {
  auth.isLoggedIn = true
  auth.username = username || jwtDecode(token).username
} else {
  logout()
}

export function login(token) {

  if (isTokenExpired(token)) {
    logout()
    return
  }

  localStorage.setItem('token', token)
  const decoded = jwtDecode(token)
  localStorage.setItem('username', decoded.username)

  auth.isLoggedIn = true
  auth.username = decoded.username
}

export function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    auth.isLoggedIn = false
    auth.username = null
}