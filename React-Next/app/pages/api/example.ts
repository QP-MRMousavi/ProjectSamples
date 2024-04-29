// pages/api/protected.ts

import { NextApiResponse, NextApiRequest } from "next";
import { AuthorizedController, handler } from "@/Core/controller";

async function get(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ message: "GET request handled" });
}

export default handler(
  new AuthorizedController({
    get: get,
    put: null,
    post: null,
    delete: null,
  })
);
