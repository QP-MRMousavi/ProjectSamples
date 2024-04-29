"use client";

import type { NextPage } from "next";
import { useState } from "react";

import {
  BreadcrumbItem,
  Breadcrumbs,
  Button,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Select,
  SelectItem,
} from "@nextui-org/react";
import { RiFileExcel2Fill } from "react-icons/ri";

import { MainContainer } from "@/components/main/main-container";
import { ToastContainer, toast } from "react-toastify";
import { LoadingModal } from "@/components/loading/loading-modal";
import { LoadingModalProps } from "@/schemas/components";
import { callToGenerateExport } from "@/Core/axios/main-absence-report";
import FiltersComponent from "@/components/main-report-filters/filters-component";

const MainReports: NextPage = () => {
  const [loading, setLoading] = useState<LoadingModalProps>({
    isOpen: false,
    title: "Loading ...",
    description: "retrieving data please wait...",
  });
  const [showDescription, setShowDescription] = useState<boolean>(false);
  const [selectedDepartmentIds, setSelectedDepartmentIds] = useState<
    Array<number>
  >([]);
  const [allDepartments, setAllDepartments] = useState([]);
  const [selectedStartingDate, setSelectedStartingDate] = useState<string>("");
  const [selectedEndingDate, setSelectedEndingDate] = useState<string>("");

  async function generateExport() {
    let generateUrlParam = "";
    if (selectedStartingDate && selectedEndingDate) {
      generateUrlParam = `ed=${selectedEndingDate}&sd=${selectedStartingDate}`;
    } else {
      if (selectedEndingDate) {
        toast.error("Maximum report duration is one year");
      }
      if (selectedStartingDate) {
        const startDate = new Date(selectedStartingDate);
        const endDate = new Date();

        const differenceInMs = endDate.getTime() - startDate.getTime();

        const differenceInYears = differenceInMs / (1000 * 60 * 60 * 24 * 365);

        if (differenceInYears > 1) {
          console.log(
            "The duration between the two dates is more than a year."
          );
        } else {
          console.log(
            "The duration between the two dates is not more than a year."
          );
        }
        generateUrlParam = "sd=" + selectedStartingDate;
      }
    }
    window.open(
      `/api/reports/main-absence-report?${generateUrlParam}`,
      "_blank"
    );
  }
  return (
    <MainContainer>
      <ToastContainer
        position="bottom-left"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />

      <LoadingModal
        title={loading.title}
        description={loading.description}
        isOpen={loading.isOpen}
      />

      <h1>Main-Report excel exporter</h1>
      <div className="grid hidden grid-cols-1 md:grid-cols-2 justify-items-stretch gap-4 ">
        <Input
          type="date"
          label="Start Date"
          isClearable
          onClear={() => {
            setSelectedStartingDate((prev) => "");
          }}
          value={selectedStartingDate}
          onChange={(e) => setSelectedStartingDate(e.target.value)}
        />
        <Input
          type="date"
          label="End Date"
          isClearable
          onClear={() => {
            setSelectedEndingDate((prev) => "");
          }}
          value={selectedEndingDate}
          onChange={(e) => setSelectedEndingDate(e.target.value)}
        />
      </div>
      {selectedStartingDate.length > 0 || selectedEndingDate.length > 0 ? (
        <>
          <h3 className="mt-2">Selected data descriptions</h3>
          <ul className="flex flex-col gap-3">
            {selectedStartingDate.length > 0 ? (
              <li>Starting Date: {selectedStartingDate}</li>
            ) : (
              <></>
            )}
            {selectedEndingDate.length > 0 ? (
              <li>Ending Date: {selectedEndingDate}</li>
            ) : (
              <></>
            )}
          </ul>
        </>
      ) : (
        <></>
      )}
      <div className="flex flex-row justify-end">
        {/* <Button
          color="primary"
          variant="ghost"
          startContent={<RiFileExcel2Fill />}
          isDisabled={
            !(selectedStartingDate.length > 0 || selectedEndingDate.length > 0)
          }
          onClick={() => {
            generateExport();
          }}
        >
          Export and Download Excel Report
        </Button> */}
      </div>

      <FiltersComponent />
    </MainContainer>
  );
};

export default MainReports;
