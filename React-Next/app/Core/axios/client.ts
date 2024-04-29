import { AuthToken } from "@/schemas/api";
import axios, { AxiosInstance, AxiosResponse } from "axios";

export const ROUTES = {
  projects: {
    getProjectPriceList: "/api/financial/project-price",
    setProjectPriceList: "/api/financial/project-price",
    getJobTitlePriceList: "/api/financial/job-title-price",
    setJobTitlePriceList: "/api/financial/job-title-price",
    postGenerateExcel: "/api/reports/main-reports",
  },
};

function getAuthTokenFromLocalStorage(): AuthToken | null {
  const tokenSTR = localStorage.getItem("auth-t");
  if (!tokenSTR) return null;
  const results = JSON.parse(tokenSTR) as AuthToken;
  return results;
}

export function createAxiosWithAuth(isFormData = false): AxiosInstance | null {
  //   const authToken = getAuthTokenFromLocalStorage();
  //   if (!authToken) return null;
  //   const headers: { [key: string]: string } = {
  //     Authorization: authToken.bearer,
  //   };
  //   if (isFormData) headers["Content-Type"] = "multipart/form-data";
  //   return axios.create({
  //     headers: headers,
  //   });
  return axios.create({});
}
