export type TableSortDescriptor<T> = {
  column: T;
  direction: "ascending" | "descending";
};
