import axios from 'axios'
import router from '../router'
import { showToast } from './toastUtils'
import { logout } from '../auth.js'

const apiUtils = axios.create({
  baseURL: 'http://localhost:5000',
})

apiUtils.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

apiUtils.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        if (error.response.data && error.response.data.error) {
          const errorMsg = error.response.data.error
          if (errorMsg === 'Invalid token user') {
            logout()
            showToast('error', 'Session expired. Please log in again.')
            router.push('/login')
          }
        } else {
          showToast('error', 'Unauthorized access. Please check your credentials.')
        }
      }
      return Promise.reject(error)
    }
  )
  

export default apiUtils
