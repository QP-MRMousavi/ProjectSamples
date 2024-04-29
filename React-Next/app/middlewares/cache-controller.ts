import { NextApiResponse, NextApiRequest } from "next";

export function cacheController(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = async function (
    req: NextApiRequest,
    res: NextApiResponse
  ) {
    const originalWriteHead = res.writeHead;

    try {
      return await originalMethod.apply(this, [req, res]);
    } finally {
      const originalWriteHead = res.writeHead;
      res.writeHead = (...args) => {
        res.setHeader("Cache-control", `max-age=${process.env.CACHE_MAX_AGE}`);

        return originalWriteHead.apply(res, args as any);
      };
    }
  };

  return descriptor;
}
