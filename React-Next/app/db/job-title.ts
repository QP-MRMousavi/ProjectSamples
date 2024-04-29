import prisma from "./db-context";
import {
  ProjectTableItemStructure,
  ProjectTableListItemsResponse,
} from "@/schemas/api";

export async function getJobTitleListForProjectTable(
  pageNumber: number,
  pageSize: number = 20,
  searchQuery: string | undefined = undefined
): Promise<ProjectTableListItemsResponse> {
  const offset = (pageNumber - 1) * pageSize;
  const data = await prisma.positions.findMany({
    select: {
      id: true,
      name: true,
      departments: {
        select: {
          name: true,
        },
      },
      app_project_job_price: true,
    },
    orderBy: {
      id: "asc",
    },
    where: {
      ...(searchQuery != undefined
        ? searchQuery.length > 0
          ? {
              OR: [{ name: { contains: searchQuery } }],
            }
          : {}
        : {}),
    },
    skip: offset,
    take: pageSize,
  });

  const totalCount = await prisma.positions.count({
    where: {
      ...(searchQuery != undefined
        ? searchQuery.length > 0
          ? {
              OR: [{ name: { contains: searchQuery } }],
            }
          : {}
        : {}),
    },
    skip: offset,
    take: pageSize,
  });
  const totalPages = Math.ceil(totalCount / pageSize);
  const results: Array<ProjectTableItemStructure> = data.map((job) => ({
    projectId: job.id,
    name: job.name,
    code: job.departments ? job.departments.name : "",
    clientName: "",
    assignment: "",
    contractPrice:
      job.app_project_job_price.length > 0
        ? `${job.app_project_job_price[0].price} ${job.app_project_job_price[0].currency}/H`
        : "0 AMD/H",
    startDate: new Date(),
    endDate: new Date(),
  }));
  return {
    totalPages: totalPages,
    results: results,
  };
}

export async function setJobTitleListForProjectTable(
  contractPrice: number,
  jobId: number
): Promise<void> {
  const existingPrice = await prisma.app_project_job_price.findFirst({
    where: {
      jobTitileId: jobId,
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
        projectId: null,
        price: contractPrice,
        currency: "AMD",
        jobTitileId: jobId,
      },
    });
  }
}
