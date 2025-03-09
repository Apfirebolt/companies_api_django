<template>
  <section class="shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5">
      <h2 class="text-3xl my-2 py-2 text-center text-jet-black">DASHBOARD</h2>
      <div class="flex flex-col items-center bg-green-100 p-4 rounded-md">
        <p v-if="authData">
          Welcome to the dashboard,
          <span class="text-lg font-semibold text-gray-700">
            {{ authData.username }}
          </span>
          Here you can view companies.
        </p>
        <div class="my-2 flex justify-between w-full items-center">
          <div>
            <label for="itemsPerPage" class="mr-2">Items per page:</label>
            <select
              id="itemsPerPage"
              v-model.number="itemsPerPage"
              class="border rounded p-2"
            >
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
          <div class="w-1/2">
            <label for="searchText" class="mr-2">Search:</label>
            <input
              type="text"
              id="searchText"
              v-model="searchText"
              class="border rounded p-2 w-1/2"
            />
          </div>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="company in companyData.results"
          :key="company.id"
          class="bg-white shadow-md rounded-lg p-4 m-2"
        >
          <h3 class="text-xl font-bold mb-2">{{ company.name }}</h3>
          <p><strong>Rating:</strong> {{ company.rating }}</p>
          <p><strong>Review:</strong> {{ company.review }}</p>
          <p><strong>Type:</strong> {{ company.company_type }}</p>
          <p><strong>Headquarters:</strong> {{ company.head_quarters }}</p>
          <p><strong>Age:</strong> {{ company.company_age }}</p>
          <p><strong>Employees:</strong> {{ company.no_of_employee }}</p>
        </div>
      </div>
    </div>
  </section>
  <!-- Pagination -->
  <Pagination
    v-if="companyData"
    @go-to-previous-page="goToPreviousPage"
    @go-to-next-page="goToNextPage"
    :allCompanies="companyData"
    :current-page="currentPage"
    :number-of-items-per-page="itemsPerPage"
  />
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useAuth } from "../store/auth";
import { useCompanyStore } from "../store/company";
import Pagination from "../components/Pagination.vue";

const auth = useAuth();
const companyStore = useCompanyStore();
const currentPage = ref(1);
const itemsPerPage = ref(25);
const searchText = ref("");
let timeoutId;

const debouncedSearch = (value) => {
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    if (value.length > 2) {
      searchCompanyUtil();
    } else if (value.length === 0) {
      companyStore.getCompaniesAction(1, itemsPerPage.value, "");
    }
  }, 1000); // Adjust delay as needed (in milliseconds)
};

watch(searchText, debouncedSearch);

const searchCompanyUtil = () => {
  companyStore.getCompaniesAction(1, itemsPerPage.value, searchText.value);
};

const authData = computed(() => auth.getAuthData);
const companyData = computed(() => companyStore.getCompanies);

const goToNextPage = async () => {
  let total_pages = Math.ceil(companyData.value.count / itemsPerPage.value);
  if (currentPage.value < total_pages) {
    currentPage.value += 1;
    await companyStore.getCompaniesAction(
      currentPage.value,
      itemsPerPage.value,
      searchText.value
    );
  }
};

const goToPreviousPage = async () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
    await companyStore.getCompaniesAction(
      currentPage.value,
      itemsPerPage.value,
      searchText.value
    );
  }
};

watch(itemsPerPage, async (newVal) => {
  console.log(newVal);
  await companyStore.getCompaniesAction(currentPage.value, newVal, searchText.value);
});

onMounted(() => {
  companyStore.getCompaniesAction(1, itemsPerPage.value, searchText.value);
});
</script>
