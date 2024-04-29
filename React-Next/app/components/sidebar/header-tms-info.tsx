"use client";
import { Image } from "@nextui-org/react";
import React, { useState } from "react";

interface Company {
  name: string;
  location: string;
  logo: React.ReactNode;
}

export const HeaderTmsInfo = () => {
  const [company, setCompany] = useState<Company>({
    name: "TMS",
    location: "Report Generator",
    logo: <Image src="/img/tms-logo.png" className="max-w-20" />,
  });
  return (
    <div className="w-full min-w-[260px]">
      <div className="flex items-center gap-2">
        {company.logo}
        <div className="flex flex-col gap-4">
          <h3 className="text-xl font-medium m-0 text-default-900 -mb-4 whitespace-nowrap">
            {company.name}
          </h3>
          <span className="text-xs font-medium text-default-500">
            {company.location}
          </span>
        </div>
      </div>
    </div>
  );
};
