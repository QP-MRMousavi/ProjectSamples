import { Decimal } from "@prisma/client/runtime/library";

export type UserActivitiesPerWeek = {
  userId: number;
  name: string;
  week: number;
  weekStartDate: Date;
  weekEndDate: Date;
  type: string;
  project: string;
  subProject: string;
  approver: string;
  approverAction: string;
  weekDayOne: Decimal;
  weekDayOneDate: Date;
  weekDayTwo: Decimal;
  weekDayTwoDate: Date;
  weekDayThree: Decimal;
  weekDayThreeDate: Date;
  weekDayFour: Decimal;
  weekDayFourDate: Date;
  weekDayFive: Decimal;
  weekDayFiveDate: Date;
  weekDaySix: Decimal;
  weekDaySixDate: Date;
  weekDaySeven: Decimal;
  weekDaySevenDate: Date;
  totalWorkedHoursInWeek: Decimal;
  note: string;
};

export type UserActivitiesPerWeekResults = {
  [key: string]: Array<UserActivitiesPerWeek>;
};

export type UserActivitiesPerWeekExcelReport = {
  index: number;
  Name: string;
  Week: number;
  Type: string;
  Project: string;
  subProject: string;
  Approver: string;
  ApproverAction: string;
  WD1: string;
  Note: string;
  weekDayDate: Date;
};
