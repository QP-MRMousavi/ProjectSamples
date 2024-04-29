import { NextApiRequest, NextApiResponse } from "next";

import { ApiController, ApiControllerSchema } from "@schemas/api";
import { requireAuthorization } from "@middlewares/auth";
import { cacheController } from "@/middlewares/cache-controller";

export class Controller implements ApiController {
  constructor(
    functions: ApiControllerSchema = {
      get: null,
      put: null,
      post: null,
      delete: null,
    }
  ) {
    if (functions.get) {
      this.GET = functions.get;
      this.allowedMethods.push("GET");
    }
    if (functions.put) {
      this.PUT = functions.put;
      this.allowedMethods.push("PUT");
    }
    if (functions.post) {
      this.POST = functions.post;
      this.allowedMethods.push("POST");
    }
    if (functions.delete) {
      this.DELETE = functions.delete;
      this.allowedMethods.push("DELETE");
    }
  }

  allowedMethods: string[] = [];

  GET(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader("Allow", this.allowedMethods);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
  POST(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader("Allow", this.allowedMethods);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
  PUT(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader("Allow", this.allowedMethods);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
  DELETE(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader("Allow", this.allowedMethods);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
  OPTION(req: NextApiRequest, res: NextApiResponse) {
    res.status(200);
  }
  @cacheController
  handleRequest(req: NextApiRequest, res: NextApiResponse) {
    switch (req.method) {
      case "GET":
        this.GET(req, res);
        break;
      case "PUT":
        this.PUT(req, res);
        break;
      case "POST":
        this.POST(req, res);
        break;
      case "DELETE":
        this.DELETE(req, res);
        break;
      case "OPTIONS":
        this.OPTION(req, res);
        break;
      default:
        res.setHeader("Allow", this.allowedMethods);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
}

export class AuthorizedController extends Controller {
  @cacheController
  @requireAuthorization
  handleRequest(req: NextApiRequest, res: NextApiResponse) {
    switch (req.method) {
      case "GET":
        this.GET(req, res);
        break;
      case "PUT":
        this.PUT(req, res);
        break;
      case "POST":
        this.POST(req, res);
        break;
      case "DELETE":
        this.DELETE(req, res);
        break;
      case "OPTIONS":
        this.OPTION(req, res);
        break;
      default:
        res.setHeader("Allow", this.allowedMethods);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
}

// Exporting handler function for Next.js API route
export function handler(controller: Controller) {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    await controller.handleRequest(req, res);
  };
}
