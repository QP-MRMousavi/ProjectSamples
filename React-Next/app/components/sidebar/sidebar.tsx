import React from "react";
import { Sidebar } from "./sidebar.styles";
import { Avatar, Tooltip } from "@nextui-org/react";
import { FaMoneyBillWheat } from "react-icons/fa6";
import { MdOutlineSettingsAccessibility } from "react-icons/md";
import { GoProject } from "react-icons/go";
import { HiOutlineDocumentReport } from "react-icons/hi";

import { TbReportAnalytics } from "react-icons/tb";
import { TbReportMoney } from "react-icons/tb";
import { TbReportSearch } from "react-icons/tb";
import { TbFileTime } from "react-icons/tb";
import { GoProjectRoadmap } from "react-icons/go";
import { FaUsers } from "react-icons/fa6";
import { MdDashboard } from "react-icons/md";

import { HeaderTmsInfo } from "./header-tms-info";
import { CollapseItems } from "./collapse-items";
import { SidebarItem } from "./sidebar-item";
import { useSidebarContext } from "../layout/layout-context";

import { usePathname } from "next/navigation";

export const SidebarWrapper = () => {
  const pathname = usePathname();
  const { collapsed, setCollapsed } = useSidebarContext();

  return (
    <aside className="h-screen z-[202] sticky top-0">
      {collapsed ? (
        <div className={Sidebar.Overlay()} onClick={setCollapsed} />
      ) : null}
      <div
        className={Sidebar({
          collapsed: collapsed,
        })}
      >
        <div className={Sidebar.Header()}>
          <HeaderTmsInfo />
        </div>
        <div className="flex flex-col justify-between h-full">
          <div className={Sidebar.Body()}>
            <SidebarItem
              title="Dashboard"
              icon={<MdDashboard />}
              isActive={pathname === "/"}
              href="/"
            />
            <CollapseItems
              icon={<FaMoneyBillWheat />}
              routeKey="financial-settings"
              items={[
                {
                  name: "Projects",
                  url: "/financial-settings/projects",
                  icon: <GoProject />,
                },
                {
                  name: "Job Titles",
                  url: "/financial-settings/job-titles",
                  icon: <MdOutlineSettingsAccessibility />,
                },
              ]}
              title="Financial Settings"
            />
            <CollapseItems
              icon={<HiOutlineDocumentReport />}
              routeKey="reports"
              items={[
                {
                  name: "Main Reports",
                  url: "/reports/main-reports",
                  icon: <TbReportAnalytics />,
                },
                {
                  name: "Financial Reports",
                  url: "/reports/financial-reports",
                  icon: <TbReportMoney />,
                },
                {
                  name: "Matrix Sum Reports",
                  url: "/reports/matrix-sum",
                  icon: <TbReportSearch />,
                },
              ]}
              title="Reports"
            />
            <SidebarItem
              title="Timesheets Status"
              icon={<TbFileTime />}
              isActive={pathname === "/timesheets-status"}
              href="/timesheets-status"
            />
            <SidebarItem
              title="Projects"
              icon={<GoProjectRoadmap />}
              isActive={pathname === "/projects"}
              href="/projects"
            />
            <SidebarItem
              title="Clients"
              icon={<FaUsers />}
              isActive={pathname === "/clients"}
              href="/clients"
            />
          </div>
          <div className={Sidebar.Footer()}></div>
        </div>
      </div>
    </aside>
  );
};
