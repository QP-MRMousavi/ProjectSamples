import React from "react";

interface Props {
  children?: React.ReactNode;
}

export const MainContainer = ({ children }: Props) => {
  return (
    <main className="h-full lg:px-6 pb-5">
      <div className="flex flex-col justify-center gap-4 xl:gap-6 pt-3 px-4 lg:px-0  flex-wrap xl:flex-nowrap sm:pt-10 max-w-[90rem] mx-auto w-full">
        {children}
      </div>
    </main>
  );
};
