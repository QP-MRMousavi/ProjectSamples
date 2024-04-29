// /api/financial/job-title-price/

import { NextApiResponse, NextApiRequest } from "next";
import { AuthorizedController, handler } from "@/Core/controller";
import { ProjectTableListItemsResponse } from "@/schemas/api/";
import {
  getJobTitleListForProjectTable,
  setJobTitleListForProjectTable,
} from "@/db/job-title";

async function getJobTitlePriceListTable(
  req: NextApiRequest,
  res: NextApiResponse<ProjectTableListItemsResponse>
) {
  const queries = req.query;
  const pageNumber = parseInt(queries.page as string, 10) || 1;
  const pageSize = parseInt(queries.size as string, 10) || 20;
  const searchParam = queries.name;

  const data = await getJobTitleListForProjectTable(
    pageNumber,
    pageSize,
    searchParam as string | undefined
  );
  res.status(200).json({
    totalPages: data.totalPages,
    results: data.results,
  });
}

async function updateJobTitlePriceList(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { price, jobId } = req.body;
  try {
    const data = await setJobTitleListForProjectTable(price, jobId);
    res.status(200).send("");
  } catch (error) {
    res.status(500).json({
      error: "Error on updating project contract price",
    });
  }
}

export default handler(
  new AuthorizedController({
    get: getJobTitlePriceListTable,
    put: updateJobTitlePriceList,
    post: null,
    delete: null,
  })
);
