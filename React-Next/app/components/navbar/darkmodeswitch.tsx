import React from "react";
import { useTheme as useNextTheme } from "next-themes";
import { Switch } from "@nextui-org/react";

export const DarkModeSwitch = () => {
  const { setTheme, resolvedTheme } = useNextTheme();
  return (
    <div className="flex flex-row gap-4 items-center">
      <span>Switch to {resolvedTheme === "dark" ? "Light" : "Dark"}</span>
      <Switch
        isSelected={resolvedTheme === "dark" ? true : false}
        onValueChange={(e) => setTheme(e ? "dark" : "light")}
      />
    </div>
  );
};
