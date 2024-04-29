import { NextApiRequest, NextApiResponse } from "next";

export interface ApiController {
  allowedMethods: Array<string>;

  GET: (req: NextApiRequest, res: NextApiResponse) => void;
  POST: (req: NextApiRequest, res: NextApiResponse) => void;
  PUT: (req: NextApiRequest, res: NextApiResponse) => void;
  DELETE: (req: NextApiRequest, res: NextApiResponse) => void;
  OPTION: (req: NextApiRequest, res: NextApiResponse) => void;

  handleRequest: (req: NextApiRequest, res: NextApiResponse) => void;
}
export type ApiControllerSchema = {
  get: ((req: NextApiRequest, res: NextApiResponse) => void) | null;
  post: ((req: NextApiRequest, res: NextApiResponse) => void) | null;
  put: ((req: NextApiRequest, res: NextApiResponse) => void) | null;
  delete: ((req: NextApiRequest, res: NextApiResponse) => void) | null;
};
