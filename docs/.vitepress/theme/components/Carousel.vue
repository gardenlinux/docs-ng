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
    centeredSlides: false,
    
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
            <div class="carousel-item-content">
              <img :src="item.image" :alt="item.name" loading="lazy" />
            </div>
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
  margin: 4rem auto;
  padding: 3rem 2rem;
  max-width: 1400px;
}

.carousel-wrapper.has-background {
  background: var(--vp-c-bg-soft);
  border-radius: 16px;
}

.carousel-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 3rem;
  color: var(--vp-c-text-1);
  letter-spacing: -0.02em;
}

.swiper {
  width: 100%;
  padding-bottom: 60px;
  padding-top: 20px;
  position: relative;
  overflow: hidden;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  height: auto;
}

.carousel-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: inherit;
  width: 100%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.carousel-item-content {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--vp-c-bg);
  border-radius: 12px;
  border: 2px solid transparent;
  width: 100%;
  height: 160px;
  box-sizing: border-box;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

/* Subtle gradient background on hover */
.carousel-item-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--vp-c-brand-1) 0%, var(--vp-c-brand-2) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}

.carousel-item.has-link {
  cursor: pointer;
}

.carousel-item.has-link:hover .carousel-item-content {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-8px);
  box-shadow: 0 12px 24px -10px rgba(0, 159, 118, 0.3),
              0 8px 16px -8px rgba(0, 0, 0, 0.1);
}

.carousel-item.has-link:hover .carousel-item-content::before {
  opacity: 0.05;
}

.carousel-item-content img {
  max-width: 90%;
  max-height: 90px;
  width: auto;
  height: auto;
  object-fit: contain;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}

.carousel-item.grayscale .carousel-item-content img {
  filter: grayscale(100%) opacity(0.7);
}

.carousel-item.has-link:hover.grayscale .carousel-item-content img {
  filter: grayscale(0%) opacity(1);
  transform: scale(1.05);
}

.carousel-item.has-link:hover .carousel-item-content img {
  transform: scale(1.05);
}

.carousel-item-name {
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--vp-c-text-2);
  margin-top: 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
  transition: color 0.3s ease;
}

.carousel-item.has-link:hover .carousel-item-name {
  color: var(--vp-c-brand-1);
}

/* Modern navigation buttons */
.swiper :deep(.swiper-button-prev),
.swiper :deep(.swiper-button-next) {
  color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 159, 118, 0.4);
}

.swiper :deep(.swiper-button-disabled) {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Modern pagination dots */
.swiper :deep(.swiper-pagination) {
  bottom: 10px;
}

.swiper :deep(.swiper-pagination-bullet) {
  background: var(--vp-c-text-3);
  opacity: 0.4;
  width: 10px;
  height: 10px;
  transition: all 0.3s ease;
}

.swiper :deep(.swiper-pagination-bullet-active) {
  background: var(--vp-c-brand-1);
  opacity: 1;
  width: 28px;
  border-radius: 5px;
}

/* Responsive */
@media (max-width: 1024px) {
  .carousel-title {
    font-size: 1.75rem;
  }
  
  .carousel-item-content {
    height: 140px;
    padding: 1.5rem;
  }
  
  .carousel-item-content img {
    max-height: 80px;
  }
}

@media (max-width: 768px) {
  .carousel-wrapper {
    padding: 2rem 1rem;
    margin: 2rem auto;
  }

  .carousel-title {
    font-size: 1.5rem;
    margin-bottom: 2rem;
  }

  .carousel-item-content {
    height: 120px;
    padding: 1.25rem;
  }

  .carousel-item-content img {
    max-height: 70px;
  }

  .swiper :deep(.swiper-button-prev),
  .swiper :deep(.swiper-button-next) {
    width: 40px;
    height: 40px;
  }

  .swiper :deep(.swiper-button-prev::after),
  .swiper :deep(.swiper-button-next::after) {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .carousel-wrapper {
    padding: 1.5rem 0.5rem;
  }

  .carousel-item-content {
    height: 100px;
    padding: 1rem;
  }

  .carousel-item-content img {
    max-height: 60px;
  }

  .carousel-item-name {
    font-size: 0.8rem;
    margin-top: 0.75rem;
  }

  .swiper :deep(.swiper-button-prev),
  .swiper :deep(.swiper-button-next) {
    width: 36px;
    height: 36px;
  }

  .swiper :deep(.swiper-button-prev::after),
  .swiper :deep(.swiper-button-next::after) {
    font-size: 16px;
  }
}
</style>
