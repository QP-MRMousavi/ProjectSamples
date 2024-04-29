import { MainAbsenceReportRequest } from "@/schemas/api";
import { createAxiosWithAuth, ROUTES } from "./client";

export async function callToGenerateExport(
  req: MainAbsenceReportRequest
): Promise<string | null> {
  const axios = createAxiosWithAuth();
  if (!axios) return null;
  const response = await axios.post(ROUTES.projects.postGenerateExcel, req);
  if (response.status != 200)
    throw new Error(`Error (${response.status}): An error occurred.`);
  const data = response.data;
  return data;
}
