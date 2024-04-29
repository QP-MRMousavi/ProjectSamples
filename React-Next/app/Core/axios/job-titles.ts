import { ProjectTableListItemsResponse } from "@/schemas/api";
import { createAxiosWithAuth, ROUTES } from "./client";

export async function getJobTitlePriceListTable(
  pageNumber: number,
  pageSize: number = 20,
  searchQuery: string = ""
): Promise<ProjectTableListItemsResponse | null> {
  const axios = createAxiosWithAuth();
  if (!axios) return null;

  const response = await axios.get(
    `${
      ROUTES.projects.getJobTitlePriceList
    }?page=${pageNumber}&size=${pageSize}${
      searchQuery.length > 0 ? `&name=${searchQuery}` : ""
    }`
  );
  if (response.status != 200)
    throw new Error(`Error (${response.status}): An error occurred.`);
  const data = response.data as ProjectTableListItemsResponse;
  return data;
}

export async function updateJobTitlePrice(
  jobId: number,
  projectPrice: number
): Promise<void> {
  const axios = createAxiosWithAuth();
  if (!axios) throw new Error(`Error: Un authorized`);
  const response = await axios.put(ROUTES.projects.setJobTitlePriceList, {
    price: projectPrice,
    jobId: jobId,
  });

  if (response.status != 200)
    throw new Error(`Error (${response.status}): ${response.data.error}`);
}
