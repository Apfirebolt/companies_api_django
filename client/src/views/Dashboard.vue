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
          Here you can add, view, and delete urls.
        </p>
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
    </div>
  </section>
  <!-- Pagination -->
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useAuth } from "../store/auth";
import { useCompanyStore } from "../store/company";

const auth = useAuth();
const companyStore = useCompanyStore();

const authData = computed(() => auth.getAuthData);
const companyData = computed(() => companyStore.getCompanies);

onMounted(() => {
  companyStore.getCompaniesAction();
});
</script>
