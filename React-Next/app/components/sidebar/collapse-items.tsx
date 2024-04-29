"use client";
import React, { useState } from "react";
import { ChevronUpIcon } from "../icons/sidebar/chevron-up-icon";
import { Accordion, AccordionItem, Link } from "@nextui-org/react";
import { usePathname } from "next/navigation";

interface Props {
  icon: React.ReactNode;
  routeKey: string;
  title: string;
  items: Array<{
    name: string;
    url: string;
    icon: React.ReactNode;
  }>;
}

export const CollapseItems = ({ icon, routeKey, items, title }: Props) => {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  return (
    <div className="flex gap-4 h-full items-center cursor-pointer">
      <Accordion
        className="px-0"
        defaultExpandedKeys={[
          pathname?.includes(routeKey) ? "MenuAccording" : "",
        ]}
        variant={pathname?.includes(routeKey) ? "shadow" : "light"}
      >
        <AccordionItem
          key="MenuAccording"
          indicator={<ChevronUpIcon />}
          classNames={{
            indicator: "data-[open=true]:-rotate-180",
            trigger:
              "py-0 min-h-[44px] hover:bg-default-100 rounded-xl active:scale-[0.98] transition-transform px-3.5",

            title:
              "px-0 flex text-base gap-2 h-full items-center cursor-pointer",
          }}
          aria-label="Accordion 1"
          title={
            <div className="flex items-center flex-row gap-2">
              <span>{icon}</span>
              <span>{title}</span>
            </div>
          }
        >
          <div className="pl-8 flex flex-col gap-4">
            {items.map((item, index) => (
              <Link
                href={item.url}
                key={index}
                className={`w-full flex gap-2`}
                color={pathname == item.url ? "primary" : "foreground"}
              >
                {item.icon}
                {item.name}
              </Link>
            ))}
          </div>
        </AccordionItem>
      </Accordion>
    </div>
  );
};
