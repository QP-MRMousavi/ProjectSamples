// /api/clients/get_all.ts

import { NextApiResponse, NextApiRequest } from "next";
import { AuthorizedController, handler } from "@/Core/controller";
import { getTimeSheetDetails } from "@/db/main-export";

async function get(req: NextApiRequest, res: NextApiResponse) {
  // res.status(200).json({ data: await getTimeSheetDetails(2024) });
}
const financialSettings = "";
export default handler(
  new AuthorizedController({
    get: get,
    put: null,
    post: null,
    delete: null,
  })
);
