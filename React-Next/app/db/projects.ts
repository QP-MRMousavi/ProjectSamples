import prisma from "./db-context";
import {
  ProjectTableItemStructure,
  ProjectTableListItemsResponse,
} from "@/schemas/api";

export async function getProjectsListForProjectTable(
  pageNumber: number,
  pageSize: number,
  searchQuery: string | undefined = undefined
): Promise<ProjectTableListItemsResponse> {
  console.log("Page Number", pageNumber, pageSize, searchQuery);
  const offset = (pageNumber - 1) * pageSize;
  const data = await prisma.projects.findMany({
    select: {
      id: true,
      name: true,
      code: true,
      assignments: {
        select: {
          name: true,
        },
      },
      start_date: true,
      end_date: true,
      app_project_job_price: true,
      clients: true,
    },
    orderBy: {
      start_date: "desc",
    },
    where: {
      is_visible: true,
      ...(searchQuery != undefined
        ? searchQuery.length > 0
          ? {
              OR: [
                { code: { contains: searchQuery } },
                { name: { contains: searchQuery } },
              ],
            }
          : {}
        : {}),
    },
    skip: offset,
    take: pageSize,
  });
  // Fetch total count of projects satisfying the search criteria
  const totalCount = await prisma.projects.count({
    where: {
      is_visible: true,
      ...(searchQuery
        ? {
            OR: [
              { code: { contains: searchQuery } },
              { name: { contains: searchQuery } },
            ],
          }
        : {}),
    },
  });

  const totalPages = Math.ceil(totalCount / pageSize);

  const results: Array<ProjectTableItemStructure> = data.map((project) => ({
    projectId: project.id,
    name: project.name,
    code: project.code,
    clientName: project.clients.name,
    assignment: project.assignments.name,
    contractPrice:
      project.app_project_job_price.length > 0
        ? `${project.app_project_job_price[0].price} ${project.app_project_job_price[0].currency}`
        : "0 AMD",
    startDate: project.start_date,
    endDate: project.end_date,
  }));
  return {
    totalPages: totalPages,
    results: results,
  };
}

export async function setProjectsListForProjectTable(
  contractPrice: number,
  projectId: number
): Promise<void> {
  const existingPrice = await prisma.app_project_job_price.findFirst({
    where: {
      projectId: projectId,
    },
  });

  if (existingPrice) {
    await prisma.app_project_job_price.update({
      where: {
        id: existingPrice.id,
      },
      data: {
        price: contractPrice,
      },
    });
  } else {
    await prisma.app_project_job_price.create({
      data: {
        projectId: projectId,
        price: contractPrice,
        currency: "AMD",
        jobTitileId: null,
      },
    });
  }
}
