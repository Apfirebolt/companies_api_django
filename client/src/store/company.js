import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useCompanyStore = defineStore("company", {
  state: () => ({
    company: ref({}),
    companies: ref([]),
    loading: ref(false),
  }),

  getters: {
    getCompany() {
      return this.company;
    },
    getCompanies() {
      return this.companies;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addCompany(companyData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.post("companies", companyData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Company added!");
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.message) {
            message = error.response.data.message;
          }
          toast.error(message);
        }
      } finally {
        this.loading = false;
      }
    },

    async getCompanyAction(companyId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        const response = await httpClient.get("companies/" + companyId, {
          headers,
        });
        this.company = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    async getCompaniesAction(page = 1, page_size = 25, search = "") {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.get("companies", {
          headers,
          params: {
            page,
            page_size,
            search,
          },
        });
        this.companies = response.data;
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async deleteCompany(companyId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.delete("company/" + companyId, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Company deleted!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async updateCompany(companyData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.put("company/" + companyData.id, companyData, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Company updated!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetCompanyData() {
      this.company = {};
      this.companies = [];
    },
  },
});
