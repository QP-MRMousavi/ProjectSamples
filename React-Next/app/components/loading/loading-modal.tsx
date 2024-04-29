import React from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Progress,
  Image,
} from "@nextui-org/react";
import { LoadingModalProps } from "@/schemas/components";

export const LoadingModal = ({
  title,
  description,
  isOpen,
}: LoadingModalProps) => {
  return (
    <Modal size="lg" backdrop="blur" isOpen={isOpen} hideCloseButton={true}>
      <ModalContent>
        <>
          <ModalHeader className="flex flex-col gap-1">{title}</ModalHeader>
          <ModalBody className="flex flex-col gap-4">
            <div className="w-full flex justify-center">
              <Image className="max-w-40" src="/img/tms-logo.png" />
            </div>
            <p>{description}</p>
          </ModalBody>
          <ModalFooter>
            <Progress
              size="sm"
              isIndeterminate
              aria-label="Loading..."
              className="max-w-md"
            />
          </ModalFooter>
        </>
      </ModalContent>
    </Modal>
  );
};
