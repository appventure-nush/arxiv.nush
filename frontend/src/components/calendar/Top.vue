<template>
  <div class="col-span-7">
    <div class="w-full flex justify-between items-center">
      <!-- Current month and year -->
      <div class="w-1/3 p-2 md:p-4">
        <div
          class="w-full inline-flex space-x-1 text-sm md:text-xl lg:text-2xl text-left font-bold md:font-semibold"
        >
          <span class="md:hidden">{{ calendarStore.monthStr.substring(0, 3) }}</span>
          <span class="hidden md:block">{{ calendarStore.monthStr }}</span>
          <span>{{ calendarStore.getYear }}</span>
        </div>
      </div>
      <!-- -------------------------- -->

      <!-- Naviigation -->
      <div
        class="hidden md:flex w-1/3 items-center justify-center text-gray-600"
      >
        <div class="flex space-x-3 items-center">
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-5 h-5 hover:text-gray-800 cursor-pointer hover:h-6 hover:w-6 transition-all"
              @click="calendarStore.decrementMonth(1)"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M18.75 19.5l-7.5-7.5 7.5-7.5m-6 15L5.25 12l7.5-7.5"
              />
            </svg>
            <!-- <v-icon class="w-5 h-5 hover:text-gray-800 cursor-pointer hover:h-6 hover:w-6 transition-all">mdi-arrow-left</v-icon> -->
          </div>
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-5 h-5 hover:text-gray-800 cursor-pointer hover:h-6 hover:w-6 transition-all"
              @click="calendarStore.incrementMonth(1)"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M11.25 4.5l7.5 7.5-7.5 7.5m-6-15l7.5 7.5-7.5 7.5"
              />
            </svg>
          </div>
        </div>
      </div>
      <!-- ----------------------------- -->

      <!-- Date picker and date view -->
      <div class="w-2/3 md:w-1/3 flex justify-end pr-2 md:pr-4">
        <div class="flex space-x-2 md:space-x-5">
          <div
            class="flex justify-center items-center border rounded-sm px-2 md:px-5 py-1 md:py-2 cursor-pointer hover:bg-gray-200 transition-colors"
            @click="calendarStore.resetDate()"
          >
            <h1 class="text-xs md:text-base font-medium md:font-semibold">
              Today
            </h1>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useCalendarStore } from "@/store/calendar";

// Store initialization and subscription
const calendarStore = useCalendarStore();

// Component variables
const monthStr = ref("");
const shortMonthStr = ref("");

/**
 * Populate the month variable with month data from store
 */
function prepareMonths() {
  monthStr.value = new Intl.DateTimeFormat("en-US", { month: "long" }).format(
    new Date(
      calendarStore.getYear,
      calendarStore.getMonth,
      calendarStore.getDay
    )
  );
  shortMonthStr.value = monthStr.value.substring(0, 3);
}

onMounted(() => {
  prepareMonths();
});
</script>
