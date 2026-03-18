import axios from 'axios'
import router from './router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem('access_token')
        router.push('/login')
      } else if (error.response.status === 422) {
        // Parse Pydantic validation errors
        const detail = error.response.data.detail
        if (Array.isArray(detail)) {
          // Ex: "Field 'email': Invalid email format"
          const messages = detail.map(d => {
            const field = d.loc && d.loc.length > 1 ? d.loc[d.loc.length - 1] : ''
            return field ? `${d.msg}` : d.msg
          })
          error.response.data.detail = messages.join(', ')
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
