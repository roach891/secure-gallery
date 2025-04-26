import { useToast } from 'vue-toastification'

const toast = useToast()

export function showToast(type, message) {
  switch(type) {
    case 'success':
      toast.success(message)
      break
    case 'error':
      toast.error(message)
      break
    case 'info':
      toast.info(message)
      break
    case 'warning':
      toast.warning(message)
      break
    default:
      toast.info(message)
  }
}
