export type ProjectTableListItemsRequest = {
  page: number;
};

export type ProjectTableListItemsResponse = {
  totalPages: number;
  results: Array<ProjectTableItemStructure>;
};

export type ProjectTableItemStructure = {
  projectId: number;
  name: string;
  code: string;
  clientName: string;
  assignment: string;
  contractPrice: string;
  startDate: Date;
  endDate: Date;
};
