// /api/financial/project-price/

import { NextApiResponse, NextApiRequest } from "next";
import { AuthorizedController, handler } from "@/Core/controller";
import { ProjectTableListItemsResponse } from "@/schemas/api/";
import {
  getProjectsListForProjectTable,
  setProjectsListForProjectTable,
} from "@/db/projects";

async function getProjectPriceListTable(
  req: NextApiRequest,
  res: NextApiResponse<ProjectTableListItemsResponse>
) {
  const queries = req.query;

  const pageNumber = parseInt(queries.page as string, 10) || 1;
  const pageSize = parseInt(queries.size as string, 10) || 10;
  const searchParam = queries.project;
  console.log("getProjectPriceListTable", pageSize, queries);
  const data = await getProjectsListForProjectTable(
    pageNumber,
    pageSize,
    searchParam as string | undefined
  );
  res.status(200).json({
    totalPages: data.totalPages,
    results: data.results,
  });
}

async function updateProjectPriceList(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { price, projectId } = req.body;
  try {
    const data = await setProjectsListForProjectTable(price, projectId);
    res.status(200).send("");
  } catch (error) {
    res.status(500).json({
      error: "Error on updating project contract price",
    });
  }
}

export default handler(
  new AuthorizedController({
    get: getProjectPriceListTable,
    put: updateProjectPriceList,
    post: null,
    delete: null,
  })
);
