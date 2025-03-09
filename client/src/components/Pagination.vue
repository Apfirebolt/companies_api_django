<template>
    <nav
    class="container mx-auto px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
    aria-label="Pagination"
  >
    <div class="hidden sm:block">
      <p class="text-sm text-gray-700">
        Showing
        {{ " " }}
        <span class="font-medium">{{ showCurrentIndex }}</span>
        {{ " " }}
        to
        {{ " " }}
        <span class="font-medium">
          {{
            currentPage * numberOfItemsPerPage < allCompanies.count
              ? currentPage * numberOfItemsPerPage
              : allCompanies.total
          }}
        </span>
        {{ " " }}
        of
        {{ " " }}
        <span class="font-medium">{{ allCompanies.count }}</span>
        {{ " " }}
        results
      </p>
    </div>
    <div class="flex-1 flex justify-between sm:justify-end">
      <button
        @click="previosPageHandler"
        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Previous
      </button>
      <button
        @click="nextPageHandler"
        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Next
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed, toRefs } from "vue";
const props = defineProps({
  currentPage: Number,
  numberOfItemsPerPage: Number,
  allCompanies: Object,
});

const emits = defineEmits(["goToPreviousPage", "goToNextPage"]);
const {  currentPage, numberOfItemsPerPage, allCompanies } = toRefs(props);

const showCurrentIndex = computed(() => {
  return currentPage.value * numberOfItemsPerPage.value - numberOfItemsPerPage.value + 1;
});

const previosPageHandler = async () => {
  emits("goToPreviousPage");
};

const nextPageHandler = () => {
  emits("goToNextPage");
};
</script>
