"use client";
import type { NextPage } from "next";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Spinner,
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  Chip,
  Pagination,
  SortDescriptor,
} from "@nextui-org/react";
import { ToastContainer, toast } from "react-toastify";

import { MainContainer } from "@/components/main/main-container";
import { LoadingModal } from "@/components/loading/loading-modal";
import {
  EditProjectPriceModal,
  LoadingModalProps,
  TableSortDescriptor,
} from "@/schemas/components";
import {
  ProjectTableItemStructure,
  ProjectTableListItemsResponse,
} from "@/schemas/api";
import {
  getProjectPriceListTable,
  updateProjectPrice,
} from "@/Core/axios/projects";
import { formatDate } from "@/Core/formatters";
import { FaCreditCard } from "react-icons/fa6";
import { CiSearch } from "react-icons/ci";

const Projects: NextPage = () => {
  const [loading, setLoading] = useState<LoadingModalProps>({
    isOpen: true,
    title: "Loading ...",
    description: "retrieving data please wait...",
  });

  const [editProjectPriceModal, setEditProjectPriceModal] =
    useState<EditProjectPriceModal>({
      isOpen: false,
      projectName: "",
      projectCode: "",
      price: 0,
      projectId: 0,
    });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize, setPageSize] = useState<number>(20);
  const [listItems, setListItems] = useState<Array<ProjectTableItemStructure>>(
    []
  );

  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const shouldRenderTable = useRef(true);
  const [sortDescriptor, setSortDescriptor] = useState<
    TableSortDescriptor<
      | "projectId"
      | "name"
      | "code"
      | "clientName"
      | "assignment"
      | "contractPrice"
      | "startDate"
      | "endDate"
    >
  >({
    column: "name",
    direction: "ascending",
  });

  const openLoadingModal = (title: string, description: string) => {
    setLoading({
      isOpen: true,
      title: title,
      description: description,
    });
  };

  const closeLoadingModal = () => {
    setLoading((prev) => ({
      ...prev,
      isOpen: false,
    }));
  };

  const renderTable = useCallback(
    async (
      refreshPage: boolean = false,
      selectedPage: number = 1,
      selectedPageSize: number = -1,
      selectedQueryTemp: string = ""
    ) => {
      try {
        let selectedQuery = "";
        setListItems([]);

        if (refreshPage) {
          setPage((prev) => 1);
        }

        if (selectedQueryTemp === "--") {
          selectedQuery = "";
        } else {
          selectedQuery = selectedQueryTemp || searchQuery; // Use the parameter value if available, else use the state value
        }
        if (selectedPageSize == -1) {
          selectedPageSize = pageSize;
        }
        setIsLoading(true);

        let data: ProjectTableListItemsResponse | null =
          await getProjectPriceListTable(
            selectedPage,
            selectedPageSize,
            selectedQuery
          );

        closeLoadingModal();

        if (!data) {
          toast.error("Please Login first");
          setIsLoading(false);
          return;
        }

        setListItems((prevListItems) => [...data!.results]);
        setTotalPages(data!.totalPages);
        setPage(selectedPage);
        setIsLoading(false);
      } catch (error: { message: string } | any) {
        toast.error(error.message || error);
        setIsLoading(false);
      }
    },
    [pageSize, page, searchQuery]
  );
  useEffect(() => {
    if (shouldRenderTable.current) {
      shouldRenderTable.current = false;
      renderTable(false);
    }
  });
  const sortedItems = useMemo(() => {
    return [...listItems].sort(
      (a: ProjectTableItemStructure, b: ProjectTableItemStructure) => {
        const first = a[sortDescriptor.column];
        const second = b[sortDescriptor.column];
        const cmp = first < second ? -1 : first > second ? 1 : 0;

        return sortDescriptor.direction === "descending" ? -cmp : cmp;
      }
    );
  }, [sortDescriptor, listItems]);
  function openEditProjectPriceModal(
    projectId: number,
    projectPrice: string,
    projectName: string,
    projectCode: string
  ) {
    setEditProjectPriceModal((prev) => ({
      isOpen: true,
      projectName: projectName,
      projectId: projectId,
      price: parseFloat(projectPrice.split(" ")[0]),
      projectCode: projectCode,
    }));
  }
  function closeEditProjectPriceModal() {
    setEditProjectPriceModal((prev) => ({
      isOpen: false,
      projectName: "",
      projectId: 0,
      price: 0,
      projectCode: "",
    }));
  }
  async function updatePriceOfProject() {
    openLoadingModal("Updating Project Contract Price", "please wait...");
    try {
      await updateProjectPrice(
        editProjectPriceModal.projectId,
        editProjectPriceModal.price
      );
      const projectIndex = listItems.findIndex(
        (x) => x.projectId === editProjectPriceModal.projectId
      );

      const updatedListItems = listItems.map((item) => {
        if (item.projectId === editProjectPriceModal.projectId) {
          return {
            ...item,
            contractPrice: `${editProjectPriceModal.price} AMD`,
          };
        }
        return item;
      });

      setListItems(updatedListItems);
      closeEditProjectPriceModal();
      closeLoadingModal();
      toast.success(
        `Project ${editProjectPriceModal.projectName} contract price updated to ${editProjectPriceModal.price} AMD.`
      );
    } catch (error) {
      toast.error((error as { message: string }).message);
      closeLoadingModal();
    }
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

      <Modal
        size="sm"
        isOpen={editProjectPriceModal.isOpen}
        onClose={closeEditProjectPriceModal}
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                {editProjectPriceModal.projectName}
              </ModalHeader>
              <ModalBody className="flex flex-col">
                <p>
                  Modifying {editProjectPriceModal.projectName} (
                  {editProjectPriceModal.projectCode}) contract price.
                </p>
                <Input
                  type="number"
                  variant="bordered"
                  label="Contract Price in AMD"
                  value={editProjectPriceModal.price.toString()}
                  onChange={(e) =>
                    setEditProjectPriceModal((prevState) => ({
                      ...prevState,
                      price: parseInt(e.target.value),
                    }))
                  }
                />
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
                <Button color="primary" onPress={updatePriceOfProject}>
                  Submit
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
      <div className=" flex flex-row flex-wrap items-end gap-4">
        <div className="flex flex-col grow gap-2">
          <span>Project code or name to search</span>
          <Input
            type="text"
            label=""
            placeholder=""
            labelPlacement="outside"
            isClearable
            onClear={async () => {
              setSearchQuery((prev) => "");
              setPage((prev) => 0);
              renderTable(true, 1, -1, "--");
            }}
            value={searchQuery.toString()}
            onChange={(e) => setSearchQuery(e.target.value)}
            startContent={
              <CiSearch className="text-2xl text-default-400 pointer-events-none flex-shrink-0" />
            }
            onKeyUp={(e) => {
              if (e.code == "Enter") {
                renderTable(true, 1);
              }
            }}
          />
        </div>
        <Button
          isIconOnly
          color="default"
          variant="faded"
          aria-label="Search"
          isLoading={isLoading}
          onClick={() => {
            renderTable(true, 1);
          }}
        >
          <CiSearch />
        </Button>
      </div>
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center">
          <span className="text-default-400 text-small">
            Total{" "}
            {totalPages == 1 ? `${totalPages} page` : `${totalPages} pages`} /{" "}
            {pageSize} rows per page
          </span>
          <label className="flex items-center text-default-400 text-small">
            Rows per page:
            <select
              className="bg-transparent outline-none text-default-400 text-small"
              value={pageSize.toString()}
              onChange={(e) => {
                setPageSize(parseInt(e.target.value));
                setPage(1);
                setIsLoading(true);
                renderTable(true, 1, parseInt(e.target.value));
              }}
            >
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
              <option value="150">150</option>
              <option value="200">200</option>
            </select>
          </label>
        </div>
      </div>
      <Table
        isHeaderSticky
        aria-label=""
        bottomContent={
          <div className="flex w-full justify-center">
            <Pagination
              isCompact
              showControls
              showShadow
              color="secondary"
              page={page}
              total={totalPages}
              onChange={(page) => {
                renderTable(false, page);
              }}
            />
          </div>
        }
        sortDescriptor={sortDescriptor}
        onSortChange={(descriptor: SortDescriptor) =>
          setSortDescriptor(
            descriptor as TableSortDescriptor<
              | "projectId"
              | "name"
              | "code"
              | "clientName"
              | "assignment"
              | "contractPrice"
              | "startDate"
              | "endDate"
            >
          )
        }
        classNames={{
          base: "max-h-[100vh] w-full py-4 overflow-scroll",
          table: "min-h-[15vh]",
        }}
      >
        <TableHeader>
          <TableColumn allowsSorting={true} key="name">
            Project
          </TableColumn>
          <TableColumn allowsSorting={true} key="code">
            Code
          </TableColumn>
          <TableColumn allowsSorting={true} key="clientName">
            Client
          </TableColumn>
          <TableColumn allowsSorting={true} key="assignment">
            Assignment
          </TableColumn>
          <TableColumn allowsSorting={true} key="contractPrice">
            Contract Price
          </TableColumn>
          <TableColumn allowsSorting={true} key="startDate">
            Start
          </TableColumn>
          <TableColumn allowsSorting={true} key="endDate">
            End
          </TableColumn>
          <TableColumn key="action">#</TableColumn>
        </TableHeader>
        <TableBody
          items={sortedItems as Array<ProjectTableItemStructure>}
          emptyContent={isLoading ? "" : "No records to display."}
          isLoading={isLoading}
          loadingContent={<Spinner label="Loading..." />}
        >
          {(item) => (
            <TableRow key={`${item.code}-${item.projectId}`}>
              <TableCell key={`${item.code}-${item.projectId}N`}>
                {item.name}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}C`}>
                {item.code}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}CN`}>
                {item.clientName}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}A`}>
                {item.assignment}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}CP`}>
                {item.contractPrice}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}SD`}>
                {formatDate(item.startDate)}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}ED`}>
                {formatDate(item.endDate)}
              </TableCell>
              <TableCell key={`${item.code}-${item.projectId}AC1`}>
                <div className="relative flex items-center gap-2">
                  <Button
                    isIconOnly
                    color="warning"
                    variant="faded"
                    aria-label="Edit Project Price"
                    onClick={() =>
                      openEditProjectPriceModal(
                        item.projectId,
                        item.contractPrice,
                        item.name,
                        item.code
                      )
                    }
                  >
                    <FaCreditCard />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </MainContainer>
  );
};

export default Projects;
