import { NextApiResponse, NextApiRequest } from "next";

import * as bcrypt from "bcrypt";

export function requireAuthorization(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = async function (
    req: NextApiRequest,
    res: NextApiResponse
  ) {
    // Check if user is logged in
    const isLoggedIn = checkIfUserIsLoggedIn(req);

    if (!isLoggedIn) {
      res.status(401).json({ error: "Unauthorized" });
      return;
    }

    // User is logged in, proceed to the original method
    return await originalMethod.apply(this, [req, res]);
  };

  return descriptor;
}

function checkIfUserIsLoggedIn(req: NextApiRequest): boolean {
  console.log("request is checking ");
  //TODO: AUTH LOGICS

  return true;
}

function hashPassword(password: string, salt: string = ""): string {
  const option = {
    cost: 11,
    salt: "",
  };

  return "hashedPassword";
}
