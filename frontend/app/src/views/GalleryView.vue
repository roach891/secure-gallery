<template>
  <div class="gallery">
    <h2>My Gallery</h2>

     <form @submit.prevent="handleFileUpload">
      <input 
        ref="fileInput" 
        type="file" 
        accept="image/*"
        required
      />
      <button type="submit">Upload Image</button>
    </form>
    <template v-if="images && images.length > 0">
        <div class="images">
            <div v-for="img in images" :key="img.filename" class="image-card">
                <img :src="img.blobUrl" alt="User image" />
                <button @click="deleteImage(img.filename)">Delete</button>
            </div>
        </div>
    </template>
  </div>
</template>

<script>
import apiUtils from '../helpers/apiUtils'
import { showToast } from '../helpers/toastUtils'

export default {
  data() {
    return {
      images: []
    }
  },
  mounted() {
    this.fetchImages()
  },
  beforeUnmount() {
    this.images.forEach(img => {
      if (img.blobUrl) {
        URL.revokeObjectURL(img.blobUrl)
      }
    })
  },
  methods: {
    async fetchImages() {
      const token = localStorage.getItem('token')

      try {
        const res = await apiUtils.get('/images')

        const imageData = res.data.images

        const imagesWithBlobUrls = await Promise.all(
          imageData.map(async (img) => {
            const imageBlob = await apiUtils.get(`/images/${img.filename}`, {
              responseType: 'blob'
            })

            const blobUrl = URL.createObjectURL(imageBlob.data)

            return {
              filename: img.filename,
              blobUrl
            }
          })
        )

        this.images = imagesWithBlobUrls
      } catch (error) {
        showToast('error', 'Failed to fetch images. Please try again later.')
      }
    },
    async handleFileUpload() {
      const token = localStorage.getItem('token')
      const file = this.$refs.fileInput.files[0]
      if (!file) return
      const formData = new FormData()
      formData.append('file', file)
      try{
        await apiUtils.post('/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        showToast('success', 'Image uploaded successfully!')
        this.fetchImages()
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          showToast('error', err.response.data.error)
        } else {
          showToast('error', 'Upload failed, please try again.')
        }
      }
    },
    async deleteImage(filename) {
      const token = localStorage.getItem('token')
      try {
        await apiUtils.delete(`/images/${filename}`)
        showToast('success', 'Image deleted successfully!')
        this.fetchImages()
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          showToast('error', err.response.data.error)
        } else {
          showToast('error', 'Upload failed, please try again.')
        }
      }
    }
  }
}
</script>

<style scoped>
.gallery {
  max-width: 1000px;
  margin: 0 auto;
  padding: 1rem;
}

.images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.image-card {
  border: 1px solid #ccc;
  padding: 0.5rem;
  border-radius: 8px;
  background: #f9f9f9;
  text-align: center;
}

.image-card img {
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: contain;
  border-radius: 4px;
}
</style>