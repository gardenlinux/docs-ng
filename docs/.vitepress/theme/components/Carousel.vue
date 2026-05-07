<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

export interface CarouselItem {
  name: string
  image: string
  url?: string
  description?: string
}

interface Props {
  title?: string
  items: CarouselItem[]
  slidesPerView?: number
  autoplay?: boolean | number
  loop?: boolean
  navigation?: boolean
  pagination?: boolean
  spaceBetween?: number
  grayscale?: boolean
  showBackground?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  slidesPerView: 5,
  autoplay: 3000,
  loop: true,
  navigation: true,
  pagination: true,
  spaceBetween: 30,
  grayscale: true,
  showBackground: false,
})

const swiperContainer = ref<HTMLElement>()
let swiperInstance: any = null

onMounted(() => {
  // Check if Swiper is already loaded
  if (!(window as any).Swiper) {
    // Load Swiper CSS from CDN
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://cdn.jsdelivr.net/npm/swiper@12/swiper-bundle.min.css'
    document.head.appendChild(link)

    // Load Swiper JS from CDN
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/swiper@12/swiper-bundle.min.js'
    script.onload = initSwiper
    document.head.appendChild(script)
  } else {
    initSwiper()
  }
})

function initSwiper() {
  if (!swiperContainer.value) return

  const autoplayConfig = typeof props.autoplay === 'number' 
    ? { delay: props.autoplay, disableOnInteraction: false }
    : props.autoplay 
    ? { delay: 3000, disableOnInteraction: false }
    : false

  const Swiper = (window as any).Swiper

  swiperInstance = new Swiper(swiperContainer.value, {
    slidesPerView: props.slidesPerView,
    spaceBetween: props.spaceBetween,
    loop: props.loop,
    autoplay: autoplayConfig,
    
    // Responsive breakpoints
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 20
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 25
      },
      768: {
        slidesPerView: 4,
        spaceBetween: 30
      },
      1024: {
        slidesPerView: props.slidesPerView,
        spaceBetween: props.spaceBetween
      }
    },

    // Navigation arrows
    navigation: props.navigation ? {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    } : false,

    // Pagination
    pagination: props.pagination ? {
      el: '.swiper-pagination',
      clickable: true,
    } : false,
  })
}

onBeforeUnmount(() => {
  if (swiperInstance) {
    swiperInstance.destroy(true, true)
  }
})
</script>

<template>
  <div 
    class="carousel-wrapper" 
    :class="{ 'has-background': showBackground }"
  >
    <h2 v-if="title" class="carousel-title">{{ title }}</h2>
    
    <!-- Swiper -->
    <div ref="swiperContainer" class="swiper">
      <!-- Additional required wrapper -->
      <div class="swiper-wrapper">
        <!-- Slides -->
        <div 
          v-for="(item, index) in items" 
          :key="`${item.name}-${index}`"
          class="swiper-slide"
        >
          <component
            :is="item.url ? 'a' : 'div'"
            :href="item.url"
            :target="item.url ? '_blank' : undefined"
            :rel="item.url ? 'noopener noreferrer' : undefined"
            class="carousel-item"
            :class="{ 'has-link': item.url, 'grayscale': grayscale }"
          >
            <img :src="item.image" :alt="item.name" loading="lazy" />
            <div v-if="item.name" class="carousel-item-name">
              {{ item.name }}
            </div>
          </component>
        </div>
      </div>
      
      <!-- Navigation buttons -->
      <div v-if="navigation" class="swiper-button-prev"></div>
      <div v-if="navigation" class="swiper-button-next"></div>
      
      <!-- Pagination -->
      <div v-if="pagination" class="swiper-pagination"></div>
    </div>
  </div>
</template>

<style scoped>
.carousel-wrapper {
  margin: 3rem auto;
  padding: 2rem 1rem;
  max-width: 1400px;
}

.carousel-wrapper.has-background {
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
}

.carousel-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--vp-c-text-1);
}

.swiper {
  width: 100%;
  padding-bottom: 50px;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  transition: all 0.3s;
  text-decoration: none;
  color: inherit;
  width: 100%;
  height: 140px;
  box-sizing: border-box;
}

.carousel-item.has-link {
  cursor: pointer;
}

.carousel-item.has-link:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.carousel-item img {
  max-width: 100%;
  max-height: 80px;
  width: auto;
  height: auto;
  object-fit: contain;
  transition: filter 0.3s;
}

.carousel-item.grayscale img {
  filter: grayscale(100%);
}

.carousel-item.has-link:hover.grayscale img {
  filter: grayscale(0%);
}

.carousel-item-name {
  text-align: center;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  margin-top: 0.75rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

/* Override Swiper button styles */
.swiper :deep(.swiper-button-prev),
.swiper :deep(.swiper-button-next) {
  color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--vp-c-divider);
  transition: all 0.3s;
}

.swiper :deep(.swiper-button-prev::after),
.swiper :deep(.swiper-button-next::after) {
  font-size: 20px;
  font-weight: bold;
}

.swiper :deep(.swiper-button-prev:hover),
.swiper :deep(.swiper-button-next:hover) {
  background: var(--vp-c-brand-1);
  color: white;
  border-color: var(--vp-c-brand-1);
}

/* Override Swiper pagination styles */
.swiper :deep(.swiper-pagination-bullet) {
  background: var(--vp-c-text-3);
  opacity: 0.5;
}

.swiper :deep(.swiper-pagination-bullet-active) {
  background: var(--vp-c-brand-1);
  opacity: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .carousel-wrapper {
    padding: 1.5rem 0.5rem;
  }

  .carousel-title {
    font-size: 1.25rem;
  }

  .carousel-item {
    height: 120px;
    padding: 1rem;
  }

  .carousel-item img {
    max-height: 70px;
  }
}

@media (max-width: 480px) {
  .carousel-item {
    height: 100px;
    padding: 0.75rem;
  }

  .carousel-item img {
    max-height: 60px;
  }
}
</style>
