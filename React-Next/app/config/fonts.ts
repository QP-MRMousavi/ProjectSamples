import { NextFontWithVariable } from "next/dist/compiled/@next/font";
import { Fira_Code as FontMono, Inter as FontSans } from "next/font/google";

export const fontSans: NextFontWithVariable = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const fontMono: NextFontWithVariable = FontMono({
  subsets: ["latin"],
  variable: "--font-mono",
});
